import json
from openai import OpenAI
from .config import OPENAI_API_KEY, MODEL, PROJECT_ROOT
from .executor import run_command
from .logger import log_step
from .utils import confirm_command, is_dangerous, safe_write_file

client = OpenAI(api_key=OPENAI_API_KEY)

PROMPT_INSTRUCTIONS = """You are a Linux CLI Agent with multi-step planning capabilities.
Your job: given a user goal, produce a sequence of actions to reach that goal.
Each assistant response must be a JSON object (no extra text) with one of the following shapes:

1) Run command:
{
  "action": "run",
  "command": "<a single shell command>"
}

2) Write a file (file-builder capability):
{
  "action": "write_file",
  "path": "<relative path under the project root>",
  "content": "<file content, string>"
}

3) Change mode (optional):
{
  "action": "mode",
  "mode": "setup" | "install" | "test" | "fix" | "file"
}

4) Finish:
{
  "action": "finish",
  "note": "optional summary text"
}

Important safety rules:
- Only return one JSON object per response.
- Do not include commands that intentionally escape the project root when writing files.
- If a command might be destructive (e.g., rm -rf), mark it as dangerous and prefer safer alternatives.
"""

def ask_model(goal: str, context: str, last_output: str):
    messages = [
        {"role": "system", "content": PROMPT_INSTRUCTIONS},
        {"role": "user", "content": f"Goal: {goal}"},
        {"role": "assistant", "content": f"Context:\n{context}\nLast Output:\n{last_output}"}
    ]
    resp = client.chat.completions.create(model=MODEL, messages=messages)
    text = resp.choices[0].message.content.strip()
    return text

def parse_action(text: str):
    try:
        return json.loads(text)
    except Exception:
        # If the model doesn't return strict JSON, try to extract the first JSON object in the text
        import re
        m = re.search(r"(\{.*\})", text, re.S)
        if m:
            try:
                return json.loads(m.group(1))
            except Exception:
                pass
    # fallback: treat whole text as a command
    return {"action": "run", "command": text}

def run_agent(goal: str):
    context = ""
    last_output = ""
    step = 1

    while True:
        print(f"\n🧩 مرحله {step}")
        raw = ask_model(goal, context, last_output)
        action = parse_action(raw)
        if not isinstance(action, dict) or 'action' not in action:
            print("⚠️ پاسخ مدل قابل فهم نبود، تلاش می‌کنیم به‌عنوان یک دستور اجرا کنیم.")
            action = {"action": "run", "command": raw}

        act = action.get("action")

        if act == "finish":
            note = action.get("note", "")
            print("✅ فرایند کامل شد:", note)
            log_step({"step": step, "action": "finish", "note": note})
            break

        if act == "mode":
            mode = action.get("mode")
            print(f"🔄 تغییر حالت به: {mode}")
            log_step({"step": step, "action": "mode", "mode": mode})
            context += f"\n[mode change to {mode}]\n"
            step += 1
            continue

        if act == "write_file":
            rel_path = action.get("path")
            content = action.get("content", "")
            try:
                abs_path = safe_write_file(rel_path, content)
                msg = f"WROTE FILE: {abs_path}"
                print(msg)
                log_step({"step": step, "action": "write_file", "path": rel_path, "abs_path": abs_path})
                context += f"\n[write_file {rel_path}]\n"
            except Exception as e:
                print("❌ خطا هنگام نوشتن فایل:", e)
                log_step({"step": step, "action": "write_file_error", "error": str(e)})
                last_output = str(e)
            step += 1
            continue

        if act == "run":
            cmd = action.get("command", "").strip()
            if not cmd:
                print("⚠️ دستور خالی است، رد می‌شود.")
                log_step({"step": step, "action": "run", "command": cmd, "output": "empty command"})
                step += 1
                continue

            # safety check
            if is_dangerous(cmd):
                print("⚠️ دستور خطرناک تشخیص داده شد:", cmd)
                ok = confirm_command(cmd)
                if not ok:
                    print("⛔ اجرای دستور لغو شد.")
                    log_step({"step": step, "action": "run", "command": cmd, "output": "user_cancelled"})
                    last_output = "user_cancelled"
                    step += 1
                    continue

            rc, output = run_command(cmd)
            log_step({"step": step, "action": "run", "command": cmd, "returncode": rc, "output": output})
            context += f"\n[run]{cmd}\noutput:\n{output}\n"
            last_output = output
            step += 1
            continue

        # unknown action
        print("⚠️ عمل‌کرد نامشخص از مدل:", action)
        log_step({"step": step, "action": "unknown", "raw": action})
        step += 1
