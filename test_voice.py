from vosk import Model, KaldiRecognizer
import pyaudio
import queue
import threading
import json
import os

# Path to your Vosk model
MODEL_PATH = "vosk-model-small-en-us-0.15"

class VoiceListener(threading.Thread):
    def __init__(self, keywords=("start", "jump", "reset", "exit")):
        super().__init__(daemon=True)
        self.keywords = keywords
        self.cmd_queue = queue.Queue()
        self.running = True

        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Vosk model not found at: {MODEL_PATH}\n"
                "Download from https://alphacephei.com/vosk/models and extract it here."
            )

        # Load model
        self.model = Model(MODEL_PATH)

        # Limit recognizer to only our keywords for better accuracy
        self.rec = KaldiRecognizer(self.model, 16000, json.dumps(self.keywords))

        # PyAudio setup
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=4096
        )

    def run(self):
        print("🎙️ Vosk: Listening for voice commands...")
        while self.running:
            data = self.stream.read(4096, exception_on_overflow=False)
            if self.rec.AcceptWaveform(data):
                # Full result
                res = json.loads(self.rec.Result())
                text = res.get("text", "")
                for word in self.keywords:
                    if word in text:
                        print(f"✅ Vosk: Detected '{word}'")
                        self.cmd_queue.put(word)
            else:
                # Partial results (fast response) only for jump
                partial = json.loads(self.rec.PartialResult())
                parttext = partial.get("partial", "")
                if "jump" in parttext:
                    print(f"🎧 (Partial) 'jump' detected")
                    self.cmd_queue.put("jump")
                    self.rec.Reset()  # Prevent multiple triggers

    def get_command(self):
        """Return next command from queue, or None if empty."""
        try:
            return self.cmd_queue.get_nowait()
        except queue.Empty:
            return None

    def stop(self):
        """Stop listener safely."""
        self.running = False
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        print("🛑 Vosk: Listener stopped.")

# --- Test Usage ---
if __name__ == "__main__":
    listener = VoiceListener()
    listener.start()
    try:
        while True:
            cmd = listener.get_command()
            if cmd:
                print(f"➡️ Command received: {cmd}")
    except KeyboardInterrupt:
        listener.stop()


