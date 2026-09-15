# استقرار آشا روی Render.com

**نسخه:** 1.0.0  
**تاریخ:** 2026-09-15

## پیش‌نیاز

1. حساب رایگان در [render.com](https://render.com)
2. ریپوی GitHub یا GitLab شامل پوشه `asha`
3. (اختیاری) کلید API پلتفرم‌های ایرانی

---

## روش ۱ — Blueprint (پیشنهادی)

1. کل پروژه `asha` را به یک ریپو پوش کنید.
2. در Render: **New → Blueprint**
3. ریپو را وصل کنید.
4. فایل `render.yaml` به‌صورت خودکار خوانده می‌شود.
5. سرویس `asha-api` ساخته می‌شود.
6. در بخش **Environment** کلیدهای API را پر کنید (اختیاری).
7. **Apply** بزنید.

بعد از چند دقیقه آدرس عمومی شبیه این می‌گیرید:

```
https://asha-api.onrender.com
```

بررسی سلامت:

```
https://asha-api.onrender.com/health
```

---

## روش ۲ — دستی (Web Service)

1. **New → Web Service**
2. ریپو را وصل کنید.
3. تنظیمات:

| فیلد | مقدار |
|------|--------|
| **Name** | `asha-api` |
| **Region** | Frankfurt (نزدیک‌تر به ایران) |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT` |
| **Plan** | Free |

4. **Advanced → Add Environment Variable:**

| Key | Value | توضیح |
|-----|--------|--------|
| `PYTHONPATH` | `.` | الزامی |
| `ASHA_ENV` | `production` | محیط اجرا |
| `ASHA_DEBUG` | `false` | خاموش کردن دیباگ |
| `ASHA_LOG_LEVEL` | `INFO` | سطح لاگ |
| `EITAA_API_KEY` | *(کلید شما)* | اختیاری |
| `BALE_API_KEY` | *(کلید شما)* | اختیاری |
| `RUBIKA_API_KEY` | *(کلید شما)* | اختیاری |
| `DIVAR_API_KEY` | *(کلید شما)* | اختیاری |
| `TOROB_API_KEY` | *(کلید شما)* | اختیاری |
| `EMALLS_API_KEY` | *(کلید شما)* | اختیاری |
| `TELEGRAM_BOT_TOKEN` | *(توکن)* | اختیاری |
| `INSTAGRAM_ACCESS_TOKEN` | *(توکن)* | اختیاری |

5. **Create Web Service**

---

## روش ۳ — Docker روی Render

1. **New → Web Service** → Docker
2. Dockerfile موجود در ریشه پروژه استفاده می‌شود.
3. **مهم:** Render پورت را با `$PORT` می‌دهد. اگر از Docker استفاده می‌کنید، Start Command را override کنید:

```bash
uvicorn src.api.main:app --host 0.0.0.0 --port $PORT
```

یا در Dockerfile به‌جای پورت ثابت از شل استفاده کنید (روش Blueprint/Python ساده‌تر است).

---

## بررسی بعد از استقرار

```bash
# سلامت
curl https://YOUR-SERVICE.onrender.com/health

# فهرست ایجنت‌ها
curl https://YOUR-SERVICE.onrender.com/agents

# ارسال وظیفه نمونه
curl -X POST https://YOUR-SERVICE.onrender.com/tasks \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"sales_closer","payload":{"customer_name":"علی","product":"گوشی","conversation":[{"text":"می‌خرم"}]}}'
```

پاسخ موفق `/health` شبیه این است:

```json
{
  "status": "ok",
  "orchestrator_running": true,
  "agents": ["sales_closer", "outbound", "..."],
  "adapters": ["eitaa", "bale", "..."]
}
```

---

## نکات پلن رایگان Render

| موضوع | توضیح |
|--------|--------|
| **Sleep** | بعد از حدود ۱۵ دقیقه بدون ترافیک، سرویس خواب می‌رود. اولین درخواست بعدی ~۳۰–۶۰ ثانیه طول می‌کشد. |
| **RAM** | حدود ۵۱۲MB — برای آشا کافی است (State و Event Bus در حافظه). |
| **بدون دیسک پایدار** | State فعلی in-memory است؛ با ری‌استارت پاک می‌شود. برای Production واقعی بعداً PostgreSQL اضافه کنید. |
| **بدون Redis اجباری** | نسخه فعلی Event Bus حافظه‌ای است؛ `REDIS_URL` فعلاً لازم نیست. |

---

## افزودن PostgreSQL (اختیاری — فاز بعد)

1. در Render: **New → PostgreSQL**
2. Internal Database URL را کپی کنید.
3. به عنوان `DATABASE_URL` به سرویس وب اضافه کنید.
4. در فاز بعد، State را به دیتابیس متصل کنید.

---

## افزودن Redis (اختیاری — فاز بعد)

1. **New → Redis**
2. `REDIS_URL` را به Environment اضافه کنید.
3. Event Bus را به Redis Streams مهاجرت دهید.

---

## عیب‌یابی رایج

| مشکل | راه‌حل |
|------|--------|
| Build fail | مطمئن شوید `requirements.txt` در ریشه است و `PYTHON_VERSION=3.12.3` ست شده. |
| `ModuleNotFoundError: src` | `PYTHONPATH=.` را در Environment بگذارید. |
| پورت اشتباه | Start Command حتماً `--port $PORT` داشته باشد (نه 8000 ثابت). |
| Health check fail | مسیر `/health` باید 200 برگرداند؛ در Blueprint از قبل تنظیم شده. |
| سرویس خواب | روی پلن رایگان طبیعی است؛ برای همیشه روشن بودن پلن Starter لازم است. |

---

## ساختار پیشنهادی ریپو برای Render

```
your-repo/
└── asha/          ← اگر کل ریپو فقط asha است، rootDir = .
    ├── render.yaml
    ├── requirements.txt
    ├── src/
    └── ...
```

اگر `asha` داخل ساب‌فولدر است، در `render.yaml` مقدار `rootDir: asha` بگذارید و Build/Start را از همان مسیر اجرا کنید.
