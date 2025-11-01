# Operating-System-Lab

This repository contains simple Operating Systems lab exercises (process/fork/zombie examples) created for a university course. The code demonstrates process creation, parent/child behavior, exit statuses, and zombie process formation on a Unix-like system (macOS in the provided workspace).

## Repository structure

- `fork.cpp` — simple example that uses `fork()` to create a child process and demonstrates parent/child execution order.
- `fork2.cpp` — variation on `fork()` usage (different order/behavior or arguments).
- `zombie.cpp` — demonstrates creation of a zombie process and how a parent can (or cannot) collect the child.
- `lab-assingment-1.py` — supporting Python script for the assignment (note the filename has a minor typo: "assingment").
- `Labs-assignment-1.ipynb` — Jupyter notebook version of the assignment/exploration.
- `output/` — contains compiled binaries and debug symbol bundles (`*.dSYM`) produced on the local machine.

## Quick build (macOS / zsh)

The `output/` directory already contains compiled binaries. To recompile from source, run these commands from the repository root. These commands use `g++`/`clang++` compatible flags and will place binaries into `output/`.

```bash
mkdir -p output
g++ -Wall -Wextra -std=c++17 -g -o output/fork fork.cpp
g++ -Wall -Wextra -std=c++17 -g -o output/fork2 fork2.cpp
g++ -Wall -Wextra -std=c++17 -g -o output/zombie zombie.cpp
```

Notes:
- The `-g` flag includes debug symbols (useful for `lldb`/`gdb`).
- On macOS, the system compiler is often `clang++`, and `g++` is an alias to it. The commands above work with either.

## Run examples

From the repository root run:

```bash
./output/fork
./output/fork2
./output/zombie
```

Observe console output for parent/child messages, exit codes, and (for `zombie`) the child process becoming a zombie until the parent reaps it.

To run the Python script:

```bash
python3 lab-assingment-1.py
```

Open the Jupyter notebook with:

```bash
jupyter notebook Labs-assignment-1.ipynb
```

## Debugging and inspection

- Use `ps aux | grep <binary-name>` to locate process states.
- Use `lldb ./output/zombie` to run under the debugger and step through forks.
- Inspect the `.dSYM` directories (macOS generated debug symbol bundles) if you need to symbolicate debug info.

## Expected behavior / learning goals

- Understand how `fork()` duplicates a process and how return values differ in parent vs child.
- Observe parent/child scheduling and ordering.
- See how a process becomes a zombie and how reaping (via `wait()`/`waitpid()`) removes zombies.

## Author / Contact

Author: Jayant Parashar


## License

This repository is provided for educational purposes. Add a license file (for example, MIT) if you intend to share or reuse this code beyond the course.

