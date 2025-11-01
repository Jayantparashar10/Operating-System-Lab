
"""
OS Lab Assignment 1: Process Creation and Management
Course: ENCS351 Operating System


This script covers:
Task 1: Process Creation Utility (os.fork(), os.wait())

Task 2: Command Execution (os.execvp(), subprocess.run())

Task 3: Zombie & Orphan Processes


Task 4: Inspecting Process Info from /proc


Task 5: Process Prioritization (os.nice())

"""

import os
import sys
import time
import subprocess

# Task 1: Process Creation Utility (os.fork(), os.wait())
def task1_create_processes(n=3):
   
    print(f"Task 1: Creating {n} Child Processes")
    print(f"Parent process (PID: {os.getpid()}) is starting.")
    
    child_pids = []
    for i in range(n):
        pid = os.fork()
        
        if pid > 0:
            child_pids.append(pid)
            
        elif pid == 0:
            my_pid = os.getpid()
            
            my_ppid = os.getppid()
            print(f"[Child {i+1}] PID: {my_pid}, Parent PID: {my_ppid}, Message: Hello!")
            
            os._exit(0) 
            
        else:
            print("Fork failed!", file=sys.stderr)
            sys.exit(1)

    print(f"\nParent (PID: {os.getpid()}) is waiting for {n} children...")
    
    for _ in range(n):
        try:
            (reaped_pid, status) = os.wait()
            print(f"Parent: Reaped child with PID {reaped_pid}. Status: {status}")
        except ChildProcessError:
            pass
            
    print("Task 1: All children terminated. Parent exiting.")


# Task 2: Command Execution (os.execvp(), subprocess.run())
def task2_command_execution(command="ls"):
    
    print(f"Task 2: Executing Command '{command}'")
    
    print("\nMethod 1: Using subprocess.run()")
    pid = os.fork()
    if pid == 0:
        print(f"[Child PID: {os.getpid()}] Executing '{command} -l':")
        try:
            subprocess.run([command, "-l"])
        except FileNotFoundError:
            print(f"Error: Command '{command}' not found.")
        os._exit(0) 
    else:
        os.wait() 
        print("Parent: Child finished subprocess.run().")

    print("\nMethod 2: Using os.execvp()")
    pid = os.fork()
    if pid == 0:
        print(f"[Child PID: {os.getpid()}] Using os.execvp() to become 'date'...")
        try:
            os.execvp("date", ["date"]) 
        except FileNotFoundError:
            print("Error: Command 'date' not found.")
            os._exit(1) 
    else:
        os.wait() 
        print("Parent: Child (which became 'date') finished.")
        
    print("Task 2: Finished.")


# Task 3: Zombie & Orphan Processes
def task3_zombie_process():
    
    print("Task 3: Simulating a ZOMBIE Process")
    pid = os.fork()
    
    if pid > 0:
        print(f"Parent (PID: {os.getpid()}) is sleeping for 30 seconds.")
        print(f"The child (PID: {pid}) will exit, but parent will NOT wait().")
        print("Run 'ps -el | grep defunct' or 'ps -el | grep Z' in another terminal to see the zombie.")
        time.sleep(30) 
        
        (reaped_pid, status) = os.wait()
        print(f"Parent finally reaping zombie child (PID: {reaped_pid}).")
        
    else:
        print(f"Child (PID: {os.getpid()}) is exiting immediately.")
        os._exit(0) 

def task3_orphan_process():
    
    print("Task 3: Simulating an ORPHAN Process")
    pid = os.fork()
    
    if pid > 0:
        print(f"Parent (PID: {os.getpid()}) is exiting in 2 seconds.")
        time.sleep(2)
        print("Parent is exiting now.")
        sys.exit(0) 
        
    else:
        my_pid = os.getpid()
        original_ppid = os.getppid()
        print(f"Child (PID: {my_pid}) started with Parent (PID: {original_ppid}).")
        
        print("Child is sleeping for 10 seconds.")
        time.sleep(10)
        
        new_ppid = os.getppid()
        print(f"Child (PID: {my_pid}) is awake. Original PPID: {original_ppid}, New PPID: {new_ppid}.")
        print("Child is exiting.")
        os._exit(0)

# Task 4: Inspecting Process Info from /proc
def task4_inspect_proc(target_pid):
    
    print(f"Task 4: Inspecting /proc/{target_pid}")
    
    try:
        print(f"\n[+] From /proc/{target_pid}/status:")
        with open(f"/proc/{target_pid}/status") as f:
            for line in f:
                if line.startswith("Name:") or line.startswith("State:") or line.startswith("VmSize:"):
                    print(f"  {line.strip()}")
                    
        print(f"\n[+] Executable Path from /proc/{target_pid}/exe:")
        
        exe_path = os.readlink(f"/proc/{target_pid}/exe")
        print(f"  {exe_path}")
        
        print(f"\n[+] Open File Descriptors from /proc/{target_pid}/fd:")
        
        fd_list = os.listdir(f"/proc/{target_pid}/fd")
        print(f"  Total: {len(fd_list)} open FDs.")
        print(f"  {fd_list}")
        
    except FileNotFoundError:
        print(f"Error: Process with PID {target_pid} not found (or /proc not available).", file=sys.stderr)
    except PermissionError:
        print(f"Error: Permission denied. Try running as root or on your own process.", file=sys.stderr)
        
    print("Task 4: Finished.")

# Task 5: Process Prioritization 
def task5_prioritization():
    
    print("Task 5: Process Prioritization (Nice)")
    print("Creating two children. Child 1 gets low priority (nice=10). Child 2 gets default (nice=0).")
    
    def cpu_intensive_task(label, nice_val):
       
        my_pid = os.getpid()
        
        os.nice(nice_val) 
        
        print(f"[Child {label}, PID: {my_pid}, Nice: {os.nice(0)}] Starting CPU task.")
        
        count = 0
        for _ in range(150_000_000): 
            count += 1
            
        print(f"[Child {label}, PID: {my_pid}] Finished.")
        os._exit(0)

    pid1 = os.fork()
    if pid1 == 0:
        cpu_intensive_task("1 (Low Priority)", 10) 

    pid2 = os.fork()
    if pid2 == 0:
        cpu_intensive_task("2 (Default Priority)", 0) 
    
    print("Parent waiting for both children...")
    os.waitpid(pid1, 0)
    print("Parent: Child 1 finished.")
    os.waitpid(pid2, 0)
    print("Parent: Child 2 finished.")
    print("Task 5: Finished.")


# Main execution block to select a task
if __name__ == "__main__":
    
    print("RUNNING ALL TASKS SEQUENTIALLY \n")
    print("\n" + "\n")
    # Task 1
    task1_create_processes(n=3)
    time.sleep(2) 
    print("\n" + "\n")

    print("\n" + "\n")
    # Task 2
    task2_command_execution(command="ls")
    time.sleep(2)
    print("\n" + "\n")


    print("\n" + "\n")
    # Task 3 (Zombie)
    print("NOTE: Task 3 (Zombie) will pause for 30 seconds.")
    print("In another terminal, run: ps -el | grep defunct")
    task3_zombie_process()
    time.sleep(2)
    print("\n" + "\n")

    print("\n" + "\n")
    # Task 4
    my_pid = os.getpid()
    print(f"NOTE: Running Task 4 on current process (PID: {my_pid}).")
    task4_inspect_proc(my_pid)
    time.sleep(2)
    print("\n" + "\n")

    print("\n" + "\n")
    # Task 5 
    print("NOTE: Task 5 will run CPU-intensive tasks.")
    task5_prioritization()
    print("\n" + "\n")
    
    print("NOTE: Task 3 (Orphan) was skipped because it is designed to")
    print("terminate the script. To test it, run it separately.")    