# Rutina Tracker

Tracker de rutina de gimnasio pensado para el celular: marcás los días entrenados, ves los ejercicios de cada día con GIFs de técnica, y la rutina de cada persona se configura desde una planilla de Google Sheets, sin tocar código.

Funciona como PWA: se puede instalar en la pantalla de inicio y anda sin conexión en el gimnasio.

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
| `Seccion` | `Calentamiento`, `Principal`, `Accesorios` o `Estiramiento`. |
| `Orden` | Orden dentro del día (`1`, `2a`, `2b`…). `2a`/`2b` es la convención para superseries. |
| `Ejercicio` | Nombre exacto del catálogo `Ejercicios`. |
| `Series` | Ej: `4 × 6–8`. |
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
