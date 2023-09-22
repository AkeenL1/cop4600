'''
import queue

def move_hashmap_to_priority_queue(hashmap):
    # Create a priority queue
    priority_queue = queue.PriorityQueue()

    # Iterate through the hashmap and add items to the priority queue
    for key, value in hashmap.items():
        # The priority key is the arrivalTime value
        arrival_time = value['arrivalTime']
        priority_queue.put((arrival_time, key, value))

    return priority_queue

# Example usage:
hashmap = {
    'item1': {'arrivalTime': 5, 'data': 'Some data 1'},
    'item2': {'arrivalTime': 3, 'data': 'Some data 2'},
    'item3': {'arrivalTime': 7, 'data': 'Some data 3'},
}

priority_queue = move_hashmap_to_priority_queue(hashmap)

# Now you can pop items from the priority queue in order of arrivalTime
while not priority_queue.empty():
    arrival_time, key, value = priority_queue.get()
    print(f'Item: {key}, Arrival Time: {arrival_time}, Data: {value["data"]}')

--------------------------------------------------------------------

import queue

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = None
        self.end_time = None

    def __lt__(self, other):
        # Priority comparison based on arrival_time
        return self.arrival_time < other.arrival_time

def move_hashmap_to_priority_queue(hashmap):
    # Create a priority queue
    priority_queue = queue.PriorityQueue()

    processes = []

    # Iterate through the hashmap and create Process objects
    for key, value in hashmap.items():
        processes.append(Process(key, value['arrivalTime'], value['burstTime']))

    # Sort processes by arrival time
    processes.sort(key=lambda x: x.arrival_time)

    # Initialize metrics
    turnaround_times = {}
    waiting_times = {}
    response_times = {}

    current_time = 0

    for process in processes:
        # Calculate waiting time
        waiting_time = max(0, current_time - process.arrival_time)
        waiting_times[process.name] = waiting_time

        # Calculate response time (same as waiting time for FIFO)
        response_times[process.name] = waiting_time

        # Calculate turnaround time
        turnaround_time = process.burst_time + waiting_time
        turnaround_times[process.name] = turnaround_time

        # Update current time
        current_time += process.burst_time

        # Add process to the priority queue
        priority_queue.put(process)

    return priority_queue, turnaround_times, waiting_times, response_times

# Example usage:
hashmap = {
    'P1': {'arrivalTime': 0, 'burstTime': 5},
    'P2': {'arrivalTime': 2, 'burstTime': 3},
    'P3': {'arrivalTime': 4, 'burstTime': 1},
}

priority_queue, turnaround_times, waiting_times, response_times = move_hashmap_to_priority_queue(hashmap)

# Print metrics for each process
for process_name in hashmap.keys():
    print(f"Process {process_name}:")
    print(f"Turnaround Time: {turnaround_times[process_name]}")
    print(f"Waiting Time: {waiting_times[process_name]}")
    print(f"Response Time: {response_times[process_name]}")
    print()

---------------------

import queue

class Process:
    def __init__(self, name, burst):
        self.name = name
        self.burst = burst

    def __lt__(self, other):
        return self.burst < other.burst

def process_priority_queue(priority_queue):
    while not priority_queue.empty():
        # Get the process with the highest priority (lowest burst time)
        current_process = priority_queue.get()

        # Decrement the burst attribute
        current_process.burst -= 1

        # Print the current queue object
        print("Current Queue:", list(priority_queue.queue))

        # Check if the burst has reached 0, and remove the process if so
        if current_process.burst == 0:
            print(f"Process {current_process.name} finished")
        else:
            # Re-add the process to the priority queue with updated burst time
            priority_queue.put(current_process)

# Example usage:
if __name__ == "__main__":
    # Create a priority queue of processes
    priority_queue = queue.PriorityQueue()
    processes = [
        Process("P1", 5),
        Process("P2", 3),
        Process("P3", 4),
    ]

    # Add processes to the priority queue
    for process in processes:
        priority_queue.put(process)

    # Call the function to process the priority queue
    process_priority_queue(priority_queue)
    ------------------------

import queue

class Process:
    def __init__(self, name, burst):
        self.name = name
        self.burst = burst

    def __lt__(self, other):
        return self.burst < other.burst

def process_priority_queue(priority_queue):
    while not priority_queue.empty():
        # Get the process with the highest priority (lowest burst time)
        current_process = priority_queue.get()

        # Decrement the burst attribute
        current_process.burst -= 1

        # Print the name of the current process
        print(f"Current Process: {current_process.name}")

        # Check if the burst has reached 0, and remove the process if so
        if current_process.burst == 0:
            print(f"Process {current_process.name} finished")
        else:
            # Re-add the process to the priority queue with updated burst time
            priority_queue.put(current_process)

# Example usage:
if __name__ == "__main__":
    # Create a priority queue of processes
    priority_queue = queue.PriorityQueue()
    processes = [
        Process("P1", 5),
        Process("P2", 3),
        Process("P3", 4),
    ]

    # Add processes to the priority queue
    for process in processes:
        priority_queue.put(process)

    # Call the function to process the priority queue
    process_priority_queue(priority_queue)

-------------------


import queue

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = None
        self.end_time = None

def fifo_scheduler(processes):
    current_time = 0
    ready_queue = queue.Queue()
    completed_processes = []
    total_processes = len(processes)
    response_times = {}
    turnaround_times = {}
    waiting_times = {}

    print(f"{total_processes} processes")
    print("Using First-In, First-Out (FIFO)")

    while completed_processes != total_processes:
        # Check for arriving processes
        for process in processes:
            if process.arrival_time == current_time:
                print(f"Time {current_time:4} : {process.name} arrived")
                ready_queue.put(process)

        if not ready_queue.empty():
            running_process = ready_queue.get()
            running_process.start_time = current_time
            print(f"Time {current_time:4} : {running_process.name} selected (burst {running_process.burst_time:4})")
            current_time += running_process.burst_time
            running_process.end_time = current_time
            completed_processes.append(running_process)
            print(f"Time {current_time:4} : {running_process.name} finished")
        else:
            print(f"Time {current_time:4} : Idle")
            current_time += 1

    # Calculate metrics
    for process in completed_processes:
        turnaround_time = process.end_time - process.arrival_time
        response_time = process.start_time - process.arrival_time
        waiting_time = turnaround_time - process.burst_time
        response_times[process.name] = response_time
        turnaround_times[process.name] = turnaround_time
        waiting_times[process.name] = waiting_time

    print(f"Finished at time {completed_processes[-1].end_time}\n")

    for process in completed_processes:
        print(f"{process.name} wait {waiting_times[process.name]:4} turnaround {turnaround_times[process.name]:4} response {response_times[process.name]:4}")

if __name__ == "__main__":
    # Define the processes (name, arrival time, burst time)
    processes = [
        Process("A", 0, 5),
        Process("B", 1, 4),
        Process("C", 4, 2),
    ]

    fifo_scheduler(processes)


---------------------


import queue

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = None
        self.end_time = None

def fifo_scheduler(processes):
    current_time = 0
    ready_queue = queue.Queue()
    completed_processes = []
    total_processes = len(processes)
    response_times = {}
    turnaround_times = {}
    waiting_times = {}

    print(f"{total_processes} processes")
    print("Using First-In, First-Out (FIFO)")

    while len(completed_processes) != total_processes:
        # Check for arriving processes
        for process in processes:
            if process.arrival_time == current_time:
                print(f"Time {current_time:4} : {process.name} arrived")
                ready_queue.put(process)

        if not ready_queue.empty():
            running_process = ready_queue.get()
            running_process.start_time = current_time
            print(f"Time {current_time:4} : {running_process.name} selected (burst {running_process.burst_time:4})")
            current_time += running_process.burst_time
            running_process.end_time = current_time
            completed_processes.append(running_process)
            print(f"Time {current_time:4} : {running_process.name} finished")
        else:
            print(f"Time {current_time:4} : Idle")
            current_time += 1

    # Calculate metrics
    for process in completed_processes:
        turnaround_time = process.end_time - process.arrival_time
        response_time = process.start_time - process.arrival_time
        waiting_time = turnaround_time - process.burst_time
        response_times[process.name] = response_time
        turnaround_times[process.name] = turnaround_time
        waiting_times[process.name] = waiting_time

    print(f"Finished at time {completed_processes[-1].end_time}\n")

    for process in completed_processes:
        print(f"{process.name} wait {waiting_times[process.name]:4} turnaround {turnaround_times[process.name]:4} response {response_times[process.name]:4}")

if __name__ == "__main__":
    # Define the processes (name, arrival time, burst time)
    processes = [
        Process("A", 0, 5),
        Process("B", 1, 4),
        Process("C", 4, 2),
    ]

    fifo_scheduler(processes)

-------------

import queue

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = None
        self.end_time = None

def fifo_scheduler(processes, runfor):
    current_time = 0
    ready_queue = queue.Queue()
    completed_processes = []
    total_processes = len(processes)
    response_times = {}
    turnaround_times = {}
    waiting_times = {}
    iteration = 0  # Counter for the number of iterations

    print(f"{total_processes} processes")
    print("Using First-In, First-Out (FIFO)")

    while len(completed_processes) != total_processes and iteration < runfor:
        # Check for arriving processes
        for process in processes:
            if process.arrival_time == current_time:
                print(f"Time {current_time:4} : {process.name} arrived")
                ready_queue.put(process)

        if not ready_queue.empty():
            running_process = ready_queue.get()
            running_process.start_time = current_time
            print(f"Time {current_time:4} : {running_process.name} selected (burst {running_process.burst_time:4})")
            current_time += running_process.burst_time
            running_process.end_time = current_time
            completed_processes.append(running_process)
            print(f"Time {current_time:4} : {running_process.name} finished")
        else:
            print(f"Time {current_time:4} : Idle")
            current_time += 1

        iteration += 1

    # Calculate metrics
    for process in completed_processes:
        turnaround_time = process.end_time - process.arrival_time
        response_time = process.start_time - process.arrival_time
        waiting_time = turnaround_time - process.burst_time
        response_times[process.name] = response_time
        turnaround_times[process.name] = turnaround_time
        waiting_times[process.name] = waiting_time

    print(f"Finished at time {completed_processes[-1].end_time}\n")

    for process in completed_processes:
        print(f"{process.name} wait {waiting_times[process.name]:4} turnaround {turnaround_times[process.name]:4} response {response_times[process.name]:4}")

if __name__ == "__main__":
    # Define the processes (name, arrival time, burst time)
    processes = [
        Process("A", 0, 5),
        Process("B", 1, 4),
        Process("C", 4, 2),
    ]

    runfor = 10  # Set the number of iterations to run for
    fifo_scheduler(processes, runfor)

    
import queue

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = None
        self.end_time = None

def fifo_scheduler(processes, runfor):
    current_time = 0
    ready_queue = queue.Queue()
    completed_processes = []
    total_processes = len(processes)
    response_times = {}
    turnaround_times = {}
    waiting_times = {}
    iteration = 0  # Counter for the number of iterations

    print(f"{total_processes} processes")
    print("Using First-In, First-Out (FIFO)")

    while len(completed_processes) != total_processes and iteration < runfor:
        # Check for arriving processes
        for process in processes:
            if process.arrival_time == current_time:
                print(f"Time {current_time:4} : {process.name} arrived")
                ready_queue.put(process)

        if not ready_queue.empty():
            running_process = ready_queue.get()
            running_process.start_time = current_time
            print(f"Time {current_time:4} : {running_process.name} selected (burst {running_process.burst_time:4})")
            current_time += running_process.burst_time
            running_process.end_time = current_time
            completed_processes.append(running_process)
            print(f"Time {current_time:4} : {running_process.name} finished")
        else:
            print(f"Time {current_time:4} : Idle")
            current_time += 1

        iteration += 1

    # Calculate metrics
    for process in completed_processes:
        turnaround_time = process.end_time - process.arrival_time
        response_time = process.start_time - process.arrival_time
        waiting_time = turnaround_time - process.burst_time
        response_times[process.name] = response_time
        turnaround_times[process.name] = turnaround_time
        waiting_times[process.name] = waiting_time

    print(f"Finished at time {runfor}\n")  # Use runfor in the "Finished at time" line

    for process in completed_processes:
        print(f"{process.name} wait {waiting_times[process.name]:4} turnaround {turnaround_times[process.name]:4} response {response_times[process.name]:4}")

if __name__ == "__main__":
    # Define the processes (name, arrival time, burst time)
    processes = [
        Process("A", 0, 5),
        Process("B", 1, 4),
        Process("C", 4, 2),
    ]

    runfor = 10  # Set the number of iterations to run for
    fifo_scheduler(processes, runfor)

    
import queue

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = None
        self.end_time = None

def fifo_scheduler(processes, runfor):
    current_time = 0
    ready_queue = queue.Queue()
    completed_processes = []
    total_processes = len(processes)
    response_times = {}
    turnaround_times = {}
    waiting_times = {}
    iteration = 0  # Counter for the number of iterations

    print(f"{total_processes} processes")
    print("Using First-In, First-Out (FIFO)")

    while len(completed_processes) != total_processes and iteration < runfor:
        # Check for arriving processes before each iteration
        for process in processes:
            if process.arrival_time == current_time:
                print(f"Time {current_time:4} : {process.name} arrived")
                ready_queue.put(process)

        if not ready_queue.empty():
            running_process = ready_queue.get()
            running_process.start_time = current_time
            print(f"Time {current_time:4} : {running_process.name} selected (burst {running_process.burst_time:4})")
            current_time += 1
            running_process.burst_time -= 1

            if running_process.burst_time == 0:
                running_process.end_time = current_time
                completed_processes.append(running_process)
                print(f"Time {current_time:4} : {running_process.name} finished")
        else:
            print(f"Time {current_time:4} : Idle")
            current_time += 1

        iteration += 1

    # Calculate metrics
    for process in completed_processes:
        turnaround_time = process.end_time - process.arrival_time
        response_time = process.start_time - process.arrival_time
        waiting_time = turnaround_time - process.burst_time
        response_times[process.name] = response_time
        turnaround_times[process.name] = turnaround_time
        waiting_times[process.name] = waiting_time

    print(f"Finished at time {runfor}\n")  # Use runfor in the "Finished at time" line

    for process in completed_processes:
        print(f"{process.name} wait {waiting_times[process.name]:4} turnaround {turnaround_times[process.name]:4} response {response_times[process.name]:4}")

if __name__ == "__main__":
    # Define the processes (name, arrival time, burst time)
    processes = [
        Process("A", 0, 5),
        Process("B", 1, 4),
        Process("C", 4, 2),
    ]

    runfor = 10  # Set the number of iterations to run for
    fifo_scheduler(processes, runfor)

import queue

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = None
        self.end_time = None

def fifo_scheduler(processes, runfor):
    current_time = 0
    ready_queue = queue.Queue()
    completed_processes = []
    total_processes = len(processes)
    response_times = {}
    turnaround_times = {}
    waiting_times = {}
    iteration = 0  # Counter for the number of iterations

    print(f"{total_processes} processes")
    print("Using First-In, First-Out (FIFO)")

    while len(completed_processes) != total_processes and iteration < runfor:
        # Check for arriving processes before each iteration
        for process in processes:
            if process.arrival_time == current_time:
                print(f"Time {current_time:4} : {process.name} arrived")
                ready_queue.put(process)

        if not ready_queue.empty():
            running_process = ready_queue.get()
            running_process.start_time = current_time
            print(f"Time {current_time:4} : {running_process.name} selected (burst {running_process.burst_time:4})")
            current_time += 1
            running_process.burst_time -= 1

            if running_process.burst_time == 0:
                running_process.end_time = current_time
                completed_processes.append(running_process)
                print(f"Time {current_time:4} : {running_process.name} finished")
            else:
                ready_queue.put(running_process)
        else:
            print(f"Time {current_time:4} : Idle")
            current_time += 1

        iteration += 1

    # Calculate metrics
    for process in completed_processes:
        turnaround_time = process.end_time - process.arrival_time
        response_time = process.start_time - process.arrival_time
        waiting_time = turnaround_time - process.burst_time
        response_times[process.name] = response_time
        turnaround_times[process.name] = turnaround_time
        waiting_times[process.name] = waiting_time

    print(f"Finished at time {runfor}\n")  # Use runfor in the "Finished at time" line

    for process in completed_processes:
        print(f"{process.name} wait {waiting_times[process.name]:4} turnaround {turnaround_times[process.name]:4} response {response_times[process.name]:4}")

if __name__ == "__main__":
    # Define the processes (name, arrival time, burst time)
    processes = [
        Process("A", 0, 5),
        Process("B", 1, 4),
        Process("C", 4, 2),
    ]

    runfor = 10  # Set the number of iterations to run for
    fifo_scheduler(processes, runfor)
-----------------------------
-----------------------------
    START HERE->


import queue

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = None
        self.end_time = None

    def __lt__(self, other):
        # Priority comparison based on arrival_time
        return self.arrival_time < other.arrival_time

def fifo_scheduler(processes, runfor):
    current_time = 0
    ready_queue = queue.PriorityQueue()
    completed_processes = []
    total_processes = len(processes)
    response_times = {}
    turnaround_times = {}
    waiting_times = {}
    iteration = 0  # Counter for the number of iterations

    print(f"{total_processes} processes")
    print("Using First-In, First-Out (FIFO) based on arrival_time")

    while len(completed_processes) != total_processes and iteration < runfor:
        # Check for arriving processes before each iteration
        for process in processes:
            if process.arrival_time == current_time:
                print(f"Time {current_time:4} : {process.name} arrived")
                ready_queue.put(process)

        if not ready_queue.empty():
            running_process = ready_queue.get()
            running_process.start_time = current_time
            print(f"Time {current_time:4} : {running_process.name} selected (burst {running_process.burst_time:4})")
            current_time += 1
            running_process.burst_time -= 1

            if running_process.burst_time == 0:
                running_process.end_time = current_time
                completed_processes.append(running_process)
                print(f"Time {current_time:4} : {running_process.name} finished")
            else:
                ready_queue.put(running_process)
        else:
            print(f"Time {current_time:4} : Idle")
            current_time += 1

        iteration += 1

    # Calculate metrics
    for process in completed_processes:
        turnaround_time = process.end_time - process.arrival_time
        response_time = process.start_time - process.arrival_time
        waiting_time = turnaround_time - process.burst_time
        response_times[process.name] = response_time
        turnaround_times[process.name] = turnaround_time
        waiting_times[process.name] = waiting_time

    print(f"Finished at time {runfor}\n")  # Use runfor in the "Finished at time" line

    for process in completed_processes:
        print(f"{process.name} wait {waiting_times[process.name]:4} turnaround {turnaround_times[process.name]:4} response {response_times[process.name]:4}")

if __name__ == "__main__":
    # Define the processes (name, arrival time, burst time)
    processes = [
        Process("A", 0, 5),
        Process("B", 1, 4),
        Process("C", 4, 2),
    ]

    runfor = 10  # Set the number of iterations to run for
    fifo_scheduler(processes, runfor)

import queue

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = None
        self.end_time = None

    def __lt__(self, other):
        # Priority comparison based on arrival_time
        return self.arrival_time < other.arrival_time

def fifo_scheduler(processes, runfor):
    current_time = 0
    ready_queue = queue.PriorityQueue()
    completed_processes = []
    total_processes = len(processes)
    response_times = {}
    turnaround_times = {}
    waiting_times = {}
    iteration = 0  # Counter for the number of iterations

    print(f"{total_processes} processes")
    print("Using First-In, First-Out (FIFO) based on arrival_time")

    while len(completed_processes) != total_processes and iteration < runfor:
        # Check for arriving processes before each iteration
        for process in processes:
            if process.arrival_time == current_time:
                ready_queue.put(process)

        if not ready_queue.empty():
            running_process = ready_queue.get()
            running_process.start_time = current_time
            current_time += 1
            running_process.burst_time -= 1

            if running_process.burst_time == 0:
                running_process.end_time = current_time
                completed_processes.append(running_process)
                print(f"Time {current_time:4} : {running_process.name} finished")
            else:
                ready_queue.put(running_process)
        else:
            current_time += 1

        iteration += 1

    # Calculate metrics and print after the simulation finishes
    for process in completed_processes:
        turnaround_time = process.end_time - process.arrival_time
        response_time = process.start_time - process.arrival_time
        waiting_time = turnaround_time - process.burst_time
        response_times[process.name] = response_time
        turnaround_times[process.name] = turnaround_time
        waiting_times[process.name] = waiting_time

    print(f"Finished at time {runfor}\n")  # Use runfor in the "Finished at time" line

    for process in completed_processes:
        print(f"{process.name} wait {waiting_times[process.name]:4} turnaround {turnaround_times[process.name]:4} response {response_times[process.name]:4}")

if __name__ == "__main__":
    # Define the processes (name, arrival time, burst time)
    processes = [
        Process("A", 0, 5),
        Process("B", 1, 4),
        Process("C", 4, 2),
    ]

    runfor = 10  # Set the number of iterations to run for
    fifo_scheduler(processes, runfor)

import queue

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = None
        self.end_time = None

    def __lt__(self, other):
        # Priority comparison based on arrival_time
        return self.arrival_time < other.arrival_time

def fifo_scheduler(processes, runfor):
    current_time = 0
    ready_queue = queue.PriorityQueue()
    completed_processes = []
    total_processes = len(processes)
    response_times = {}
    turnaround_times = {}
    waiting_times = {}
    iteration = 0  # Counter for the number of iterations

    print(f"{total_processes} processes")
    print("Using First-In, First-Out (FIFO) based on arrival_time")

    while len(completed_processes) != total_processes and iteration < runfor:
        # Check for arriving processes before each iteration
        for process in processes:
            if process.arrival_time == current_time:
                print(f"Time {current_time:4} : {process.name} arrived")

        if not ready_queue.empty():
            running_process = ready_queue.get()
            running_process.start_time = current_time
            current_time += 1
            running_process.burst_time -= 1

            if running_process.burst_time == 0:
                running_process.end_time = current_time
                completed_processes.append(running_process)
                print(f"Time {current_time:4} : {running_process.name} finished")
            else:
                ready_queue.put(running_process)
        else:
            print(f"Time {current_time:4} : Idle")
            current_time += 1

        # Check for beginning time (after updating current_time)
        for process in processes:
            if process.start_time == current_time - 1:
                print(f"Time {current_time-1:4} : {process.name} selected (burst {process.burst_time:4})")

        iteration += 1

    # Calculate metrics and print after the simulation finishes
    for process in completed_processes:
        turnaround_time = process.end_time - process.arrival_time
        response_time = process.start_time - process.arrival_time
        waiting_time = turnaround_time - process.burst_time
        response_times[process.name] = response_time
        turnaround_times[process.name] = turnaround_time
        waiting_times[process.name] = waiting_time

    print(f"Finished at time {runfor}\n")  # Use runfor in the "Finished at time" line

    for process in completed_processes:
        print(f"{process.name} wait {waiting_times[process.name]:4} turnaround {turnaround_times[process.name]:4} response {response_times[process.name]:4}")

if __name__ == "__main__":
    # Define the processes (name, arrival time, burst time)
    processes = [
        Process("A", 0, 5),
        Process("B", 1, 4),
        Process("C", 4, 2),
    ]

    runfor = 10  # Set the number of iterations to run for
    fifo_scheduler(processes, runfor)

import queue

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = None
        self.end_time = None

def fifo_scheduler(processes, runfor):
    current_time = 0
    ready_queue = queue.Queue()
    completed_processes = []
    total_processes = len(processes)
    response_times = {}
    turnaround_times = {}
    waiting_times = {}
    iteration = 0  # Counter for the number of iterations

    print(f"{total_processes} processes")
    print("Using First-In, First-Out (FIFO)")

    while len(completed_processes) != total_processes and iteration < runfor:
        # Check for arriving processes
        for process in processes:
            if process.arrival_time == current_time:
                print(f"Time {current_time:4} : {process.name} arrived")
                ready_queue.put(process)

        if not ready_queue.empty():
            running_process = ready_queue.get()
            running_process.start_time = current_time
            print(f"Time {current_time:4} : {running_process.name} selected (burst {running_process.burst_time:4})")
            current_time += running_process.burst_time
            running_process.end_time = current_time
            completed_processes.append(running_process)
            print(f"Time {current_time:4} : {running_process.name} finished")
        else:
            print(f"Time {current_time:4} : Idle")
            current_time += 1

        iteration += 1

    # Calculate metrics
    for process in completed_processes:
        turnaround_time = process.end_time - process.arrival_time
        response_time = process.start_time - process.arrival_time
        waiting_time = turnaround_time - process.burst_time
        response_times[process.name] = response_time
        turnaround_times[process.name] = turnaround_time
        waiting_times[process.name] = waiting_time

    print(f"Finished at time {completed_processes[-1].end_time}\n")

    for process in completed_processes:
        print(f"{process.name} wait {waiting_times[process.name]:4} turnaround {turnaround_times[process.name]:4} response {response_times[process.name]:4}")

if __name__ == "__main__":
    # Define the processes (name, arrival time, burst time)
    processes = [
        Process("A", 0, 5),
        Process("B", 1, 4),
        Process("C", 4, 2),
    ]

    runfor = 10  # Set the number of iterations to run for
    fifo_scheduler(processes, runfor)

import queue

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = None
        self.end_time = None

def fifo_scheduler(processes, runfor):
    current_time = 0
    ready_queue = queue.Queue()
    completed_processes = []
    total_processes = len(processes)
    response_times = {}
    turnaround_times = {}
    waiting_times = {}
    iteration = 0  # Counter for the number of iterations

    queued_messages = []  # Queue for user messages

    print(f"{total_processes} processes")
    print("Using First-In, First-Out (FIFO)")

    while len(completed_processes) != total_processes and iteration < runfor:
        # Check for arriving processes
        for process in processes:
            if process.arrival_time == current_time:
                print(f"Time {current_time:4} : {process.name} arrived")
                ready_queue.put(process)

        # Check for queued messages
        while queued_messages:
            message_time, message = queued_messages[0]
            if message_time <= current_time:
                print(f"Time {current_time:4} : {message}")
                queued_messages.pop(0)
            else:
                break

        if not ready_queue.empty():
            running_process = ready_queue.get()
            running_process.start_time = current_time
            print(f"Time {current_time:4} : {running_process.name} selected (burst {running_process.burst_time:4})")
            current_time += running_process.burst_time
            running_process.end_time = current_time
            completed_processes.append(running_process)
            print(f"Time {current_time:4} : {running_process.name} finished")
        else:
            print(f"Time {current_time:4} : Idle")
            current_time += 1

        iteration += 1

    # Calculate metrics
    for process in completed_processes:
        turnaround_time = process.end_time - process.arrival_time
        response_time = process.start_time - process.arrival_time
        waiting_time = turnaround_time - process.burst_time
        response_times[process.name] = response_time
        turnaround_times[process.name] = turnaround_time
        waiting_times[process.name] = waiting_time

    print(f"Finished at time {completed_processes[-1].end_time}\n")

    for process in completed_processes:
        print(f"{process.name} wait {waiting_times[process.name]:4} turnaround {turnaround_times[process.name]:4} response {response_times[process.name]:4}")

if __name__ == "__main__":
    # Define the processes (name, arrival time, burst time)
    processes = [
        Process("A", 0, 5),
        Process("B", 1, 4),
        Process("C", 4, 2),
    ]

    runfor = 10  # Set the number of iterations to run for

    # Define queued messages with timestamps
    queued_messages = [
        (2, "User message at time 2"),
        (4, "User message at time 4"),
    ]

    for message_time, message in queued_messages:
        print(f"Queued message at time {message_time}: {message}")

    fifo_scheduler(processes, runfor)

import queue

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = None
        self.end_time = None

def fifo_scheduler(processes, runfor):
    current_time = 0
    ready_queue = queue.PriorityQueue()
    completed_processes = []
    total_processes = len(processes)
    response_times = {}
    turnaround_times = {}
    waiting_times = []
    iteration = 0  # Counter for the number of iterations

    queued_messages = []  # Queue for user messages

    print(f"{total_processes} processes")
    print("Using First-In, First-Out (FIFO)")

    while len(completed_processes) != total_processes and current_time < runfor:
        # Check for arriving processes
        for process in processes:
            if process.arrival_time <= current_time and process not in completed_processes:
                ready_queue.put(process)

        # Check for queued messages
        while queued_messages:
            message_time, message = queued_messages[0]
            if message_time <= current_time:
                print(f"Time {current_time:4} : {message}")
                queued_messages.pop(0)
            else:
                break

        if not ready_queue.empty():
            running_process = ready_queue.get()
            running_process.start_time = current_time
            print(f"Time {current_time:4} : {running_process.name} selected (burst {running_process.burst_time:4})")

            if running_process.burst_time > 1:
                # Enqueue the process with reduced burst time
                ready_queue.put(Process(running_process.name, running_process.arrival_time, running_process.burst_time - 1))
            else:
                # Process finished
                current_time += 1
                running_process.end_time = current_time
                completed_processes.append(running_process)
                print(f"Time {current_time:4} : {running_process.name} finished")
        else:
            print(f"Time {current_time:4} : Idle")
            current_time += 1

        iteration += 1

    # Calculate metrics
    for process in completed_processes:
        turnaround_time = process.end_time - process.arrival_time
        response_time = process.start_time - process.arrival_time
        waiting_time = turnaround_time - process.burst_time
        response_times[process.name] = response_time
        turnaround_times[process.name] = turnaround_time
        waiting_times.append(waiting_time)

    print(f"Finished at time {current_time}\n")

    for i, process in enumerate(completed_processes):
        print(f"{process.name} wait {waiting_times[i]:4} turnaround {turnaround_times[process.name]:4} response {response_times[process.name]:4}")

if __name__ == "__main__":
    # Define the processes (name, arrival time, burst time)
    processes = [
        Process("A", 0, 5),
        Process("B", 1, 4),
        Process("C", 4, 2),
    ]

    runfor = 10  # Set the number of iterations to run for

    # Define queued messages with timestamps
    queued_messages = [
        (2, "User message at time 2"),
        (4, "User message at time 4"),
    ]

    for message_time, message in queued_messages:
        print(f"Queued message at time {message_time}: {message}")

    fifo_scheduler(processes, runfor)

import queue

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = None
        self.end_time = None

def fifo_scheduler(processes, runfor):
    current_time = 0
    ready_queue = queue.Queue()
    completed_processes = []
    total_processes = len(processes)
    response_times = {}
    turnaround_times = {}
    waiting_times = {}
    iteration = 0  # Counter for the number of iterations

    queued_messages = []  # Queue for user messages

    print(f"{total_processes} processes")
    print("Using First-In, First-Out (FIFO)")

    while len(completed_processes) != total_processes and iteration < runfor:
        # Check for arriving processes
        for process in processes:
            if process.arrival_time == current_time:
                print(f"Time {current_time:4} : {process.name} arrived")
                ready_queue.put(process)

        # Check for queued messages
        while queued_messages:
            message_time, message = queued_messages[0]
            if message_time <= current_time:
                print(f"Time {current_time:4} : {message}")
                queued_messages.pop(0)
            else:
                break

        if not ready_queue.empty():
            running_process = ready_queue.get()
            running_process.start_time = current_time
            print(f"Time {current_time:4} : {running_process.name} selected (burst {running_process.burst_time:4})")
            current_time += running_process.burst_time
            running_process.end_time = current_time
            completed_processes.append(running_process)
            print(f"Time {current_time:4} : {running_process.name} finished")
        else:
            print(f"Time {current_time:4} : Idle")
            current_time += 1

        iteration += 1

    # Calculate metrics
    for process in completed_processes:
        turnaround_time = process.end_time - process.arrival_time
        response_time = process.start_time - process.arrival_time
        waiting_time = turnaround_time - process.burst_time
        response_times[process.name] = response_time
        turnaround_times[process.name] = turnaround_time
        waiting_times[process.name] = waiting_time

    print(f"Finished at time {completed_processes[-1].end_time}\n")

    for process in completed_processes:
        print(f"{process.name} wait {waiting_times[process.name]:4} turnaround {turnaround_times[process.name]:4} response {response_times[process.name]:4}")

if __name__ == "__main__":
    # Define the processes (name, arrival time, burst time)
    processes = [
        Process("A", 0, 5),
        Process("B", 1, 4),
        Process("C", 4, 2),
    ]

    runfor = 10  # Set the number of iterations to run for

    # Define queued messages with timestamps
    queued_messages = [
        (2, "User message at time 2"),
        (4, "User message at time 4"),
    ]

    for message_time, message in queued_messages:
        print(f"Queued message at time {message_time}: {message}")

    fifo_scheduler(processes, runfor)

import queue

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = None
        self.end_time = None

def fifo_scheduler(processes, runfor):
    current_time = 0
    ready_queue = queue.Queue()
    completed_processes = []
    total_processes = len(processes)
    response_times = {}
    turnaround_times = {}
    waiting_times = {}
    iteration = 0  # Counter for the number of iterations

    print(f"{total_processes} processes")
    print("Using First-In, First-Out (FIFO)")

    while len(completed_processes) != total_processes and iteration < runfor:
        # Check for arriving processes before each iteration
        for process in processes:
            if process.arrival_time == current_time:
                print(f"Time {current_time:4} : {process.name} arrived")
                ready_queue.put(process)

        if not ready_queue.empty():
            running_process = ready_queue.get()
            running_process.start_time = current_time
            print(f"Time {current_time:4} : {running_process.name} selected (burst {running_process.burst_time:4})")
            current_time += running_process.burst_time
            running_process.end_time = current_time
            completed_processes.append(running_process)
            print(f"Time {current_time:4} : {running_process.name} finished")
        else:
            print(f"Time {current_time:4} : Idle")
            current_time += 1

        iteration += 1

    # Calculate metrics
    for process in completed_processes:
        turnaround_time = process.end_time - process.arrival_time
        response_time = process.start_time - process.arrival_time
        waiting_time = turnaround_time - process.burst_time
        response_times[process.name] = response_time
        turnaround_times[process.name] = turnaround_time
        waiting_times[process.name] = waiting_time

    print(f"Finished at time {completed_processes[-1].end_time}\n")

    for process in completed_processes:
        print(f"{process.name} wait {waiting_times[process.name]:4} turnaround {turnaround_times[process.name]:4} response {response_times[process.name]:4}")

if __name__ == "__main__":
    # Define the processes (name, arrival time, burst time)
    processes = [
        Process("A", 0, 5),
        Process("B", 1, 4),
        Process("C", 4, 2),
    ]

    runfor = 10  # Set the number of iterations to run for
    fifo_scheduler(processes, runfor)

import queue

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = None
        self.end_time = None

    def __lt__(self, other):
        # Priority comparison based on arrival_time
        return self.arrival_time < other.arrival_time

def fifo_scheduler(processes, runfor):
    current_time = 0
    ready_queue = queue.PriorityQueue()
    completed_processes = []
    total_processes = len(processes)
    response_times = {}
    turnaround_times = {}
    waiting_times = {}
    iteration = 0  # Counter for the number of iterations

    print(f"{total_processes} processes")
    print("Using First-In, First-Out (FIFO) based on arrival_time")

    while len(completed_processes) != total_processes and iteration < runfor:
        # Check for arriving processes before each iteration
        for process in processes:
            if process.arrival_time == current_time and process.start_time is None:
                print(f"Time {current_time:4} : {process.name} arrived")
                ready_queue.put(process)

        if not ready_queue.empty():
            running_process = ready_queue.get()
            running_process.start_time = current_time
            print(f"Time {current_time:4} : {running_process.name} selected (burst {running_process.burst_time:4})")
            current_time += 1
            running_process.burst_time -= 1

            if running_process.burst_time == 0:
                running_process.end_time = current_time
                completed_processes.append(running_process)
                print(f"Time {current_time:4} : {running_process.name} finished")
            else:
                ready_queue.put(running_process)
        else:
            print(f"Time {current_time:4} : Idle")
            current_time += 1

        iteration += 1

    # Calculate metrics
    for process in completed_processes:
        turnaround_time = process.end_time - process.arrival_time
        response_time = process.start_time - process.arrival_time
        waiting_time = turnaround_time - process.burst_time
        response_times[process.name] = response_time
        turnaround_times[process.name] = turnaround_time
        waiting_times[process.name] = waiting_time

    print(f"Finished at time {runfor}\n")  # Use runfor in the "Finished at time" line

    for process in completed_processes:
        print(f"{process.name} wait {waiting_times[process.name]:4} turnaround {turnaround_times[process.name]:4} response {response_times[process.name]:4}")

if __name__ == "__main__":
    # Define the processes (name, arrival time, burst time)
    processes = [
        Process("A", 0, 5),
        Process("B", 1, 4),
        Process("C", 4, 2),
    ]

    runfor = 10  # Set the number of iterations to run for
    fifo_scheduler(processes, runfor)
================================                        HERE just need IDLE
import queue

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = None
        self.end_time = None

    def __lt__(self, other):
        # Priority comparison based on arrival_time
        return self.arrival_time < other.arrival_time

def fifo_scheduler(processes, runfor):
    current_time = 0
    ready_queue = queue.PriorityQueue()
    completed_processes = []
    total_processes = len(processes)
    response_times = {}
    turnaround_times = {}
    waiting_times = {}
    iteration = 0  # Counter for the number of iterations

    print(f"{total_processes} processes")
    print("Using First-In, First-Out (FIFO) based on arrival_time")

    selected_processes = set()  # Set to keep track of selected processes

    while len(completed_processes) != total_processes and iteration < runfor:
        # Check for arriving processes before each iteration
        for process in processes:
            if process.arrival_time == current_time and process.start_time is None:
                print(f"Time {current_time:4} : {process.name} arrived")
                ready_queue.put(process)

        if not ready_queue.empty():
            running_process = ready_queue.get()
            if running_process.name not in selected_processes:
                running_process.start_time = current_time
                print(f"Time {current_time:4} : {running_process.name} selected (burst {running_process.burst_time:4})")
                selected_processes.add(running_process.name)
            current_time += 1
            running_process.burst_time -= 1

            if running_process.burst_time == 0:
                running_process.end_time = current_time
                completed_processes.append(running_process)
                selected_processes.remove(running_process.name)  # Remove from selected set
                print(f"Time {current_time:4} : {running_process.name} finished")
            else:
                ready_queue.put(running_process)
        else:
            print(f"Time {current_time:4} : Idle")
            current_time += 1

        iteration += 1

    # Calculate metrics
    for process in completed_processes:
        turnaround_time = process.end_time - process.arrival_time
        response_time = process.start_time - process.arrival_time
        waiting_time = turnaround_time - process.burst_time
        response_times[process.name] = response_time
        turnaround_times[process.name] = turnaround_time
        waiting_times[process.name] = waiting_time

    print(f"Finished at time {runfor}\n")  # Use runfor in the "Finished at time" line

    for process in completed_processes:
        print(f"{process.name} wait {waiting_times[process.name]:4} turnaround {turnaround_times[process.name]:4} response {response_times[process.name]:4}")

if __name__ == "__main__":
    # Define the processes (name, arrival time, burst time)
    processes = [
        Process("A", 0, 5),
        Process("B", 1, 4),
        Process("C", 4, 2),
    ]

    runfor = 15  # Set the number of iterations to run for
    fifo_scheduler(processes, runfor)

import queue

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = None
        self.end_time = None

    def __lt__(self, other):
        # Priority comparison based on arrival_time
        return self.arrival_time < other.arrival_time

def fifo_scheduler(processes, runfor):
    current_time = 0
    ready_queue = queue.PriorityQueue()
    completed_processes = []
    total_processes = len(processes)
    response_times = {}
    turnaround_times = {}
    waiting_times = {}
    iteration = 0  # Counter for the number of iterations

    print(f"{total_processes} processes")
    print("Using First-In, First-Out (FIFO) based on arrival_time")

    selected_processes = set()  # Set to keep track of selected processes

    while len(completed_processes) != total_processes and iteration < runfor:
        # Check for arriving processes before each iteration
        for process in processes:
            if process.arrival_time == current_time and process.start_time is None:
                print(f"Time {current_time:4} : {process.name} arrived")
                ready_queue.put(process)

        if not ready_queue.empty():
            running_process = ready_queue.get()
            if running_process.name not in selected_processes:
                running_process.start_time = current_time
                print(f"Time {current_time:4} : {running_process.name} selected (burst {running_process.burst_time:4})")
                selected_processes.add(running_process.name)
            current_time += 1
            running_process.burst_time -= 1

            if running_process.burst_time == 0:
                running_process.end_time = current_time
                completed_processes.append(running_process)
                selected_processes.remove(running_process.name)  # Remove from selected set
                print(f"Time {current_time:4} : {running_process.name} finished")
        else:
            if not selected_processes:
                print(f"Time {current_time:4} : Idle")
            current_time += 1

        iteration += 1

    # Calculate metrics
    for process in completed_processes:
        turnaround_time = process.end_time - process.arrival_time
        response_time = process.start_time - process.arrival_time
        waiting_time = turnaround_time - process.burst_time
        response_times[process.name] = response_time
        turnaround_times[process.name] = turnaround_time
        waiting_times[process.name] = waiting_time

    print(f"Finished at time {runfor}\n")  # Use runfor in the "Finished at time" line

    for process in completed_processes:
        print(f"{process.name} wait {waiting_times[process.name]:4} turnaround {turnaround_times[process.name]:4} response {response_times[process.name]:4}")

if __name__ == "__main__":
    # Define the processes (name, arrival time, burst time)
    processes = [
        Process("A", 0, 5),
        Process("B", 1, 4),
        Process("C", 4, 2),
    ]

    runfor = 10  # Set the number of iterations to run for
    fifo_scheduler(processes, runfor)

import queue

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = None
        self.end_time = None

    def __lt__(self, other):
        # Priority comparison based on arrival_time
        return self.arrival_time < other.arrival_time

def fifo_scheduler(processes, runfor):
    current_time = 0
    ready_queue = queue.PriorityQueue()
    completed_processes = []
    total_processes = len(processes)
    response_times = {}
    turnaround_times = {}
    waiting_times = {}
    iteration = 0  # Counter for the number of iterations

    print(f"{total_processes} processes")
    print("Using First-In, First-Out (FIFO) based on arrival_time")

    selected_processes = set()  # Set to keep track of selected processes
    is_idle = True  # Flag to check if the system is idle

    while len(completed_processes) != total_processes and iteration < runfor:
        # Check for arriving processes before each iteration
        for process in processes:
            if process.arrival_time == current_time and process.start_time is None:
                print(f"Time {current_time:4} : {process.name} arrived")
                ready_queue.put(process)

        if not ready_queue.empty():
            running_process = ready_queue.get()
            if running_process.name not in selected_processes:
                running_process.start_time = current_time
                print(f"Time {current_time:4} : {running_process.name} selected (burst {running_process.burst_time:4})")
                selected_processes.add(running_process.name)
                is_idle = False
            current_time += 1
            running_process.burst_time -= 1

            if running_process.burst_time == 0:
                running_process.end_time = current_time
                completed_processes.append(running_process)
                selected_processes.remove(running_process.name)  # Remove from selected set
                print(f"Time {current_time:4} : {running_process.name} finished")
        elif not is_idle:
            print(f"Time {current_time:4} : Idle")
            is_idle = True
            current_time += 1
        else:
            current_time += 1

        iteration += 1

    # Calculate metrics
    for process in completed_processes:
        turnaround_time = process.end_time - process.arrival_time
        response_time = process.start_time - process.arrival_time
        waiting_time = turnaround_time - process.burst_time
        response_times[process.name] = response_time
        turnaround_times[process.name] = turnaround_time
        waiting_times[process.name] = waiting_time

    print(f"Finished at time {runfor}\n")  # Use runfor in the "Finished at time" line

    for process in completed_processes:
        print(f"{process.name} wait {waiting_times[process.name]:4} turnaround {turnaround_times[process.name]:4} response {response_times[process.name]:4}")

if __name__ == "__main__":
    # Define the processes (name, arrival time, burst time)
    processes = [
        Process("A", 0, 5),
        Process("B", 1, 4),
        Process("C", 4, 2),
    ]

    runfor = 10  # Set the number of iterations to run for
    fifo_scheduler(processes, runfor)
=========================               HERE, just need Idle

import queue

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = None
        self.end_time = None

    def __lt__(self, other):
        # Priority comparison based on arrival_time
        return self.arrival_time < other.arrival_time

def fifo_scheduler(processes, runfor):
    current_time = 0
    ready_queue = queue.PriorityQueue()
    completed_processes = []
    total_processes = len(processes)
    response_times = {}
    turnaround_times = {}
    waiting_times = {}
    iteration = 0  # Counter for the number of iterations

    print(f"{total_processes} processes")
    print("Using First-In, First-Out (FIFO) based on arrival_time")

    selected_processes = set()  # Set to keep track of selected processes

    while len(completed_processes) != total_processes and iteration < runfor:
        # Check for arriving processes before each iteration
        for process in processes:
            if process.arrival_time == current_time and process.start_time is None:
                print(f"Time {current_time:4} : {process.name} arrived")
                ready_queue.put(process)

        if not ready_queue.empty():
            running_process = ready_queue.get()
            if running_process.name not in selected_processes:
                running_process.start_time = current_time
                print(f"Time {current_time:4} : {running_process.name} selected (burst {running_process.burst_time:4})")
                selected_processes.add(running_process.name)
            current_time += 1
            running_process.burst_time -= 1

            if running_process.burst_time == 0:
                running_process.end_time = current_time
                completed_processes.append(running_process)
                selected_processes.remove(running_process.name)  # Remove from selected set
                print(f"Time {current_time:4} : {running_process.name} finished")
            else:
                ready_queue.put(running_process)
        else:
            #if len(completed_processes) < total_processes:
            print(f"Time {current_time:4} : Idle")
            current_time += 1

        iteration += 1

    # Calculate metrics
    for process in completed_processes:
        turnaround_time = process.end_time - process.arrival_time
        response_time = process.start_time - process.arrival_time
        waiting_time = turnaround_time - process.burst_time
        response_times[process.name] = response_time
        turnaround_times[process.name] = turnaround_time
        waiting_times[process.name] = waiting_time

    print(f"Finished at time {runfor}\n")  # Use runfor in the "Finished at time" line

    for process in completed_processes:
        print(f"{process.name} wait {waiting_times[process.name]:4} turnaround {turnaround_times[process.name]:4} response {response_times[process.name]:4}")

if __name__ == "__main__":
    # Define the processes (name, arrival time, burst time)
    processes = [
        Process("A", 0, 5),
        Process("B", 1, 4),
        Process("C", 4, 2),
    ]

    runfor = 20  # Set the number of iterations to run for
    fifo_scheduler(processes, runfor)

import queue

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = None
        self.end_time = None

    def __lt__(self, other):
        # Priority comparison based on arrival_time
        return self.arrival_time < other.arrival_time

def fifo_scheduler(processes, runfor):
    current_time = 0
    ready_queue = queue.PriorityQueue()
    completed_processes = []
    total_processes = len(processes)
    response_times = {}
    turnaround_times = {}
    waiting_times = {}
    iteration = 0  # Counter for the number of iterations

    print(f"{total_processes} processes")
    print("Using First-In, First-Out (FIFO) based on arrival_time")

    selected_processes = set()  # Set to keep track of selected processes

    # Check for arriving processes before entering the while loop
    for process in processes:
        if process.arrival_time == current_time and process.start_time is None:
            print(f"Time {current_time:4} : {process.name} arrived")
            ready_queue.put(process)

    while len(completed_processes) != total_processes and iteration < runfor:
        if not ready_queue.empty():
            running_process = ready_queue.get()
            if running_process.name not in selected_processes:
                running_process.start_time = current_time
                print(f"Time {current_time:4} : {running_process.name} selected (burst {running_process.burst_time:4})")
                selected_processes.add(running_process.name)
            current_time += 1
            running_process.burst_time -= 1

            if running_process.burst_time == 0:
                running_process.end_time = current_time
                completed_processes.append(running_process)
                selected_processes.remove(running_process.name)  # Remove from selected set
                print(f"Time {current_time:4} : {running_process.name} finished")
            else:
                ready_queue.put(running_process)
        else:
            if len(completed_processes) < total_processes:
                print(f"Time {current_time:4} : Idle")
            current_time += 1

        iteration += 1

    # Calculate metrics
    for process in completed_processes:
        turnaround_time = process.end_time - process.arrival_time
        response_time = process.start_time - process.arrival_time
        waiting_time = turnaround_time - process.burst_time
        response_times[process.name] = response_time
        turnaround_times[process.name] = turnaround_time
        waiting_times[process.name] = waiting_time

    print(f"Finished at time {runfor}\n")  # Use runfor in the "Finished at time" line

    for process in completed_processes:
        print(f"{process.name} wait {waiting_times[process.name]:4} turnaround {turnaround_times[process.name]:4} response {response_times[process.name]:4}")

if __name__ == "__main__":
    # Define the processes (name, arrival time, burst time)
    processes = [
        Process("A", 0, 5),
        Process("B", 1, 4),
        Process("C", 4, 2),
    ]

    runfor = 10  # Set the number of iterations to run for
    fifo_scheduler(processes, runfor)

import queue

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = None
        self.end_time = None

    def __lt__(self, other):
        # Priority comparison based on arrival_time
        return self.arrival_time < other.arrival_time

def fifo_scheduler(processes, runfor):
    current_time = 0
    ready_queue = queue.PriorityQueue()
    completed_processes = []
    total_processes = len(processes)
    response_times = {}
    turnaround_times = {}
    waiting_times = {}
    iteration = 0  # Counter for the number of iterations

    print(f"{total_processes} processes")
    print("Using First-In, First-Out (FIFO) based on arrival_time")

    selected_processes = set()  # Set to keep track of selected processes

    # Initialize the queue before entering the loop
    for process in processes:
        if process.arrival_time == current_time and process.start_time is None:
            print(f"Time {current_time:4} : {process.name} arrived")
            ready_queue.put(process)

    while len(completed_processes) != total_processes and iteration < runfor:
        if not ready_queue.empty():
            running_process = ready_queue.get()
            if running_process.name not in selected_processes:
                running_process.start_time = current_time
                print(f"Time {current_time:4} : {running_process.name} selected (burst {running_process.burst_time:4})")
                selected_processes.add(running_process.name)
            current_time += 1
            running_process.burst_time -= 1

            if running_process.burst_time == 0:
                running_process.end_time = current_time
                completed_processes.append(running_process)
                selected_processes.remove(running_process.name)  # Remove from selected set
                print(f"Time {current_time:4} : {running_process.name} finished")
            else:
                ready_queue.put(running_process)
        else:
            if len(completed_processes) < total_processes:
                print(f"Time {current_time:4} : Idle")
            current_time += 1

        iteration += 1

    # Calculate metrics
    for process in completed_processes:
        turnaround_time = process.end_time - process.arrival_time
        response_time = process.start_time - process.arrival_time
        waiting_time = turnaround_time - process.burst_time
        response_times[process.name] = response_time
        turnaround_times[process.name] = turnaround_time
        waiting_times[process.name] = waiting_time

    print(f"Finished at time {runfor}\n")  # Use runfor in the "Finished at time" line

    for process in completed_processes:
        print(f"{process.name} wait {waiting_times[process.name]:4} turnaround {turnaround_times[process.name]:4} response {response_times[process.name]:4}")

if __name__ == "__main__":
    # Define the processes (name, arrival time, burst time)
    processes = [
        Process("A", 0, 5),
        Process("B", 1, 4),
        Process("C", 4, 2),
    ]

    runfor = 10  # Set the number of iterations to run for
    fifo_scheduler(processes, runfor)

import queue

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = None
        self.end_time = None

def fifo_scheduler(processes, runfor):
    current_time = 0
    ready_queue = queue.Queue()  # Change to a normal queue
    completed_processes = []
    total_processes = len(processes)
    response_times = {}
    turnaround_times = {}
    waiting_times = {}
    iteration = 0  # Counter for the number of iterations

    print(f"{total_processes} processes")
    print("Using First-In, First-Out (FIFO) based on arrival_time")

    selected_processes = set()  # Set to keep track of selected processes

    while len(completed_processes) != total_processes and iteration < runfor:
        # Check for arriving processes before each iteration
        for process in processes:
            if process.arrival_time == current_time and process.start_time is None:
                print(f"Time {current_time:4} : {process.name} arrived")
                ready_queue.put(process)

        if not ready_queue.empty():
            running_process = ready_queue.get()
            if running_process.name not in selected_processes:
                running_process.start_time = current_time
                print(f"Time {current_time:4} : {running_process.name} selected (burst {running_process.burst_time:4})")
                selected_processes.add(running_process.name)
            current_time += 1
            running_process.burst_time -= 1

            if running_process.burst_time == 0:
                running_process.end_time = current_time
                completed_processes.append(running_process)
                selected_processes.remove(running_process.name)  # Remove from selected set
                print(f"Time {current_time:4} : {running_process.name} finished")
            else:
                ready_queue.put(running_process)
        else:
            if len(completed_processes) < total_processes:
                print(f"Time {current_time:4} : Idle")
            current_time += 1

        iteration += 1

    # Calculate metrics
    for process in completed_processes:
        turnaround_time = process.end_time - process.arrival_time
        response_time = process.start_time - process.arrival_time
        waiting_time = turnaround_time - process.burst_time
        response_times[process.name] = response_time
        turnaround_times[process.name] = turnaround_time
        waiting_times[process.name] = waiting_time

    print(f"Finished at time {runfor}\n")  # Use runfor in the "Finished at time" line

    for process in completed_processes:
        print(f"{process.name} wait {waiting_times[process.name]:4} turnaround {turnaround_times[process.name]:4} response {response_times[process.name]:4}")

if __name__ == "__main__":
    # Define the processes (name, arrival time, burst time)
    processes = [
        Process("A", 0, 5),
        Process("B", 1, 4),
        Process("C", 4, 2),
    ]

    runfor = 10  # Set the number of iterations to run for
    fifo_scheduler(processes, runfor)

import queue

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = None
        self.end_time = None

def fifo_scheduler(processes, runfor):
    current_time = 0
    ready_queue = queue.Queue()  # Change to a normal queue
    completed_processes = []
    total_processes = len(processes)
    response_times = {}
    turnaround_times = {}
    waiting_times = {}
    iteration = 0  # Counter for the number of iterations

    print(f"{total_processes} processes")
    print("Using First-In, First-Out (FIFO) based on arrival_time")

    selected_processes = set()  # Set to keep track of selected processes

    while len(completed_processes) != total_processes and iteration < runfor:
        # Check for arriving processes before each iteration
        for process in processes:
            if process.arrival_time == current_time and process.start_time is None:
                print(f"Time {current_time:4} : {process.name} arrived")
                ready_queue.put(process)
        if not ready_queue.empty():
            running_process = ready_queue.get()
            if running_process.name not in selected_processes:
                running_process.start_time = current_time
                print(f"Time {current_time:4} : {running_process.name} selected (burst {running_process.burst_time:4})")
                selected_processes.add(running_process.name)
            current_time += 1
            running_process.burst_time -= 1

            if running_process.burst_time == 0:
                running_process.end_time = current_time
                completed_processes.append(running_process)
                selected_processes.remove(running_process.name)  # Remove from selected set
                print(f"Time {current_time:4} : {running_process.name} finished")
            else:
                ready_queue.put(running_process)
        else:
            if len(completed_processes) < total_processes:
                print(f"Time {current_time:4} : Idle")
            current_time += 1

        iteration += 1

    # Calculate metrics
    for process in completed_processes:
        turnaround_time = process.end_time - process.arrival_time
        response_time = process.start_time - process.arrival_time
        waiting_time = turnaround_time - process.burst_time
        response_times[process.name] = response_time
        turnaround_times[process.name] = turnaround_time
        waiting_times[process.name] = waiting_time

    # Check for unfinished processes in the ready_queue
    unfinished_processes = []
    while not ready_queue.empty():
        unfinished_process = ready_queue.get()
        unfinished_processes.append(unfinished_process)

    print(f"Finished at time {runfor}\n")  # Use runfor in the "Finished at time" line

    for process in completed_processes:
        print(f"{process.name} wait {waiting_times[process.name]:4} turnaround {turnaround_times[process.name]:4} response {response_times[process.name]:4}")

    for process in unfinished_processes:
        print(f"{process.name} did not finish")

if __name__ == "__main__":
    # Define the processes (name, arrival time, burst time)
    processes = [
        Process("A", 0, 5),
        Process("B", 1, 4),
        Process("C", 4, 2),
    ]

    runfor = 20  # Set the number of iterations to run for
    fifo_scheduler(processes, runfor)
'''
import queue

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = None
        self.end_time = None

def fifo_scheduler(processes, runfor):
    current_time = 0
    ready_queue = queue.Queue()  # Change to a normal queue
    completed_processes = []
    total_processes = len(processes)
    response_times = {}
    turnaround_times = {}
    waiting_times = {}
    iteration = 0  # Counter for the number of iterations

    print(f"{total_processes} processes")
    print("Using First-In, First-Out (FIFO) based on arrival_time")

    selected_processes = set()  # Set to keep track of selected processes

    while iteration < runfor:
        # Check for arriving processes before each iteration
        for process in processes:
            if process.arrival_time == current_time and process.start_time is None:
                print(f"Time {current_time:4} : {process.name} arrived")
                ready_queue.put(process)

        if not ready_queue.empty():
            running_process = ready_queue.get()
            if running_process.name not in selected_processes:
                running_process.start_time = current_time
                print(f"Time {current_time:4} : {running_process.name} selected (burst {running_process.burst_time:4})")
                selected_processes.add(running_process.name)
            current_time += 1
            running_process.burst_time -= 1

            if running_process.burst_time == 0:
                running_process.end_time = current_time
                completed_processes.append(running_process)
                selected_processes.remove(running_process.name)  # Remove from selected set
                print(f"Time {current_time:4} : {running_process.name} finished")
            else:
                ready_queue.put(running_process)
        else:
            print(f"Time {current_time:4} : Idle")
            current_time += 1

        iteration += 1

    # Calculate metrics
    for process in completed_processes:
        turnaround_time = process.end_time - process.arrival_time
        response_time = process.start_time - process.arrival_time
        waiting_time = turnaround_time - process.burst_time
        response_times[process.name] = response_time
        turnaround_times[process.name] = turnaround_time
        waiting_times[process.name] = waiting_time

    # Check for unfinished processes in the ready_queue
    unfinished_processes = []
    while not ready_queue.empty():
        unfinished_process = ready_queue.get()
        unfinished_processes.append(unfinished_process)

    print(f"Finished at time {runfor}\n")  # Use runfor in the "Finished at time" line

    for process in completed_processes:
        print(f"{process.name} wait {waiting_times[process.name]:4} turnaround {turnaround_times[process.name]:4} response {response_times[process.name]:4}")

    for process in unfinished_processes:
        print(f"{process.name} did not finish")

if __name__ == "__main__":
    # Define the processes (name, arrival time, burst time)
    processes = [
        Process("A", 0, 5),
        Process("B", 1, 4),
        Process("C", 4, 2),
    ]

    runfor = 10  # Set the number of iterations to run for
    fifo_scheduler(processes, runfor)
