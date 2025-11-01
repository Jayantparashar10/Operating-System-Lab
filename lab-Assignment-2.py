"""
OS Lab Assignment 2: System Startup and Process Simulation
Course: ENCS351 Operating System

This script simulates a basic system startup sequence.
It uses 'multiprocessing' to create child processes [cite: 98]
and 'logging' to track their lifecycle in a file[cite: 99, 100].
"""

import multiprocessing
import time
import logging
import sys

def system_process(task_name):
    
    logger = multiprocessing.get_logger()
    
    logger.info(f"{task_name} started")
    time.sleep(2)  
    logger.info(f"{task_name} ended")

def setup_logging():
    
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.INFO) 
    
    handler = logging.FileHandler('process_log.txt', mode='w')
    
    formatter = logging.Formatter(
        '%(asctime)s - %(processName)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    if not logger.hasHandlers():
        logger.addHandler(handler)

if __name__ == '__main__':
    
    setup_logging()
    
    print("System Starting...")
    logging.info("System Starting...") 

    p1 = multiprocessing.Process(target=system_process, args=('Process-1',)) 
    p2 = multiprocessing.Process(target=system_process, args=('Process-2',))

    p1.start() 
    p2.start() 

    p1.join() 
    p2.join() 
    
    logging.info("System Shutdown.")
    print("System Shutdown.") 