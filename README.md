# wn-offloading

Simulates offloading scenario of a device to a more powerful edge server.
In edge_client.py the task can be chosen. Either ```task_type = "object_detection"``` or ```"env_stats"```.
Depending on the task, the edge server will simulate processing it and send the result back to the device.
Both will print the result of the task and the processing time. Additionally, the device will print the time for the whole process.

To run the offloading simulation:
```
docker-compose build
docker-compose up
```
