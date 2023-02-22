import threading
import time
from datetime import datetime, timedelta

from app.models.computer import Computer

class ServerManager:
    stop_flag = None
    threashold_seconds = None
    app_instance = None

    def __init__(self, app_instance) -> None:
        self.device_status_thread = threading.Thread(target=self.device_status)
        ServerManager.stop_flag = False
        ServerManager.threashold_seconds = 60
        ServerManager.app_instance = app_instance

    def start(self):
        self.device_status_thread.start()

    def stop(self):
        ServerManager.stop_flag = True

    @staticmethod
    def device_status():
        while True:
            with ServerManager.app_instance.app_context():
                threashold = datetime.now() - timedelta(seconds=ServerManager.threashold_seconds)
                computers = Computer.query.filter(Computer.updated < threashold).all()

                for computer in computers:
                    computer.status = False
                    computer.save()
                print(len(computers))

            time.sleep(ServerManager.threashold_seconds)

            if ServerManager.stop_flag:
                return