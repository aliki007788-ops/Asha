# آشا (ASHA) — Product Brief برای هوش مصنوعی / همکار فنی
**نسخه محصول:** 2.0.0  
**تاریخ:** 2026-09-15  
**هدف این سند:** توضیح کامل آنچه ساخته شده، بدون نیاز به خواندن کل سورس‌کد.

---

## ۱. آشا چیست؟

آشا یک **کارخانه ایجنت چندپلتفرمی** است برای کسب‌وکارهای ایرانی.

- ۱۵ ایجنت مستقل برای فروش، پشتیبانی، محتوا، فاکتور، جذب نیرو و ...
- اتصال به پیام‌رسان‌ها و پلتفرم‌های ایرانی (و Bridge برای تلگرام/اینستاگرام)
- API تجاری با FastAPI
- قابل استقرار روی Render / Docker / VPS
- معماری Plugin-based: ایجنت جدید بدون تغییر هسته اضافه می‌شود

**هدف تجاری:** افزایش فروش کسب‌وکار بدون استخدام نیروی جدید.

---

## ۲. معماری (۵ لایه)

```
لایه ۱ — هسته (Core)
  Orchestrator | Registry | Config | State | Event Bus

لایه ۲ — ۱۵ ایجنت مشتری‌رو
  sales_closer, outbound, sequencer, proposal, upsell, support,
  seo_content, video_script, content_calendar, cart_recovery,
  invoice, recruitment, market_research, personal_assistant, agency

لایه ۳ — ماژول‌های پشتیبان
  memory, analytics, pricing, auth, queue, reporting,
  error_recovery, model_updater, compliance

لایه ۴ — Adapter Layer
  eitaa, bale, rubika, divar, torob, emalls, telegram_bridge, instagram_bridge

لایه ۵ — پلتفرم‌های بیرونی
  ایتا | بله | روبیکا | دیوار | ترب | ایمالز | تلگرام | اینستاگرام
```

**قوانین طراحی:**
1. استقلال ایجنت‌ها (خرابی یکی بقیه را نمی‌خواباند)
2. لایه اتصال واحد (Adapter مشترک)
3. بدون patch روی patch — تحویل فایل کامل
4. Single Source of Truth
5. Plugin-based

---

## ۳. تکنولوژی

| مورد | مقدار |
|------|--------|
| زبان | Python 3.11+ / 3.12 |
| API | FastAPI + Uvicorn |
| تست | pytest + pytest-asyncio (۴۸ تست PASS) |
| HTTP کلاینت | httpx |
| استقرار | Docker, render.yaml, GitHub Actions keep-alive |
| State / Event Bus فعلی | In-memory (برای یک instance کافی) |
| اختیاری بعدی | PostgreSQL, Redis Streams |

---

## ۴. ایجنت‌ها (۱۵ عدد — همه با منطق واقعی execute)

| agent_id | نقش |
|----------|-----|
| sales_closer | تحلیل قصد خرید، اعتراض‌ها، پیام بستن فروش |
| outbound | پیام اولیه به لید |
| sequencer | توالی چندمرحله‌ای nurture |
| proposal | پیشنهاد قیمت / پروپوزال |
| upsell | پیشنهاد مکمل بعد از خرید |
| support | FAQ و پشتیبانی |
| seo_content | محتوای SEO |
| video_script | اسکریپت ویدیو |
| content_calendar | تقویم محتوا |
| cart_recovery | بازیابی سبد رهاشده |
| invoice | صدور فاکتور |
| recruitment | غربالگری رزومه |
| market_research | بینش بازار |
| personal_assistant | یادآوری و کارهای روزمره |
| agency | هماهنگی کمپین چندایجنتی |

ورودی همه: `payload: dict` — خروجی: `dict` با `status`, `agent_id` و فیلدهای اختصاصی.

---

## ۵. Adapterها — وضعیت واقعی

| پلتفرم | API واقعی | حالت |
|--------|-----------|------|
| **ایتا** | `eitaayar.ir/api/{token}/sendMessage` و app API | live اگر `EITAA_API_KEY` باشد، وگرنه mock |
| **بله** | `tapi.bale.ai/bot{token}/...` (شبیه تلگرام) | live اگر `BALE_API_KEY` باشد |
| **روبیکا** | `botapi.rubika.ir/v3/{token}/...` | live اگر `RUBIKA_API_KEY` باشد |
| دیوار / ترب / ایمالز | اسکلت + mock | نیاز به API شریک/فروشنده |
| تلگرام / اینستاگرام | Bridge اسکلت | mock تا توکن |

همه Adapter اینترفیس مشترک دارند:
- `send_message(chat_id, text) -> bool`
- `receive_messages() -> list[Message]`
- `send_file(chat_id, file_path) -> bool`
- `health_check() -> dict`

---

## ۶. API تجاری (FastAPI)

| متد | مسیر | توضیح |
|-----|------|--------|
| GET | `/health` | سلامت سیستم (بدون کلید) |
| GET | `/agents` | فهرست ایجنت‌ها |
| POST | `/tasks` | `{agent_id, payload}` → task_id |
| GET | `/tasks/{id}` | وضعیت و نتیجه وظیفه |
| GET | `/adapters/{platform}/health` | سلامت Adapter |
| POST | `/adapters/{platform}/send` | ارسال مستقیم پیام |
| POST | `/pipeline/message` | پیام → ایجنت → ارسال پاسخ روی پلتفرم |
| POST | `/webhooks/bale` | وب‌هوک ورودی بله |
| POST | `/webhooks/rubika` و `/webhooks/rubika/receiveUpdate` | وب‌هوک روبیکا |
| POST | `/webhooks/eitaa` | وب‌هوک ایتا |

**امنیت:** اگر `ASHA_API_KEY` ست شود، درخواست‌های تجاری نیاز به هدر `X-API-Key` دارند.  
وب‌هوک‌ها بدون API key هستند (پلتفرم صدا می‌زند).

---

## ۷. جریان کاری نمونه

1. مشتری در بله پیام می‌دهد.
2. بله به `POST /webhooks/bale` می‌زند.
3. Adapter پیام را به `Message` استاندارد تبدیل می‌کند.
4. Orchestrator وظیفه را به مثلاً `support` یا `sales_closer` می‌دهد.
5. ایجنت پاسخ می‌سازد.
6. Adapter پاسخ را با API زنده به همان chat_id می‌فرستد.

یا از بیرون:
`POST /pipeline/message` با `{platform, chat_id, text, agent_id}`.

---

## ۸. ساختار پوشه پروژه

```
asha/
├── PRODUCT_BRIEF.md          ← همین سند
├── PROJECT_STATE.md
├── CHANGELOG.md
├── README.md
├── requirements.txt
├── render.yaml
├── Dockerfile
├── .env.example
├── .github/workflows/keep-alive.yml
├── src/
│   ├── core/          # orchestrator, registry, config, state, event_bus
│   ├── agents/        # ۱۵ ایجنت + base
│   ├── adapters/      # ۸ adapter + base
│   ├── support_agents/
│   ├── plugins/
│   ├── api/main.py
│   └── bootstrap.py   # ثبت همه ایجنت‌ها و ساخت سیستم
├── tests/             # unit + integration + contract — ۴۸ PASS
└── docs/
```

---

## ۹. متغیرهای محیطی مهم

```
ASHA_ENV=production
ASHA_API_KEY=...          # امنیت API
EITAA_API_KEY=...         # ایتایار
BALE_API_KEY=...          # بازوی بله
RUBIKA_API_KEY=...        # بات روبیکا
```

---

## ۱۰. آنچه عمداً هنوز کامل نیست (Deferred)

| مورد | دلیل فنی |
|------|----------|
| دیوار / ترب / ایمالز live | API عمومی بات مثل بله ندارند؛ نیاز قرارداد/کلید فروشنده |
| PostgreSQL برای State | نسخه فعلی in-memory؛ برای یک instance Render کافی است |
| Redis Event Bus | برای چند instance / مقیاس بالا |
| LLM داخل ایجنت‌ها | منطق فعلی rule-based است؛ LLM اختیاری برای نسخه بعدی |

---

## ۱۱. ادعای فروش صادقانه

- **قابل فروش به‌عنوان:** موتور فروش/پشتیبانی روی ایتا + بله + روبیکا + API داخلی
- **قابل دمو بدون کلید:** بله (حالت mock)
- **قابل live:** با گذاشتن توکن‌های واقعی پلتفرم روی سرور
- **غیرواقعی است اگر ادعا شود:** همه مارکت‌پلیس‌های ایران بدون هیچ کلید شریکی وصل‌اند

---

## ۱۲. دستورات عملیاتی

```bash
pip install -r requirements.txt
uvicorn src.api.main:app --host 0.0.0.0 --port $PORT
pytest tests/ -q   # باید ۴۸ passed
```

Health: `GET /health` → `status: ok`, `version: 2.0.0`, فهرست agents و adapters.

---

## ۱۳. پیام برای هوش مصنوعی بعدی

> آشا یک سیستم Multi-Agent با هسته Orchestrator/Registry/EventBus است.
> ۱۵ ایجنت فروش/پشتیبانی/محتوا دارد.
> Adapterهای ایتا، بله، روبیکا به API رسمی وصل می‌شوند (با کلید).
> FastAPI مسیر task، pipeline و webhook دارد.
> تست‌ها سبزند. State فعلاً حافظه‌ای است.
> اگر تغییری می‌دهی: فایل کامل بده، patch جزئی نده؛ Adapter Audit و Caller Audit را رعایت کن.

این سند برای ادامه توسعه، فروش، یا توضیح محصول به AI/تیم دیگر کافی است.
