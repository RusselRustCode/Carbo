# Carbon Polygon Backend (scaffold)

Minimal scaffold for Carbon Polygon backend using FastAPI, SQLAlchemy 2.0 (async) and Pydantic v2.

Run development server:

```bash
export DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/carbon
uvicorn app.main:app --reload
```
