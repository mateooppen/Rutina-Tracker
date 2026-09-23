# Rutina Tracker

Tracker de rutina de gimnasio pensado para el celular: marcás los días entrenados, ves los ejercicios de cada día con GIFs de técnica, y la rutina de cada persona se configura desde una planilla de Google Sheets, sin tocar código.

Funciona como PWA: se puede instalar en la pantalla de inicio y anda sin conexión en el gimnasio.

## Qué hace

- **Rutina**: tus días de entrenamiento; cada día abre su pantalla con calentamiento, bloques de ejercicios (las superseries son un bloque) y estiramientos.
- **Registro de series**: al tocar un ejercicio aparecen sus series con peso y reps precargados de la última vez; confirmás cada serie con un toque. Muestra "Última vez" y la meta del día (te avisa cuándo subir el peso). La técnica (fotos + pasos) queda en un panel "Ver técnica".
- **Timer de descanso**: arranca solo al confirmar una serie (en superseries, después del ejercicio B), con ±15 s y saltar; vibra y suena al terminar. La pantalla no se apaga mientras entrenás.
- **Progreso**: semana actual, días completados e historial.
- **Ajustes**: usuario, planilla de Google Sheets, respaldo (exportar/importar JSON) y glosario.

## Estructura

- **`index.html`** — toda la app (HTML + CSS + JS vanilla, sin dependencias ni build).
- **`sw.js`** / **`manifest.json`** / **`icon*.{svg,png}`** — soporte PWA (offline e instalación).
- **`assets/`** — GIFs e imágenes de técnica de los ejercicios (`thumbs/` tiene las miniaturas).
- **`plantilla/`** — CSVs para crear tu planilla de Google Sheets con el formato esperado.

## Cómo configurar la rutina (Google Sheets)

1. Creá una planilla nueva en [Google Sheets](https://sheets.new).
2. Importá `plantilla/Ejercicios.csv` (Archivo → Importar → Subir → "Insertar hojas nuevas") y renombrá la pestaña a **`Ejercicios`**. Repetí con `plantilla/Rutinas.csv` en una pestaña **`Rutinas`**. Los nombres de las pestañas tienen que ser exactamente esos.
3. Compartila: botón **Compartir → Cualquier persona con el enlace → Lector**.
4. En la app, abrí **Configuración y datos**, pegá el link de la planilla y tocá **Conectar y sincronizar**.

La app cachea los datos en el teléfono: la planilla solo hace falta cuando cambiás la rutina (volvé a tocar sincronizar, o reabrí la app con conexión). El progreso de cada usuario (semanas, historial) se guarda localmente en cada dispositivo.

### Pestaña `Ejercicios` (catálogo, compartido entre todos)

| Columna | Qué va |
|---|---|
| `Ejercicio` | Nombre del ejercicio (es la clave que usa `Rutinas`). |
| `Grupo` | Grupo muscular (informativo). |
| `Media` | Archivo de `assets/` (ej: `leg_press.gif`) o una URL completa de imagen. Vacío = sin imagen. |
| `Pasos` | Pasos de técnica separados por `\|` (barra vertical). |
| `Tip` | Consejo corto de técnica. |
| `Alternativa` | Texto con el ejercicio alternativo si la máquina está ocupada. |

### Pestaña `Rutinas` (una fila por ejercicio y día, por usuario)

| Columna | Qué va |
|---|---|
| `Usuario` | Nombre de la persona. Cada nombre distinto aparece como un usuario en la app. |
| `Semana` | `A`, `B`… si la rutina alterna tipos de semana; vacío si todas las semanas son iguales. |
| `Dia` | Número de día (1, 2, 3…). La cantidad de días de la rutina sale de acá. Vacío = fila de calentamiento/estiramiento general. |
| `DiaNombre` | Nombre del día (ej: "Piernas y glúteos"). |
| `Seccion` | `Calentamiento`, `Principal`, `Secundario`, `Accesorios`, `Opcional`, `Estiramiento` u otro nombre (se muestra como título). Las filas de `Calentamiento`/`Estiramiento` con `Dia` vacío valen para todos los días; con un `Dia`, solo para ese día (p. ej. un día en casa con su propio calentamiento). |
| `Orden` | Orden dentro del día (`1`, `2a`, `2b`…). `2a`/`2b` es la convención para superseries. |
| `Ejercicio` | Nombre exacto del catálogo `Ejercicios`. |
| `Series` | Ej: `4 × 6–8`. También tiempos: `3 × 20 seg`, `90 seg por pierna`. |
| `Intensidad` | Ej: `RPE 8` o `RIR 2`. Opcional. |
| `Descanso` | Ej: `90 seg`. Opcional. |
| `Tag` | `principal`, `superserie`, `dropset` o `finisher`. Opcional. |
| `Nota` | Aclaración que se muestra como etiqueta (ej: "Superserie con 2b"). |

## Desarrollo

Servir la carpeta con cualquier servidor estático (el service worker no funciona con `file://`):

```bash
npx serve .
```

Al modificar `index.html` u otros archivos del shell, subí la versión de `CACHE` en `sw.js` para que los teléfonos tomen la actualización.

## Créditos

Los GIFs de técnica vienen del repo [rutina](https://github.com/mateooppen/rutina).

Las fotos de `assets/db/` (pares inicio/final) vienen de [free-exercise-db](https://github.com/yuhonas/free-exercise-db), dominio público (Unlicense). En la planilla se referencian como `db/Nombre` (sin extensión) y la app las alterna con un fundido.

Las ilustraciones de `assets/rep/` son de RepDB: "Exercise data by RepDB (repdb.co)", uso libre dentro de aplicaciones con atribución (ver su [LICENSE-DATA](https://github.com/RepDB/exercise-dataset/blob/main/LICENSE-DATA.md)). En la planilla se referencian como `rep/<id>` (par inicio/fin) o `rep/<archivo>.webp` (imagen única).

Las ilustraciones de `assets/gen/` son propias, generadas localmente con ComfyUI (Qwen Image Edit) a partir de referencias de pose. En la planilla se referencian como `gen/<nombre>` (par `-inicio.png`/`-final.png`) o `gen/<archivo>.png` (imagen única).
