# استقرار آشا (ASHA Deployment)

**نسخه مستند:** 0.1.0  
**تاریخ:** 2026-09-14

## پیش‌نیازها

- Python 3.11+
- PostgreSQL
- Redis
- Docker (توصیه می‌شود)

## مراحل استقرار (پس از تکمیل فاز ۱)

1. کپی `.env.example` به `.env` و پر کردن مقادیر
2. نصب وابستگی‌ها
3. اجرای migrations
4. راه‌اندازی سرویس‌ها با Docker Compose (در فازهای بعدی اضافه می‌شود)

## وضعیت فعلی

فاز ۱ هنوز در حال توسعه است. استقرار Production فقط پس از تکمیل فاز ۸ و Human Review Gate مجاز است.

## استقرار روی Render.com

راهنمای کامل: [deployment-render.md](./deployment-render.md)

خلاصه سریع:
- فایل `render.yaml` در ریشه پروژه آماده است.
- Start Command: `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`
- Health Check: `/health`
- Region پیشنهادی: Frankfurt
