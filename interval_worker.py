import threading, time

class IntervalWorker:
    def __init__(self, log, method, interval_seconds):
        self.log = log
        self.method = method
        self.interval_seconds = interval_seconds
        self.running = False
        self.thread = threading.Thread(daemon=True, target=self._interval_method)

    def _interval_method(self):
        while self.running:
            self.log(f"running method {self.method.__name__}")
            self.method()
            self.log(f"sleeping for {self.interval_seconds}s")
            time.sleep(self.interval_seconds)

    def start(self):
        if self.thread.is_alive():
            self.log('already running')
            return
        else:
            self.log('starting worker thread')
            self.running = True
            self.thread.start()

    def stop(self):
        self.log('stopping worker thread...')
        self.running = False
        self.thread.join
        self.log('joined with worker thread!')