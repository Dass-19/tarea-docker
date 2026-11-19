<p align="center">
  <img src="docs/assets/logo.svg" width="460" alt="DASS">
</p>

<h3 align="center">Customer Data Transformation</h3>

<p align="center">
  A container that reads a customer CSV, cleans and normalizes the data<br>
  (duplicates, ages, gender, income, dates, satisfaction, subscription) and writes the result to another CSV.
</p>

<p align="center">
  <img src="docs/assets/accent-bar.svg" width="520" alt="">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.13-537195?style=flat-square&logo=python&logoColor=white" alt="Python 3.13">
  <img src="https://img.shields.io/badge/docker-slim%20image-537195?style=flat-square&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/pandas-3.1.1-b89146?style=flat-square&logo=pandas&logoColor=white" alt="pandas 3.1.1">
  <img src="https://img.shields.io/badge/numpy-2.4.6-b89146?style=flat-square&logo=numpy&logoColor=white" alt="numpy 2.4.6">
  <img src="https://img.shields.io/badge/user-non--root-844747?style=flat-square" alt="Non-root user">
  <img src="https://img.shields.io/badge/uv-package%20manager-5b635d?style=flat-square" alt="uv">
</p>

<p align="center">
  <a href="#build">Build</a> ·
  <a href="#run">Run</a> ·
  <a href="#environment-variables">Environment variables</a> ·
  <a href="#volumes">Volumes</a> ·
  <a href="#example-with-expected-output">Example</a>
</p>

---

## Build

```bash
docker build -t dass-transformation .
```

## Run

With the default paths, mounting the output folder to keep the result:

```bash
docker run --rm -v "$(pwd)/data/processed:/app/data/processed" dass-transformation
```

> **Tip:** in PowerShell, use `${PWD}` instead of `$(pwd)`.

With custom input and output paths:

```bash
docker run --rm \
  -v "$(pwd)/data/raw:/in" \
  -v "$(pwd)/output:/out" \
  -e INPUT_PATH=/in/data.csv \
  -e OUTPUT_PATH=/out/clean.csv \
  dass-transformation
```

## Environment variables

| Variable      | Description              | Default                          |
|---------------|--------------------------|----------------------------------|
| `INPUT_PATH`  | Path to the input CSV    | `/app/data/raw/data.csv`         |
| `OUTPUT_PATH` | Path to the output CSV   | `/app/data/processed/data.csv`   |

If the `OUTPUT_PATH` folder does not exist, the script creates it.

## Volumes

| Container path         | Purpose                                     |
|------------------------|---------------------------------------------|
| `/app/data/raw`        | Input. The image already includes a sample `data.csv`; mount this folder to use a different file. |
| `/app/data/processed`  | Output. Mount it to keep the result: without a volume, the file is lost when the container exits. |

> **Note:** the container runs as the unprivileged user `appuser`, so the mounted output folder must be writable by it.

## Example with expected output

```bash
docker run --rm -v "$(pwd)/data/processed:/app/data/processed" dass-transformation
```

The command prints nothing to the console and exits with code `0`. It creates `data/processed/data.csv`.

**Input** (`data/raw/data.csv`, 203 rows):

```csv
id_cliente,nombre_completo,edad,genero,ciudad,ingreso_mensual,fecha_registro,compras_ultimo_mes,gasto_total,satisfaccion,suscripcion_activa
USR-1066,Luis Torres,34.0,F,Cuenca,2484.96,2023-06-24,14.0,512.2,1.0,NO
USR-1187,Andrés López,74.0,,Guayaquil,1226.05,02/02/2025,17.0,1203.52,5.0,0
USR-1101,Valentina Vargas,74.0,Femenino,Guayaquil,1763.53,04-16-2026,12.0,441.22,3.0,0
```

**Output** (`data/processed/data.csv`, 195 rows after removing duplicates):

```csv
id_cliente,nombre_completo,edad,genero,ciudad,ingreso_mensual,fecha_registro,compras_ultimo_mes,gasto_total,satisfaccion,suscripcion_activa
USR-1066,Luis Torres,34,Femenino,Cuenca,2484.96,2023-06-24,14,512.2,1,False
USR-1187,Andrés López,74,No especificado,Guayaquil,1226.05,2025-02-02,17,1203.52,5,False
USR-1101,Valentina Vargas,74,Femenino,Guayaquil,1763.53,2026-04-16,12,441.22,3,False
```

Visible changes:

- Ages and counts become integers.
- Gender is normalized (`F` → `Femenino`, empty → `No especificado`).
- Dates use the `YYYY-MM-DD` format.
- Subscription becomes a boolean.

To check that the container does not run as root:

```bash
docker run --rm dass-transformation whoami
# appuser
```
