# RateLimiterProject
A progressive implementation of a rate limiter, starting simple and advancing to more complex algorithms.

Basic Sliding Window -> 

Unlike fixed window rate limiting, sliding windows prevent edge-case bursts like: 5 requests at 1.99s + 5 requests at 2.01s = ❌ unfair 10 requests. 

A deque (double-ended queue) allows:


popleft() → O(1)

append() → O(1)

This is critical for sliding window cleanup.

Per-User Isolation Using defaultdict.

Thread Safety with threading.Lock, Without locking, concurrent threads could:

Read outdated request counts

Append timestamps simultaneously

Bypass rate limits unintentionally

What the lock guarantees

✔ Atomic cleanup + check + insert

✔ Prevents race conditions

✔ Ensures strict enforcement under concurrency
Provided a Multithreaded Test Simulation
