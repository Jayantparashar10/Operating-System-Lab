import os

# Task 1: CPU Scheduling - Priority
def priority_scheduling():
    print("\n--- Priority Scheduling Simulation ---")
    processes = []
    try:
        n = int(input("Enter number of processes: "))
        for i in range(n):
            bt = int(input(f"Enter Burst Time for P{i+1}: "))
            pr = int(input(f"Enter Priority (lower number = higher priority) for P{i+1}: "))
            processes.append((i+1, bt, pr))
        
        # Sort by priority (lower number = higher priority)
        processes.sort(key=lambda x: x[2])
        
        wt = 0
        total_wt = 0
        total_tt = 0
        
        print("\nPID\tBT\tPriority\tWT\tTAT")
        for pid, bt, pr in processes:
            tat = wt + bt
            print(f"{pid}\t{bt}\t{pr}\t\t{wt}\t{tat}")
            total_wt += wt
            total_tt += tat
            wt += bt
            
        if n > 0:
            print(f"Average Waiting Time: {total_wt / n:.2f}")
            print(f"Average Turnaround Time: {total_tt / n:.2f}")
    except ValueError:
        print("Invalid input. Please enter integers.")

# Task 1: CPU Scheduling - Round Robin
def round_robin_scheduling():
    print("\n--- Round Robin Scheduling Simulation ---")
    try:
        n = int(input("Enter number of processes: "))
        processes = []
        for i in range(n):
            bt = int(input(f"Enter Burst Time for P{i+1}: "))
            # Process structure: [PID, Burst Time, Remaining Time, Waiting Time, Turnaround Time]
            processes.append([i+1, bt, bt, 0, 0])
            
        quantum = int(input("Enter Time Quantum: "))
        
        time = 0
        completed = 0
        
        # Keep looping until all processes are completed
        while completed < n:
            check = False
            for p in processes:
                if p[2] > 0: # If remaining time > 0
                    check = True
                    if p[2] > quantum:
                        time += quantum
                        p[2] -= quantum
                    else:
                        time += p[2]
                        p[3] = time - p[1] # Waiting Time = Completion Time - Burst Time
                        p[2] = 0
                        p[4] = time # Turnaround Time = Completion Time
                        completed += 1
            if not check:
                break
                
        total_wt = sum(p[3] for p in processes)
        total_tt = sum(p[4] for p in processes)
        
        print("\nPID\tBT\tWT\tTAT")
        for p in processes:
            print(f"{p[0]}\t{p[1]}\t{p[3]}\t{p[4]}")
            
        if n > 0:
            print(f"Average Waiting Time: {total_wt / n:.2f}")
            print(f"Average Turnaround Time: {total_tt / n:.2f}")

    except ValueError:
        print("Invalid input. Please enter integers.")

# Task 2: Sequential File Allocation
def sequential_file_allocation():
    print("\n--- Sequential File Allocation ---")
    try:
        total_blocks = int(input("Enter total number of blocks: "))
        block_status = [0] * total_blocks

        n = int(input("Enter number of files: "))
        for i in range(n):
            start = int(input(f"Enter starting block for file {i+1}: "))
            length = int(input(f"Enter length of file {i+1}: "))
            allocated = True
            
            # Check availability
            for j in range(start, start+length):
                if j >= total_blocks or block_status[j] == 1:
                    allocated = False
                    break
            
            if allocated:
                for j in range(start, start+length):
                    block_status[j] = 1
                print(f"File {i+1} allocated from block {start} to {start+length-1}")
            else:
                print(f"File {i+1} cannot be allocated.")
    except ValueError:
        print("Invalid input.")

# Task 3: Indexed File Allocation
def indexed_file_allocation():
    print("\n--- Indexed File Allocation ---")
    try:
        total_blocks = int(input("Enter total number of blocks: "))
        block_status = [0] * total_blocks
        n = int(input("Enter number of files: "))
        
        for i in range(n):
            index = int(input(f"Enter index block for file {i+1}: "))
            if index >= total_blocks or block_status[index] == 1:
                print("Index block already allocated or invalid.")
                continue
                
            count = int(input("Enter number of data blocks: "))
            print("Enter block numbers (space separated): ")
            data_blocks = list(map(int, input().split()))
            
            if len(data_blocks) != count:
                print("Number of blocks entered does not match count.")
                continue
                
            # Check if any block is already allocated
            conflict = False
            for blk in data_blocks:
                if blk >= total_blocks or block_status[blk] == 1:
                    conflict = True
                    break
            
            if conflict:
                print("Block(s) already allocated or invalid input.")
                continue
            
            # Allocate
            block_status[index] = 1
            for blk in data_blocks:
                block_status[blk] = 1
            print(f"File {i+1} allocated with index block {index} -> {data_blocks}")
            
    except ValueError:
        print("Invalid input.")

# Task 4: Contiguous Memory Allocation
def contiguous_memory_allocation():
    print("\n--- Contiguous Memory Allocation ---")
    
    def allocate_memory(strategy):
        print(f"\nRunning {strategy.upper()} Fit Strategy:")
        try:
            print("Enter partition sizes (space separated): ")
            partitions = list(map(int, input().split()))
            
            print("Enter process sizes (space separated): ")
            processes = list(map(int, input().split()))
            
            allocation = [-1] * len(processes)

            for i, psize in enumerate(processes):
                idx = -1
                if strategy == "first":
                    for j, part in enumerate(partitions):
                        if part >= psize:
                            idx = j
                            break
                elif strategy == "best":
                    best_fit = float("inf")
                    for j, part in enumerate(partitions):
                        if part >= psize and part < best_fit:
                            best_fit = part
                            idx = j
                elif strategy == "worst":
                    worst_fit = -1
                    for j, part in enumerate(partitions):
                        if part >= psize and part > worst_fit:
                            worst_fit = part
                            idx = j
                
                if idx != -1:
                    allocation[i] = idx
                    partitions[idx] -= psize

            for i, a in enumerate(allocation):
                if a != -1:
                    print(f"Process {i+1} allocated in Partition {a+1}")
                else:
                    print(f"Process {i+1} cannot be allocated")
        except ValueError:
            print("Invalid input.")

    allocate_memory("first")
    allocate_memory("best")
    allocate_memory("worst")

# Task 5: MFT Memory Management
def mft_memory_management():
    print("\n--- MFT (Fixed Partition) Simulation ---")
    try:
        mem_size = int(input("Enter total memory size: "))
        part_size = int(input("Enter partition size: "))
        n = int(input("Enter number of processes: "))
        
        if part_size == 0:
            print("Partition size cannot be 0.")
            return

        partitions = mem_size // part_size
        print(f"Memory divided into {partitions} partitions")
        
        for i in range(n):
            psize = int(input(f"Enter size of Process {i+1}: "))
            if psize <= part_size:
                print(f"Process {i+1} allocated.")
            else:
                print(f"Process {i+1} too large for fixed partition.")
    except ValueError:
        print("Invalid input.")

# Task 5: MVT Memory Management
def mvt_memory_management():
    print("\n--- MVT (Variable Partition) Simulation ---")
    try:
        mem_size = int(input("Enter total memory size: "))
        n = int(input("Enter number of processes: "))
        for i in range(n):
            psize = int(input(f"Enter size of Process {i+1}: "))
            if psize <= mem_size:
                print(f"Process {i+1} allocated.")
                mem_size -= psize
                print(f"Remaining Memory: {mem_size}")
            else:
                print(f"Process {i+1} cannot be allocated. Not enough memory.")
    except ValueError:
        print("Invalid input.")

def main():
    priority_scheduling()
    round_robin_scheduling()
    sequential_file_allocation()
    indexed_file_allocation()
    contiguous_memory_allocation()
    mft_memory_management()
    mvt_memory_management()

if __name__ == "__main__":
    main()
