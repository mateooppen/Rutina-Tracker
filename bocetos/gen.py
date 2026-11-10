"""Uso: python -I gen.py <imagen_referencia> <seed> <prefijo> <prompt.txt> [salida.png]
Sube la referencia a ComfyUI, corre el workflow Qwen Image Edit y descarga el resultado."""
import sys, json, time, uuid, urllib.request, mimetypes, os

HOST = 'http://127.0.0.1:8188'
img, seed, prefix, prompt_file = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
out = sys.argv[5] if len(sys.argv) > 5 else prefix + '.png'
prompt = open(prompt_file, encoding='utf-8').read().strip()

# --- subir imagen (multipart a mano) ---
name = os.path.basename(img)
boundary = uuid.uuid4().hex
data = open(img, 'rb').read()
body = (f'--{boundary}\r\nContent-Disposition: form-data; name="image"; filename="{name}"\r\n'
        f'Content-Type: {mimetypes.guess_type(name)[0] or "application/octet-stream"}\r\n\r\n').encode() + data + \
       (f'\r\n--{boundary}\r\nContent-Disposition: form-data; name="overwrite"\r\n\r\ntrue\r\n--{boundary}--\r\n').encode()
req = urllib.request.Request(HOST + '/upload/image', body, {'Content-Type': f'multipart/form-data; boundary={boundary}'})
up = json.load(urllib.request.urlopen(req))
print('subida:', up['name'])

g = {
  '1': {'class_type': 'UNETLoader', 'inputs': {'unet_name': 'qwen_image_edit_2509_fp8_e4m3fn.safetensors', 'weight_dtype': 'default'}},
  '2': {'class_type': 'LoraLoaderModelOnly', 'inputs': {'model': ['1', 0], 'lora_name': 'Qwen-Edit-2509-Lightning-4steps.safetensors', 'strength_model': 1}},
  '3': {'class_type': 'ModelSamplingAuraFlow', 'inputs': {'model': ['2', 0], 'shift': 3}},
  '4': {'class_type': 'CFGNorm', 'inputs': {'model': ['3', 0], 'strength': 1}},
  '5': {'class_type': 'CLIPLoader', 'inputs': {'clip_name': 'qwen_2.5_vl_7b_fp8_scaled.safetensors', 'type': 'qwen_image', 'device': 'default'}},
  '6': {'class_type': 'VAELoader', 'inputs': {'vae_name': 'qwen_image_vae.safetensors'}},
  '7': {'class_type': 'LoadImage', 'inputs': {'image': up['name'], 'upload': 'image'}},
  '8': {'class_type': 'ImageScaleToTotalPixels', 'inputs': {'image': ['7', 0], 'upscale_method': 'lanczos', 'megapixels': 1, 'resolution_steps': 8}},
  '9': {'class_type': 'TextEncodeQwenImageEditPlus', 'inputs': {'clip': ['5', 0], 'vae': ['6', 0], 'image1': ['8', 0], 'prompt': prompt}},
  '10': {'class_type': 'TextEncodeQwenImageEditPlus', 'inputs': {'clip': ['5', 0], 'vae': ['6', 0], 'image1': ['8', 0], 'prompt': ''}},
  '11': {'class_type': 'VAEEncode', 'inputs': {'pixels': ['8', 0], 'vae': ['6', 0]}},
  '12': {'class_type': 'KSampler', 'inputs': {'model': ['4', 0], 'positive': ['9', 0], 'negative': ['10', 0], 'latent_image': ['11', 0],
          'seed': seed, 'steps': 4, 'cfg': 1, 'sampler_name': 'euler', 'scheduler': 'simple', 'denoise': 1}},
  '13': {'class_type': 'VAEDecode', 'inputs': {'samples': ['12', 0], 'vae': ['6', 0]}},
  '14': {'class_type': 'SaveImage', 'inputs': {'images': ['13', 0], 'filename_prefix': 'rutina/' + prefix}},
}
req = urllib.request.Request(HOST + '/prompt', json.dumps({'prompt': g}).encode(), {'Content-Type': 'application/json'})
try:
    r = json.load(urllib.request.urlopen(req))
except urllib.error.HTTPError as e:
    print('400:', e.read().decode('utf-8','replace')[:3000]); sys.exit(1)
pid = r['prompt_id']; print('prompt_id:', pid, 'errores:', r.get('node_errors') or 'ninguno')

t0 = time.time()
while True:
    time.sleep(3)
    h = json.load(urllib.request.urlopen(HOST + '/history/' + pid))
    if pid in h:
        st = h[pid].get('status', {})
        if st.get('status_str') == 'error':
            print('ERROR:', json.dumps(st.get('messages'), ensure_ascii=False)[:2000]); sys.exit(1)
        imgs = [o for n in h[pid]['outputs'].values() for o in n.get('images', [])]
        if imgs: break
    if time.time() - t0 > 900: print('timeout'); sys.exit(1)
o = imgs[0]
url = HOST + f"/view?filename={urllib.request.quote(o['filename'])}&subfolder={urllib.request.quote(o.get('subfolder',''))}&type={o['type']}"
open(out, 'wb').write(urllib.request.urlopen(url).read())
print('listo:', out, f'({time.time()-t0:.0f} s)')
