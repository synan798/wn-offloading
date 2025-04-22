import socket
import json
import random
import time
import os

HOST = 'edge'
PORT = 9898

def generate_env_data():
    return [random.gauss(22, 2) for _ in range(50)]

def log_result_to_file(result):
    os.makedirs("results", exist_ok=True)
    with open("results/device_result.json", "w") as f:
        json.dump(result, f, indent=2)

task_type = "object_detection" # "env_stats" 

if task_type == "env_stats":
    payload = {
        "task": task_type,
        "data": generate_env_data()
    }
else:
    payload = {"task": task_type}

print(f"[Device] Sending task '{task_type}' to edge node...")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    time.sleep(2)
    s.connect((HOST, PORT))

    start = time.time()
    s.sendall(json.dumps(payload).encode())
    response = s.recv(4096)
    end = time.time()

    result = json.loads(response.decode())
    result["round_trip_time_sec"] = round(end - start, 3)

    print(f"[Device] Received result: {result}")
    log_result_to_file(result)
