# CLI-Agent (Enhanced) — چندحالته با File Builder و حفاظت

این نسخه توسعه‌یافته‌ی CLI-Agent است که قابلیت‌های زیر را اضافه می‌کند:
- File Builder: مدل می‌تواند بطور خودکار فایل‌ ایجاد کند (پایتون، شل‌اسکریپت، و غیره).
- Auto-confirmation: تشخیص دستورات خطرناک و درخواست تأیید از کاربر (یا auto-confirm).
- Sandbox mode: اجرای شبیه‌سازی شده دستورات تا زمانی که SANDBOX خاموش شود.
- محفوظ‌سازی لاگ مراحل در `logs/agent_log.json`.

## نصب
1. کلون و ورود:
```bash
git clone <repo>
cd repo
```

2. نصب نیازمندی‌ها:
```bash
pip install -r requirements.txt
```

3. پیکربندی:
- متغیر محیطی `OPENAI_API_KEY` را ست کنید.
- برای تست امن، `CLI_AGENT_SANDBOX=1` پیش‌فرض است (دستورها اجرا نمی‌شوند).
- برای فعال کردن تایید خودکار: `CLI_AGENT_AUTO_CONFIRM=1`.

مثال:
```bash
export OPENAI_API_KEY="sk-..."
export CLI_AGENT_SANDBOX=1
export CLI_AGENT_AUTO_CONFIRM=0
python main.py
```

## مثال
ورودی:
```
به من یک فایل پایتون بساز که یک سرور ساده Flask راه‌اندازی کنه و یک route /health داشته باشه.
```

مدل ممکن است یک پاسخ JSON بدهد:
```json
{
  "action": "write_file",
  "path": "workspace/app.py",
  "content": "from flask import Flask\napp=Flask(__name__)\n@app.route('/health')\ndef h(): return 'ok'\nif __name__=='__main__': app.run()"
}
```

سپس agent فایل را ایجاد می‌کند و لاگ می‌نویسد.

## نکات امنیتی
- **هرگز** این Agent را با دسترسی روت روی سرور تولیدی اجرا نکنید.
- در حالت sandbox تست کنید و ابتدا خروجی لاگ را بررسی کنید.
- File writes محدود به مسیر مشخص‌شده در `PROJECT_ROOT` هستند.

## لایسنس
MIT
