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
