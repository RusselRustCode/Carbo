# Carbon Polygon Backend (scaffold)

Minimal scaffold for Carbon Polygon backend using FastAPI, SQLAlchemy 2.0 (async) and Pydantic v2.

Run development server:

```bash
export DATABASE_URL=postgresql+asyncpg://carbon:carbon@localhost:5432/carbon_polygon

uvicorn app.main:app --reload
```
