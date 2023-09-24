'''
Team Members:
Akeen Lewis
Chris Flannery
David Ferguson
McGreggor Kennison
'''

import sys


class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.start_time = -1
        self.finish_time = -1
        self.wait_time = 0
        self.turnaround_time = 0
        self.response_time = -1

def round_robin(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    required_params = ["processcount", "runfor", "use"]
    for param in required_params:
        if not any(param in line for line in lines):
            print(f"Error: Missing parameter {param}.")
            return

    if "use rr" in "".join(lines) and not any("quantum" in line for line in lines):
        print("Error: Missing quantum parameter when use is 'rr'.")
        return

    processcount = int(lines[0].split()[1])
    runfor = int(lines[1].split()[1])
    algorithm = lines[2].split()[1]

    if algorithm != "rr":
        print(f"Error: Only 'rr' algorithm is supported.")
        return

    quantum = int(lines[3].split()[1])
    processes = [Process(parts[2], int(parts[4]), int(parts[6])) for parts in
                 [line.split() for line in lines[4:4 + processcount]]]

    # Here starts the simulation
    time = 0
    queue = []
    results = []
    unfinished = []
    stats = []

    while time < runfor:
        # Add arriving processes to the queue
        arrivals = [p for p in processes if p.arrival_time == time]
        for p in arrivals:
            results.append(f"Time {time:3} : {p.name} arrived")
        queue.extend(arrivals)

        if queue:
            current_process = queue.pop(0)
            if current_process.start_time == -1:
                current_process.start_time = time
                results.append(
                    f"Time {time:3} : {current_process.name} selected (burst {current_process.remaining_time:3})")

            for _ in range(quantum):
                if current_process.remaining_time > 0:
                    current_process.remaining_time -= 1
                    time += 1
                if current_process.remaining_time == 0:
                    current_process.finish_time = time
                    results.append(f"Time {time:3} : {current_process.name} finished")
                    break
            if current_process.remaining_time > 0:
                queue.append(current_process)
        else:
            results.append(f"Time {time:3} : Idle")
            time += 1

    for p in processes:
        if p.finish_time == -1:
            unfinished.append(f"{p.name} did not finish")
        else:
            wait_time = p.start_time - p.arrival_time
            turnaround_time = p.finish_time - p.arrival_time
            response_time = wait_time
            stats.append(f"{p.name} wait {wait_time:3} turnaround {turnaround_time:3} response {response_time:3}")

    output = []
    output.append(f"{processcount} processes")
    output.append("Using Round Robin")
    output.append(f"Quantum: {quantum}")
    output.extend(results)
    output.append(f"Finished at time {time}")
    for u in unfinished:
        output.append(u)
    output.extend(stats)

    with open(filename.replace(".in", ".out"), 'w') as out_file:
        for line in output:
            out_file.write(line + "\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: scheduler-get.py <input file>")
        sys.exit(1)

    input_filename = sys.argv[1]
    if not input_filename.endswith(".in"):
        print("Error: The input file should have an '.in' extension.")
        sys.exit(1)

    with open('input.in', 'r') as file:
        contents = file.read()

        if 'use rr' in contents:
            round_robin(input_filename)
        if 'use sfj' in contents:
            print('The file contains "use sfj".')
        if 'use fcfs' in contents:
            print('The file contains "use fifo".')



def sjf_scheduler(processes, run_for):
    current_time = 0
    event_log = []
    process_queue = []
    finished_processes = []

    while current_time < run_for:
        for process in processes:
            if process.arrival_time == current_time:
                event_log.append(f"Time {current_time:3d} : {process.name} arrived")
                process_queue.append(process)
        
        if not process_queue:
            event_log.append(f"Time {current_time:3d} : Idle")
            current_time += 1
            continue
        
        process_queue.sort(key=lambda x: (x.remaining_time, x.name))
        current_process = process_queue[0]

        if current_process.response_time == -1:
            current_process.response_time = current_time
            event_log.append(f"Time {current_time:3d} : {current_process.name} selected (burst {current_process.remaining_time:3d})")

        if current_process.remaining_time == current_process.burst_time:
            current_process.wait_time = current_time - current_process.arrival_time

        current_process.remaining_time -= 1

        if current_process.remaining_time == 0:
            event_log.append(f"Time {current_time+1:3d} : {current_process.name} finished")
            finished_processes.append(current_process)
            process_queue.remove(current_process)
        
        current_time += 1

    return event_log, finished_processes

def main(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    process_count = None
    run_for = None
    algorithm = None
    quantum = None
    input_processes = []  # Store processes in input order

    for line in lines:
        line = line.strip().split()
        if line[0] == "processcount":
            process_count = int(line[1])
        elif line[0] == "runfor":
            run_for = int(line[1])
        elif line[0] == "use":
            algorithm = line[1]
        elif line[0] == "quantum":
            quantum = int(line[1])
        elif line[0] == "process":
            name = line[2]
            arrival_time = int(line[4])  # Adjusted index to 4 for arrival_time
            burst_time = int(line[6])    # Adjusted index to 6 for burst_time
            input_processes.append(Process(name, arrival_time, burst_time))

    if algorithm == "sjf":
        event_log, finished_processes = sjf_scheduler(input_processes, run_for)
    else:
        event_log = []
        finished_processes = []

    print(f"{process_count} processes")
    print(f"Using preemptive {algorithm} Shortest Job First")

    for log in event_log:
        print(log)

    print(f"Finished at time {run_for}\n")  # Adjusted the finished time

    # Display process statistics in the order they appear in the input
    for process in input_processes:
        turnaround_time = process.wait_time + process.burst_time
        response_time = process.response_time - process.arrival_time
        print(f"{process.name} wait {process.wait_time:3d} turnaround {turnaround_time:3d} response {response_time:3d}")

    # List processes that didn't finish
    not_finished = [process.name for process in input_processes if process not in finished_processes]
    for process in not_finished:
        print(f"{process} did not finish")

if __name__ == "__main__":
    main("input1.in")  # Replace with your input file
