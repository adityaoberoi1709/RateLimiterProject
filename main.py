from fastapi import FastAPI, Request,Query,Header, HTTPException
from BasicRateLimiter import RateLimiterSlidingWindow
import time
app = FastAPI(title="FastAPI Rate Limiter Demo")
limiter = RateLimiterSlidingWindow()
def getuserid(request: Request):
    return request.client.host
@app.get("/")
def home():
    return {"message": "FastAPI Rate Limiter is running"}
@app.get("/data")
def get_data(request: Request):
    try:
        user_id = getuserid(request)

        if not limiter.allowrequest(user_id):
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later."
            )
        remaining = limiter.request - limiter.getrequestinwindow(user_id)

        return {
          "message": "Request allowed ✅",
          "user": user_id,
          "timestamp": time.time(),
          "requests_made_in_window": limiter.getrequestinwindow(user_id),
          "requests_remaining": remaining
          }
    except HTTPException:
        raise
    except Exception as e:
        # Log error to console
        print("Error in /data:", e)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
@app.get("/config")
def update_limits(
    max_request: int = Query(None, description="Max requests per window"),
    window_time: float = Query(None, description="Window size in seconds")
):
    if max_request is None:
        max_request = limiter.request
    if window_time is None:
        window_time = limiter.window

    limiter.set_limits(max_request=max_request, window_time=window_time)
    return {
        "message": "Rate limiter configuration updated ✅",
        "new_max_request": limiter.request,
        "new_window_time": limiter.window
    }
