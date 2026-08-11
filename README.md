# react-testing-academy — Bloque 2 (Python)

Repositorio de prácticas del curso. Todo el código fuente vive en `src/` y todos los
tests en `test/`, con las fixtures compartidas en `test/conftest.py`.

## Puesta en marcha

```bash
uv sync          # instala pytest, fastapi, sqlalchemy, hypothesis, pytest-cov, pytest-xdist
uv run pytest -v
```

## Mapa de archivos

| Archivo | Sesión / bloque |
|---|---|
| `src/descuentos.py` + `test/test_descuentos.py` | S1-S2 — parametrización |
| `src/notificador.py` + `test/test_notificador.py` | S2 — mocking de dependencias externas |
| `src/gestor_pedidos.py` + `test/test_gestor_pedidos.py` | S2 — práctica libre |
| `src/app.py` + `test/conftest.py` + `test/test_api_pedidos.py` | **S3 — Bloque 2.3: testing de APIs** |
| `test/test_hypothesis_descuentos.py` | **S3 — Bloque 2.4: cobertura + property-based** |

Los tests con `# TODO` de `test_api_pedidos.py` y `test_hypothesis_descuentos.py` se
completan en directo durante la Sesión 3.

## Sesión 3 — comandos de la sesión

Cobertura (Bloque 2.4). El gancho del guión: con solo las 2 properties completas
el módulo ronda el **31%**; al completar los TODO sube.

```bash
uv run pytest --cov=src.descuentos --cov-report=term-missing test/test_hypothesis_descuentos.py
uv run pytest --cov=src --cov-report=term-missing        # cobertura de todo el paquete
uv run pytest --cov=src --cov-fail-under=80              # umbral tipo CI
```

Selección de tests desde la terminal (chuleta de las 09:10):

```bash
uv run pytest -k "descuento"   # por nombre
uv run pytest -m "not lento"   # por marcador
uv run pytest -x               # para en el primer fallo
uv run pytest --lf             # solo los que fallaron la última vez
uv run pytest -s               # muestra los print()
uv run pytest --pdb            # debugger en el punto del fallo
uv run pytest -n auto          # paralelo entre cores (pytest-xdist)
```

## Notas

- El `client` de `test/conftest.py` sobrescribe la dependencia `get_db` de FastAPI por
  una sesión SQLite **en memoria** (`StaticPool`), con `rollback` en el teardown del
  `yield`. Ningún test toca `pedidos.db` ni la red.
- `test_calcular_descuento_nunca_negativo` compara con `pytest.approx`: con
  `porcentaje=100` la aritmética de floats devuelve `-3.6e-12` y hypothesis lo
  encuentra. Es un ejemplo real de caso límite, no un apaño.
