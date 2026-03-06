import time
import random
import subprocess
from datetime import datetime

HOURS_BETWEEN_VIDEOS = 2
MIN_HOURS = 1.5
MAX_HOURS = 3.0

def run_scheduler():
    print("⏰ BRAINROT SCHEDULER STARTED")
    run_count = 0
    while True:
        run_count += 1
        print(f"\n🎬 RUN #{run_count} — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        try:
            result = subprocess.run(["python", "main.py"], timeout=600)
            if result.returncode == 0:
                print("✅ Short created!")
            else:
                print("⚠️ Check errors above")
        except subprocess.TimeoutExpired:
            print("⏰ Timed out — skipping")
        except Exception as e:
            print(f"❌ Error: {e}")

        wait_hours = random.uniform(MIN_HOURS, MAX_HOURS)
        wait_seconds = wait_hours * 3600
        next_run = datetime.fromtimestamp(time.time() + wait_seconds)
        print(f"\n😴 Next Short at {next_run.strftime('%H:%M:%S')}")
        time.sleep(wait_seconds)

if __name__ == "__main__":
    run_scheduler()
