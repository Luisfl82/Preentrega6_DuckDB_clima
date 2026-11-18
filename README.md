# Preentrega 6 - Análisis de datos meteorológicos con DuckDB y SQL

Se consulta un CSV de clima **directamente con SQL** usando DuckDB como motor embebido (sin instalar ni cargar datos en MySQL/PostgreSQL y sin generar archivos binarios de base de datos).

## Cómo replicar
1. `pip install -r requirements.txt`
2. `python generar_datos_clima.py`  (crea `data/clima.csv`; también podés usar un CSV de NOAA con las mismas columnas)
3. `python analisis_duckdb.py`

## Qué hace el análisis
- Registra el CSV como vista con `read_csv_auto` (consulta directa sobre el archivo).
- **Limpieza:** descarta filas con temperaturas nulas.
- 4 consultas: conteo de registros por estación, promedio mensual de temperatura máxima, máximo histórico por estación y filtro complejo (días > 28 °C con lluvia > 10 mm).

## Hallazgos principales
_(completar con los números que imprime tu ejecución)_
- Estación con mayor máximo histórico: ...
- Estación más fría en promedio: ...
- Tiempos de respuesta: cada consulta tarda pocos milisegundos (se imprime en pantalla).

## Notas
- La base corre en memoria (`:memory:`), por eso no se suben archivos `.duckdb`.
