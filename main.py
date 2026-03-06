import anthropic
import os
import random
import subprocess
from pathlib import Path
from datetime import datetime

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
OUTPUT_DIR = Path("outputs")
BACKGROUND_DIR = Path("backgrounds")
OUTPUT_DIR.mkdir(exist_ok=True)
BACKGROUND_DIR.mkdir(exist_ok=True)

BRAINROT_TOPICS = [
    "why sigma males don't use microwaves",
    "the Ohio conspiracy nobody talks about",
    "why skibidi toilet is actually a documentary",
    "the dark lore behind among us",
    "why rizz is an ancient superpower",
    "gyatt theory explained by scientists",
    "why NPC mode is actually enlightenment",
    "the truth about fanum tax economics",
    "why the alpha male fears the mewing technique",
    "how to unlock your inner grimace shake",
    "why touching grass reverses brain rot",
    "the forbidden lore of the rizzler",
    "why gen alpha will solve climate change with vibes",
    "the matrix but everyone is an NPC",
    "why your cat is actually sigma",
]

def generate_script(topic):
    print(f"🧠 Generating script for: {topic}")
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[{"role": "user", "content": f"""You are a viral YouTube Shorts brainrot content creator. 
Write a 30-45 second script about: "{topic}"
Rules:
- Start with an insane hook in the first 3 words (e.g. "BRO WAIT WHAT", "NO WAY THIS")
- Use gen z brainrot language: sigma, rizz, NPC, Ohio, skibidi, W, L, no cap, fr fr, gyatt, mewing
- Make wild unhinged claims with fake confidence
- End with "follow for part 2" or "comment if you knew this"
- Under 120 words total
- Write ONLY the spoken words, no stage directions"""}]
    )
    script = message.content[0].text.strip()
    print(f"✅ Script done ({len(script.split())} words)")
    return script

def generate_voiceover(script, output_path):
    print("🎤 Generating voiceover...")
    voices = ["en-US-GuyNeural", "en-US-ChristopherNeural", "en-GB-RyanNeural"]
    voice = random.choice(voices)
    mp3_path = str(output_path).replace(".mp4", ".mp3")
    result = subprocess.run(
        ["edge-tts", f"--voice={voice}", f"--text={script}", f"--write-media={mp3_path}"],
        capture_output=True, text=True, timeout=60
    )
    return mp3_path if result.returncode == 0 else None

def get_audio_duration(audio_path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)],
        capture_output=True, text=True
    )
    try:
        return float(result.stdout.strip())
    except:
        return 30.0

def generate_srt(script, duration, srt_path):
    words = script.split()
    chunk_size = max(3, len(words) // 10)
    chunks = [words[i:i+chunk_size] for i in range(0, len(words), chunk_size)]
    time_per_chunk = duration / len(chunks)
    with open(srt_path, "w") as f:
        for i, chunk in enumerate(chunks):
            start = i * time_per_chunk
            end = start + time_per_chunk
            h, m, s, ms = int(start//3600), int((start%3600)//60), int(start%60), int((start%1)*1000)
            he, me, se, mse = int(end//3600), int((end%3600)//60), int(end%60), int((end%1)*1000)
            f.write(f"{i+1}\n{h:02d}:{m:02d}:{s:02d},{ms:03d} --> {he:02d}:{me:02d}:{se:02d},{mse:03d}\n")
            f.write(" ".join(chunk).upper() + "\n\n")

def get_background_video():
    videos = list(BACKGROUND_DIR.glob("*.mp4")) + list(BACKGROUND_DIR.glob("*.mov"))
    return random.choice(videos) if videos else None

def compose_video(background, audio, srt, output, duration):
    print("🎬 Composing video...")
    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", str(background),
        "-i", str(audio),
        "-filter_complex",
        f"[0:v]scale=1920:1080,crop=607:1080:(iw-607)/2:0,scale=1080:1920,subtitles={srt}:force_style='FontSize=22,FontName=Impact,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=3,Outline=3,Alignment=2,MarginV=80'[v]",
        "-map", "[v]", "-map", "1:a",
        "-t", str(duration),
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        str(output)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return result.returncode == 0

def create_short():
    if not ANTHROPIC_API_KEY:
        print("❌ Add ANTHROPIC_API_KEY to Replit Secrets!")
        return

    topic = random.choice(BRAINROT_TOPICS)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = OUTPUT_DIR / f"{timestamp}_{topic[:20].replace(' ', '_')}"

    print(f"\n🚀 Topic: {topic}")
    script = generate_script(topic)
    print(f"\n📝 Script:\n{script}\n")

    audio = generate_voiceover(script, base)
    if not audio:
        print("❌ Voiceover failed — is edge-tts installed?")
        return

    duration = get_audio_duration(audio)
    srt = str(base) + ".srt"
    generate_srt(script, duration, srt)

    bg = get_background_video()
    if not bg:
        print("⚠️ No background videos found — add .mp4 files to backgrounds/ folder")
        print("✅ Script + audio saved to outputs/ anyway!")
        return

    output = str(base) + ".mp4"
    if compose_video(bg, audio, srt, output, duration):
        print(f"🎉 SHORT READY: {output}")
    else:
        print("❌ Video composition failed")

if __name__ == "__main__":
    print("🤖 BRAINROT BOT ACTIVATED\n")
    create_short()
