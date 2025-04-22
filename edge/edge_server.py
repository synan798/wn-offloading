import socket
import json
import statistics
import time
import random
import os

HOST = '0.0.0.0'
PORT = 9898

def simulate_env_stats(data):
    mean_val = statistics.mean(data)
    stddev_val = statistics.stdev(data)
    anomaly = stddev_val > 3.0
    time.sleep(1.5)
    return {
        "mean": round(mean_val, 2),
        "stddev": round(stddev_val, 2),
        "anomaly": anomaly
    }

def simulate_object_detection():
    objects = ["car", "pedestrian", "bike", "none"]
    detected = random.choices(objects, k=3)
    time.sleep(2.0)
    return {"detected_objects": detected}

def log_result_to_file(result):
    os.makedirs("results", exist_ok=True)
    with open("results/edge_result.json", "w") as f:
        json.dump(result, f, indent=2)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("[Edge] Ready to accept offloaded tasks...")

    conn, addr = s.accept()
    with conn:
        print(f"[Edge] Connection from {addr}")
        raw_data = conn.recv(4096)
        task = json.loads(raw_data.decode())

        task_type = task.get("task")
        start = time.time()

        if task_type == "env_stats":
            data = task["data"]
            result_data = simulate_env_stats(data)
        elif task_type == "object_detection":
            result_data = simulate_object_detection()
        else:
            result_data = {"error": "Unsupported task"}
        
        end = time.time()
        result_data["processing_time_sec"] = round(end - start, 3)

        print(f"[Edge] Completed '{task_type}' task:", result_data)
        log_result_to_file(result_data)
        conn.sendall(json.dumps(result_data).encode())
