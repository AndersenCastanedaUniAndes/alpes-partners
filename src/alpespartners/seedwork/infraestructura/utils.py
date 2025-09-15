import time
import os

def time_millis():
    return int(time.time() * 1000)

def broker_host():
    return os.getenv('BROKER_HOST', default="localhost")

def service_name():
    return os.getenv('SERVICE_NAME', default="alpespartners")

