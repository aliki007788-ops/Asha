# مستندات Plugin System (ASHA Plugins)

**نسخه مستند:** 0.1.0  
**تاریخ:** 2026-09-14

## هدف

امکان افزودن ایجنت یا ماژول ثالث بدون تغییر در هسته آشا.

## کلاس پایه

`src/plugins/base.py` → `BasePlugin`

متدهای اصلی:
- `initialize(context)`
- `execute(payload)`
- `shutdown()`

## بارگذاری

`src/plugins/loader.py` → `PluginLoader`

## وضعیت

اسکلت اولیه در فاز ۱ آماده است. قابلیت کامل در فاز ۷ تکمیل می‌شود.
