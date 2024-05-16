import time
def exponential_backoff(function, session, max_retries = 5):
    delay = 1
    for attempt in range(max_retries):
        try:
            function(session)
            print(delay)
        except Exception as e:
            time.sleep(delay)
            delay *= 2  # Double the delay for the next attempt
            print(e)

    raise Exception("Maximum retry attempts reached")