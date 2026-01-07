from collections import defaultdict,deque
import time
import threading
from multiprocessing import Process, Manager
class RateLimiterSlidingWindow:
    def __init__(self,max_request = 5,window_time= 2):
        self.request = max_request
        self.window = window_time
        self.users = defaultdict(deque)
        self.lock = threading.Lock()
    def allowrequest(self,user_id: str):
        current_time = time.time()
        with self.lock:
            request_times = self.users[user_id]
            while request_times and request_times[0]<=current_time-self.window:
                request_times.popleft()
            if len(request_times)<self.request:
                request_times.append(current_time)
                return True
            return False
if __name__=="__main__":
    limiter = RateLimiterSlidingWindow()
    user = 'Adi'
    allowed_count = 0
    denied_count = 0
    
    def make_request(request_id):
        global allowed_count,denied_count
        allowed = limiter.allowrequest(user)
        if allowed:
            allowed_count+=1 
            print(f"Thread {request_id}: ALLOWED")
        else:
            denied_count+=1
            print(f"Thread {request_id}: DENIED")
    threads = []
    for i in range(10):
        t = threading.Thread(target = make_request,args = (i,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print(f"\nFinal Result:{allowed_count} allowed, {denied_count} denied\n")