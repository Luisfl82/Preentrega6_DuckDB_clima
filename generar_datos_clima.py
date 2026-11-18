"""Genera un CSV de clima de ejemplo (3 estaciones, 2 años) con algunos nulos.
Si querés datos reales, bajá un CSV de NOAA y poné el mismo formato de columnas."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(3)
fechas = pd.date_range("2023-01-01", "2024-12-31", freq="D")
filas = []
for est, base in [("La Plata", 17), ("Bariloche", 8), ("Salta", 20)]:
    estacional = 8 * np.sin((fechas.dayofyear.values - 80) / 365 * 2 * np.pi)
    temp = base + estacional + rng.normal(0, 2, len(fechas))
    filas.append(pd.DataFrame({
        "estacion": est, "fecha": fechas,
        "temp_max": (temp + 5).round(1), "temp_min": (temp - 5).round(1),
        "precipitacion_mm": rng.gamma(0.5, 6, len(fechas)).round(1),
    }))
df = pd.concat(filas, ignore_index=True)
df.loc[df.sample(40, random_state=1).index, "temp_max"] = np.nan
df.to_csv("data/clima.csv", index=False)
print("Creado data/clima.csv con", len(df), "filas")
