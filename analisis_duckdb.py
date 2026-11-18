"""Preentrega 6 - Análisis de clima con DuckDB: SQL directo sobre un archivo CSV."""
import time

import duckdb

ARCHIVO = "data/clima.csv"

# DuckDB en memoria: no crea ningún archivo de base de datos
con = duckdb.connect(database=":memory:")

# Registro el CSV como tabla virtual, con limpieza básica de nulos en temperaturas
con.execute(f"""
    CREATE VIEW clima AS
    SELECT estacion,
           CAST(fecha AS DATE) AS fecha,
           temp_max,
           temp_min,
           precipitacion_mm
    FROM read_csv_auto('{ARCHIVO}')
    WHERE temp_max IS NOT NULL AND temp_min IS NOT NULL
""")

consultas = {
    "1) Registros válidos por estación (conteo)": """
        SELECT estacion, COUNT(*) AS dias_registrados
        FROM clima
        GROUP BY estacion
        ORDER BY estacion
    """,
    "2) Promedio mensual de temperatura máxima por estación (promedios)": """
        SELECT estacion,
               strftime(date_trunc('month', fecha), '%Y-%m') AS mes,
               ROUND(AVG(temp_max), 1) AS temp_max_promedio
        FROM clima
        GROUP BY estacion, date_trunc('month', fecha)
        ORDER BY estacion, mes
        LIMIT 12
    """,
    "3) Máximo histórico por estación (agregación)": """
        SELECT estacion, MAX(temp_max) AS maximo_historico
        FROM clima
        GROUP BY estacion
        ORDER BY maximo_historico DESC
    """,
    "4) Días calurosos y lluviosos (filtrado complejo)": """
        SELECT estacion, fecha, temp_max, precipitacion_mm
        FROM clima
        WHERE temp_max > 28 AND precipitacion_mm > 10
        ORDER BY precipitacion_mm DESC
        LIMIT 10
    """,
}

for titulo, sql in consultas.items():
    t0 = time.perf_counter()
    resultado = con.execute(sql).df()
    ms = (time.perf_counter() - t0) * 1000
    print(f"\n=== {titulo} === ({ms:.1f} ms)")
    print(resultado.to_string(index=False))

con.close()
