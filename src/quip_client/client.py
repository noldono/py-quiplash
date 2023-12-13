from gamecomm import client


class GameClient(client.GameClient):

    def __init__(self, url, token=None, on_event=None):
        super().__init__(url, token, on_event)

    def is_event(self, message: dict):
        return "event" in message

    def is_success(self, response: dict):
        return response["status"] == "ok"

    def start(self):
        super().start()

    def stop(self):
        super().stop()
