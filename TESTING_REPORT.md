# TESTING_REPORT.md

## Resumen ejecutivo de hallazgos

## Lista de bugs encontrados con referencias a los Issues

## Metricas de coverage alcanzadas

## Recomendaciones de mejora

## Instrucciones para ejecutar las pruebas
1. docker compose up --build
2. docker compose exec api pytest tests/test_api.py
3. docker compose exec api pytest --cov=app --cov-report=html tests/
4. start htmlcov/index.html




