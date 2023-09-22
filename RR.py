import sys


class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.start_time = -1
        self.finish_time = -1


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

    round_robin(input_filename)

