import os
import sys
import time
import logging
import multiprocessing
import subprocess
import platform

# Task 1: Batch Processing Simulation
def batch_processing_simulation():
    print("\n=== Task 1: Batch Processing Simulation ===")
    # Create dummy scripts for demonstration
    scripts = ['script1.py', 'script2.py', 'script3.py']
    for name in scripts:
        with open(name, 'w') as f:
            f.write(f"print('Hello from {name}')")
    
    try:
        for script in scripts:
            print(f"Executing {script}...")
            # Use sys.executable to ensure we use the same python interpreter
            subprocess.call([sys.executable, script])
    except Exception as e:
        print(f"Error executing scripts: {e}")
    finally:
        # Clean up dummy scripts
        for name in scripts:
            if os.path.exists(name):
                os.remove(name)

# Task 2: System Startup and Logging
def process_task(name):
    logging.info(f"{name} started")
    time.sleep(1)
    logging.info(f"{name} terminated")

def system_startup_logging():
    print("\n=== Task 2: System Startup and Logging ===")
    # Configure logging
    logging.basicConfig(filename='system_log.txt', level=logging.INFO,
                        format='%(asctime)s - %(processName)s - %(message)s', force=True)
    
    print("System Booting...")
    p1 = multiprocessing.Process(target=process_task, args=("Process-1",))
    p2 = multiprocessing.Process(target=process_task, args=("Process-2",))
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
    print("System Shutdown. Logs recorded in system_log.txt.")

# Task 3: System Calls and IPC
def system_calls_ipc():
    print("\n=== Task 3: System Calls and IPC ===")
    
    # os.fork() is only available on Unix-like systems
    if not hasattr(os, 'fork'):
        print("os.fork() is not available on this operating system (Windows).")
        print("Skipping fork/exec/pipe simulation.")
        return

    try:
        r, w = os.pipe()
        pid = os.fork()
        
        if pid > 0:
            # Parent process
            os.close(r)
            print("Parent writing to pipe...")
            os.write(w, b"Hello from parent")
            os.close(w)
            os.wait()
        else:
            # Child process
            os.close(w)
            message = os.read(r, 1024)
            print("Child received:", message.decode())
            os.close(r)
            os._exit(0)
    except Exception as e:
        print(f"An error occurred during IPC simulation: {e}")

# Task 4: VM Detection and Shell Interaction
def vm_detection_shell():
    print("\n=== Task 4: VM Detection and Shell Interaction ===")
    
    print("--- System Info ---")
    print(f"System: {platform.system()}")
    print(f"Release: {platform.release()}")
    print(f"Version: {platform.version()}")
    print(f"Machine: {platform.machine()}")
    
    # Attempt to run shell commands if on Linux/Unix
    if platform.system() != "Windows":
        try:
            print("\nKernel Version:")
            subprocess.call(['uname', '-r'])
            print("User:")
            subprocess.call(['whoami'])
        except FileNotFoundError:
            pass

    print("\n--- VM Detection ---")
    is_vm = False
    
    # Basic heuristic checks
    if platform.system() == "Linux":
        try:
            with open('/proc/cpuinfo', 'r') as f:
                if 'hypervisor' in f.read().lower():
                    is_vm = True
        except:
            pass
        # Check for product_name
        try:
            with open('/sys/class/dmi/id/product_name', 'r') as f:
                product_name = f.read().lower()
                if 'virtualbox' in product_name or 'vmware' in product_name or 'kvm' in product_name:
                    is_vm = True
        except:
            pass
            
    elif platform.system() == "Windows":
        try:
            # Check manufacturer via wmic
            output = subprocess.check_output("wmic computersystem get manufacturer", shell=True).decode().lower()
            if "vmware" in output or "virtualbox" in output or "qemu" in output or "innotek" in output:
                is_vm = True
        except:
            pass

    if is_vm:
        print("Result: System is likely running inside a Virtual Machine.")
    else:
        print("Result: System appears to be running on physical hardware (or VM not detected).")

# Task 5: CPU Scheduling Algorithms
def fcfs_scheduling():
    print("\n--- FCFS Scheduling ---")
    try:
        n = int(input("Enter number of processes: "))
        processes = []
        for i in range(n):
            bt = int(input(f"Enter Burst Time for P{i+1}: "))
            processes.append({'pid': i+1, 'bt': bt})
        
        wt = 0
        total_wt = 0
        total_tt = 0
        
        print("PID\tBT\tWT\tTAT")
        for p in processes:
            tat = wt + p['bt']
            print(f"{p['pid']}\t{p['bt']}\t{wt}\t{tat}")
            total_wt += wt
            total_tt += tat
            wt += p['bt']
            
        if n > 0:
            print(f"Average Waiting Time: {total_wt / n:.2f}")
            print(f"Average Turnaround Time: {total_tt / n:.2f}")
    except ValueError:
        print("Invalid input.")

def sjf_scheduling():
    print("\n--- SJF Scheduling (Non-preemptive) ---")
    try:
        n = int(input("Enter number of processes: "))
        processes = []
        for i in range(n):
            bt = int(input(f"Enter Burst Time for P{i+1}: "))
            processes.append({'pid': i+1, 'bt': bt})
            
        # Sort by burst time
        processes.sort(key=lambda x: x['bt'])
        
        wt = 0
        total_wt = 0
        total_tt = 0
        
        print("PID\tBT\tWT\tTAT")
        for p in processes:
            tat = wt + p['bt']
            print(f"{p['pid']}\t{p['bt']}\t{wt}\t{tat}")
            total_wt += wt
            total_tt += tat
            wt += p['bt']
            
        if n > 0:
            print(f"Average Waiting Time: {total_wt / n:.2f}")
            print(f"Average Turnaround Time: {total_tt / n:.2f}")
    except ValueError:
        print("Invalid input.")

def priority_scheduling():
    print("\n--- Priority Scheduling ---")
    processes = []
    try:
        n = int(input("Enter number of processes: "))
        for i in range(n):
            bt = int(input(f"Enter Burst Time for P{i+1}: "))
            pr = int(input(f"Enter Priority (lower number = higher priority) for P{i+1}: "))
            processes.append((i+1, bt, pr))
        
        processes.sort(key=lambda x: x[2])
        
        wt = 0
        total_wt = 0
        total_tt = 0
        
        print("PID\tBT\tPriority\tWT\tTAT")
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
        print("Invalid input.")

def round_robin_scheduling():
    print("\n--- Round Robin Scheduling ---")
    try:
        n = int(input("Enter number of processes: "))
        processes = []
        for i in range(n):
            bt = int(input(f"Enter Burst Time for P{i+1}: "))
            # [PID, Burst Time, Remaining Time, Waiting Time, Turnaround Time]
            processes.append([i+1, bt, bt, 0, 0])
            
        quantum = int(input("Enter Time Quantum: "))
        
        time = 0
        completed = 0
        
        while completed < n:
            check = False
            for p in processes:
                if p[2] > 0:
                    check = True
                    if p[2] > quantum:
                        time += quantum
                        p[2] -= quantum
                    else:
                        time += p[2]
                        p[3] = time - p[1]
                        p[2] = 0
                        p[4] = time
                        completed += 1
            if not check:
                break
                
        total_wt = sum(p[3] for p in processes)
        total_tt = sum(p[4] for p in processes)
        
        print("PID\tBT\tWT\tTAT")
        for p in processes:
            print(f"{p[0]}\t{p[1]}\t{p[3]}\t{p[4]}")
            
        if n > 0:
            print(f"Average Waiting Time: {total_wt / n:.2f}")
            print(f"Average Turnaround Time: {total_tt / n:.2f}")
    except ValueError:
        print("Invalid input.")

def cpu_scheduling_algorithms():
    print("\n=== Task 5: CPU Scheduling Algorithms ===")
    fcfs_scheduling()
    sjf_scheduling()
    priority_scheduling()
    round_robin_scheduling()

def main():
    batch_processing_simulation()
    system_startup_logging()
    system_calls_ipc()
    vm_detection_shell()
    cpu_scheduling_algorithms()

if __name__ == "__main__":
    main()
