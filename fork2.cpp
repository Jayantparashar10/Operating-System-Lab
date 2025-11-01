#include <iostream>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int main() {
    int N;
    std::cout << "Enter number of child processes: ";
    std::cin >> N;

    std::string cmd;
    std::cout << "Enter command to execute (e.g., ls): ";
    std::cin >> cmd;

    for (int i = 0; i < N; ++i) {
        pid_t pid = fork();
        if (pid == 0) {
            char *args[] = {const_cast<char*>(cmd.c_str()), nullptr};
            std::cout << "Child #" << i << " executing command '" << cmd << "' with PID: " << getpid() << std::endl;
            execvp(args[0], args);
            perror("execvp failed");
            return 1;
        }
    }

    for (int i = 0; i < N; ++i) {
        wait(NULL);
    }
    std::cout << "All child processes executed the command." << std::endl;
    return 0;
}
