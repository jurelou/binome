import time
import threading
from opulence.engine import celery_app


AGENTS = {}


class Manager:
    def __init__(self):
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    @staticmethod
    def is_listening_for_scans(inspect, worker):
        def is_active(inspect, worker):
            for i in range(5):
                state = inspect.active()
                if state and worker in state:
                    return True
                time.sleep(1)
            return False

        if not is_active(inspect, worker):
            return False
        active_queues = inspect.active_queues()[worker]
        return any(q["name"] == "scan" for q in active_queues)

    def add_worker(self, worker):
        global AGENTS
        print("yo")
        inspect = celery_app.control.inspect([worker])
        if not self.is_listening_for_scans(inspect, worker):
            AGENTS.pop(worker, None)
            return
        conf = inspect.conf()
        if not conf or "collectors" not in conf[worker]:
            AGENTS[worker] = []
        else:
            # print(f"ADDING worker {worker} -> {conf[worker]['collectors']}")
            AGENTS[worker] = conf[worker]["collectors"]

    def offline_event(self, event):
        global AGENTS
        AGENTS.pop(event["hostname"], None)
        print(f"AGENTS: {AGENTS}")

    def online_event(self, event):
        self.add_worker(event["hostname"])
        print(f"AGENTS: {AGENTS}")

    def capture(self, handlers, limit):
        with celery_app.connection() as connection:
            recv = celery_app.events.Receiver(connection, handlers=handlers)
            recv.capture(limit=limit, timeout=None, wakeup=True)
        print("DONE capture")
        print(f"AGENTS: {AGENTS}")

    def run(self):
        print("go")
        self.capture({'worker-heartbeat': self.online_event}, limit=5)
        self.capture({'worker-online': self.online_event, 'worker-offline': self.offline_event}, limit=None)
