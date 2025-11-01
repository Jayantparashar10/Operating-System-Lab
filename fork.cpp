#include <iostream>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int main() {
    int N;
    std::cout << "Enter number of child processes: ";
    std::cin >> N;

    for (int i = 0; i < N; ++i) {
        pid_t pid = fork();
        if (pid == 0) {
            std::cout << "Child #" << i << " PID: " << getpid()
                      << ", Parent PID: " << getppid()
                      << ", Message: I am child process " << i << std::endl;
            return 0; 
        }
    }

    for (int i = 0; i < N; ++i) {
        wait(NULL);  
    }
    std::cout << "All child processes have finished." << std::endl;
    return 0;
}
