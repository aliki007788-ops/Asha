# مستندات Adapterها (ASHA Adapters)

**نسخه مستند:** 0.1.0  
**تاریخ:** 2026-09-14

## اینترفیس مشترک

همه Adapterها باید `BaseAdapter` را پیاده‌سازی کنند:

- `send_message(chat_id, text) -> bool`
- `receive_messages() -> list[Message]`
- `send_file(chat_id, file_path) -> bool`
- `health_check() -> dict`

## Adapterهای برنامه‌ریزی‌شده

| پلتفرم       | فایل                    | وضعیت      |
|--------------|-------------------------|------------|
| ایتا         | eitaa_adapter.py        | فاز ۲      |
| بله          | bale_adapter.py         | فاز ۲      |
| روبیکا       | rubika_adapter.py       | فاز ۲+     |
| دیوار        | divar_adapter.py        | فاز ۵      |
| ترب          | torob_adapter.py        | فاز ۵      |
| ایمالز       | emalls_adapter.py       | فاز ۵      |
| تلگرام       | telegram_bridge.py      | فاز ۶      |
| اینستاگرام   | instagram_bridge.py     | فاز ۶      |

## افزودن Adapter جدید

1. ارث‌بری از `BaseAdapter`
2. پیاده‌سازی متدهای abstract
3. ثبت در Registry (در صورت نیاز)
4. نوشتن Contract Test
5. به‌روزرسانی این مستند
