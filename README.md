# آشا (ASHA) — کارخانه ایجنت چندپلتفرمی

**نسخه:** 1.0.0 | **وضعیت:** Ship-Ready | **۴۸ تست PASS**

## نصب

```bash
cd asha
pip install -r requirements.txt
cp .env.example .env
python -m pytest tests/ -v
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

## API

- GET /health
- GET /agents
- POST /tasks  body: {"agent_id":"sales_closer","payload":{...}}
- GET /tasks/{task_id}
- GET /adapters/{platform}/health
- POST /adapters/{platform}/send

## اجزا

- ۱۵ ایجنت | ۸ Adapter | هسته کامل | FastAPI | Docker
