from vosk import Model, KaldiRecognizer
import pyaudio
import queue
import threading
import json
import os

MODEL_PATH = "vosk-model-small-en-us-0.15"

class VoiceListener(threading.Thread):
    def __init__(self, keywords=("start","jump","pause","resume","reset","exit")):
        super().__init__(daemon=True)
        self.keywords = keywords
        self.cmd_queue = queue.Queue()
        self.running = True

        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                "Vosk model not found. Download from https://alphacephei.com/vosk/models"
            )

        self.model = Model(MODEL_PATH)
        self.rec = KaldiRecognizer(self.model,16000,json.dumps(self.keywords))

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=4096
        )

    def run(self):
        print("🎤 Voice listener started")

        while self.running:
            data = self.stream.read(4096,exception_on_overflow=False)

            if self.rec.AcceptWaveform(data):
                result = json.loads(self.rec.Result())
                text = result.get("text","")

                for word in self.keywords:
                    if word in text:
                        print("Command:",word)
                        self.cmd_queue.put(word)

            else:
                partial = json.loads(self.rec.PartialResult())
                part = partial.get("partial","")

                if "jump" in part:
                    self.cmd_queue.put("jump")
                    self.rec.Reset()

    def get_command(self):
        try:
            return self.cmd_queue.get_nowait()
        except queue.Empty:
            return None

    def stop(self):
        self.running = False
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


if __name__ == "__main__":
    listener = VoiceListener()
    listener.start()

    try:
        while True:
            cmd = listener.get_command()
            if cmd:
                print("➡ Command:",cmd)

    except KeyboardInterrupt:
        listener.stop()