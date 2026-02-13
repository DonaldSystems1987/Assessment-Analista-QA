# TESTING_REPORT.md

## Resumen ejecutivo de hallazgos

ste documento resume los hallazgos de las pruebas realizadas sobre la Inventory Management API. Se realizaron pruebas unitarias y de integración para validar la autenticación, autorización y gestión de productos/inventario.

Tests unitarios ejecutados: 6 / 6 pasaron 

Tests de integración/API ejecutados: 7 / 7 pasaron 

Cobertura de código: Se recomienda generar con pytest --cov=app --cov-report=html tests/ para verificar cobertura completa de la carpeta app/.

Hallazgos críticos y de mejora se listan en la sección de Bugs.

## Lista de bugs encontrados con referencias a los Issues

-Low-stock retorna productos con stock alto
- Cálculo de valor de inventario incorrecto
- Deprecation warning datetime.utcnow()
- Token expirado no lanza error

## Metricas de coverage alcanzadas

## Recomendaciones de mejora
Corregir la función /inventory/low-stock para filtrar correctamente productos con quantity < min_stock.

Corregir /inventory/value para sumar correctamente price * quantity de todos los productos.

Actualizar uso de datetime.utcnow() a datetime.now(timezone.utc) para eliminar warnings de deprecación.

Modificar verify_token para lanzar error 401 en caso de token expirado.

Mantener buena práctica de tests y commits frecuentes con mensajes descriptivos.

## Instrucciones para ejecutar las pruebas
1. docker compose up --build
python -m pip install -r requirements.txt
python -m pip install -r requirements-test.txt
python -m pytest tests/test_unit.py
python -m pytest tests/test_api.py
pytest --cov=app --cov-report=html tests/
https://docs.pytest.org/en/stable/how-to/capture-warnings.html







