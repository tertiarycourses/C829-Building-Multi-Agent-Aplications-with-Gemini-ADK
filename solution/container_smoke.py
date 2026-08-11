from pathlib import Path
import time
import urllib.error
import urllib.request


deadline = time.monotonic() + 60
last_error: Exception | None = None

while time.monotonic() < deadline:
    try:
        status = urllib.request.urlopen(
            "http://127.0.0.1:8080/docs", timeout=5
        ).status
        if status == 200:
            evidence = Path(__file__).with_name("evidence")
            evidence.mkdir(exist_ok=True)
            (evidence / "http-smoke.txt").write_text(
                f"GET /docs status={status}\n", encoding="utf-8"
            )
            break
    except (TimeoutError, urllib.error.URLError) as exc:
        last_error = exc
    time.sleep(2)
else:
    raise SystemExit(f"Container was not ready within 60 seconds: {last_error}")
