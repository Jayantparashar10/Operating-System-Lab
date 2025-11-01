#include <iostream>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

void zombie_demo() {
    pid_t pid = fork();
    if (pid == 0) {
        std::cout << "Zombie Child: PID " << getpid() << std::endl;
        return; 
    } else {
        std::cout << "Parent (Zombie Demo): PID " << getpid() << ", Child PID: " << pid << std::endl;
        sleep(10); 
        
    }
}

void orphan_demo() {
    pid_t pid = fork();
    if (pid == 0) {
        sleep(5); 
        std::cout << "Orphan Child: PID " << getpid() << ", New Parent PID: " << getppid() << std::endl;
        return;
    } else {
        std::cout << "Parent (Orphan Demo): PID " << getpid() << ", exiting." << std::endl;
        return; 
    }
}

int main() {
    std::cout << "--- Zombie Demo ---" << std::endl;
    zombie_demo();
    sleep(15); 
    std::cout << "\n--- Orphan Demo ---" << std::endl;
    orphan_demo();
    sleep(10); 
    return 0;
}
