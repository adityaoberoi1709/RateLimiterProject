from collections import defaultdict,deque
import time
import threading
class RateLimiterSlidingWindow:
    def __init__(self,max_request = 5,window_time= 2):
        self.request = max_request
        self.window = window_time
        self.users = defaultdict(deque)
        self.lock = threading.Lock()
    def allowrequest(self,user_id):
        current_time = time.time()
        with self.lock:
            request_times = self.users[user_id]
            while request_times and request_times[0]<=current_time-self.window:
                request_times.popleft()
            if len(request_times)<self.request:
                request_times.append(current_time)
                return True
            return False
    def getrequestinwindow(self,user_id):
        current_time = time.time()
        with self.lock:
            request_times = self.users[user_id]
            # Remove old timestamps first
            while request_times and request_times[0] <= current_time - self.window:
                request_times.popleft()
            return len(request_times)
    def set_limits(self, max_request: int, window_time: float):
        with self.lock:
            self.request = max_request
            self.window = window_time
