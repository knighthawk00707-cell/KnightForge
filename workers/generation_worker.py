from PySide6.QtCore import QObject, Signal, Slot
import time

from engine.generator import PasswordGenerator


PREVIEW_LIMIT = 1000


class GenerationWorker(QObject):

    password_generated = Signal(str)
    progress = Signal(int)
    speed = Signal(float)
    elapsed = Signal(float)
    finished = Signal()

    def __init__(self, settings):
        super().__init__()

        self.settings = settings

        self.running = True
        self.paused = False

    @Slot()
    def run(self):

        start_time = time.time()
        count = 0

        try:
            for password in PasswordGenerator.generate(self.settings):

                if not self.running:
                    break

                while self.paused and self.running:
                    time.sleep(0.05)

                if not self.running:
                    break

                self.password_generated.emit(password)

                count += 1

                if count % 100 == 0:

                    elapsed = time.time() - start_time

                    self.progress.emit(count)
                    self.elapsed.emit(elapsed)

                    if elapsed > 0:
                        self.speed.emit(count / elapsed)

                if count >= PREVIEW_LIMIT:
                    break

        finally:
            self.finished.emit()

    def stop(self):
        self.running = False

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False