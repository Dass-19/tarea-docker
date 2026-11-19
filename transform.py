import os

import numpy as np
import pandas as pd

# Paths configurable via environment variables
input_path = os.environ.get("INPUT_PATH", "data/raw/data.csv")
output_path = os.environ.get("OUTPUT_PATH", "data/processed/data.csv")


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the input DataFrame by performing various data cleaning and transformation operations.

    Parameters:
    df (pd.DataFrame): The input DataFrame to be transformed.

    Returns:
    pd.DataFrame: The transformed DataFrame.
    """
    # Remove duplicate rows based on 'id_cliente' column
    df = df.drop_duplicates(subset=["id_cliente"], keep="first")

    # Filter out rows where 'edad' is less than or equal to 0
    df.loc[(df["edad"] < 18) | (df["edad"] > 100), "edad"] = np.nan
    df["edad"] = df["edad"].fillna(df["edad"].median()).astype(int)

    # Clean and standardize the 'nombre_completo' column
    df["nombre_completo"] = df["nombre_completo"].str.strip().str.title()

    # Map gender values to standardized categories
    mapa_genero = {
    "M": "Masculino",
    "m": "Masculino",
    "Masculino": "Masculino",
    "F": "Femenino",
    "f": "Femenino",
    "Femenino": "Femenino",
    "Otro": "Otro",
    "No binario": "Otro",
    }
    df["genero"] = df["genero"].map(mapa_genero).fillna("No especificado")

    # Clean and convert 'ingreso_mensual' to numeric
    df["ingreso_mensual"] = (
    df["ingreso_mensual"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
    )
    df["ingreso_mensual"] = pd.to_numeric(df["ingreso_mensual"], errors="coerce")

    # Handle outliers in 'ingreso_mensual' using the IQR method
    Q1 = df["ingreso_mensual"].quantile(0.25)
    Q3 = df["ingreso_mensual"].quantile(0.75)
    IQR = Q3 - Q1
    limite_superior = Q3 + 1.5 * IQR

    df.loc[df["ingreso_mensual"] > limite_superior, "ingreso_mensual"] = np.nan
    df["ingreso_mensual"] = (
        df["ingreso_mensual"].fillna(df["ingreso_mensual"].median()).round(2)
    )

    # Convert 'fecha_registro' to datetime, handling mixed formats and filling missing values with the median date
    df["fecha_registro"] = pd.to_datetime(
    df["fecha_registro"], format="mixed", errors="coerce"
    )
    df["fecha_registro"] = df["fecha_registro"].fillna(df["fecha_registro"].median())

    # Handle outliers in 'satisfaccion' by replacing values outside the range [1, 5] with NaN and filling them with the median
    df.loc[(df["satisfaccion"] < 1) | (df["satisfaccion"] > 5), "satisfaccion"] = (
    np.nan
    )
    df["satisfaccion"] = (
        df["satisfaccion"].fillna(df["satisfaccion"].median()).astype(int)
    )

    # Handle missing values in 'compras_ultimo_mes' and 'gasto_total' columns
    df["compras_ultimo_mes"] = df["compras_ultimo_mes"].fillna(0).astype(int)
    df["gasto_total"] = (
        df["gasto_total"].fillna(df["gasto_total"].median()).round(2)
    )

    # Map 'suscripcion_activa' values to boolean
    mapa_bool = {
    "Sí": True,
    "si": True,
    "1": True,
    "True": True,
    "No": False,
    "NO": False,
    "0": False,
    "False": False,
    }
    df["suscripcion_activa"] = (
        df["suscripcion_activa"].astype(str).map(mapa_bool).fillna(False)
    )

    return df

# Read the raw CSV file, transform the data, and save the transformed DataFrame to a new CSV file
df = pd.read_csv(input_path)
transformed_df = transform_data(df)
os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
transformed_df.to_csv(output_path, index=False)
