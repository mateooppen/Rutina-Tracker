/* Service worker de Rutina Tracker.
 * - Precachea el shell de la app para que funcione offline.
 * - Cachea los GIFs de assets/ a medida que se ven (cache-first).
 * Al publicar cambios, subí la versión de CACHE para invalidar lo viejo. */
const CACHE = 'rtm-v4';
const SHELL = ['./', 'manifest.json', 'icon.svg', 'icon-180.png', 'icon-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return; // p. ej. Google Sheets: directo a la red

  // Assets (GIFs/imágenes): cache-first, no cambian seguido.
  if (url.pathname.includes('/assets/')) {
    e.respondWith(
      caches.match(e.request).then(hit => hit || fetch(e.request).then(res => {
        if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); }
        return res;
      }))
    );
    return;
  }

  // Shell: red primero (para tomar actualizaciones), cache si no hay señal.
  e.respondWith(
    fetch(e.request).then(res => {
      if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); }
      return res;
    }).catch(() => caches.match(e.request).then(hit => hit || caches.match('./')))
  );
});
