# Port Mapping Program

## Overview

This program is designed to map open ports on a specified host or network. Created by Antonio Amaral Egydio Martins, it utilizes multithreading to enhance the scanning process, making it faster and more efficient. Users can specify the host, range of ports to scan, timeout for each connection attempt, number of threads, and whether to display closed ports.

## Features

- Fast scanning with configurable number of threads.
- Ability to set a custom timeout for connection attempts.
- Option to scan a specific range of ports.
- Option to show or hide closed ports.
- User-friendly CLI with color-coded outputs.

## Requirements

- Python 3.x
- Colorama library

## Installation

First, ensure you have Python 3 installed on your system. You can download Python from [python.org](https://www.python.org/downloads/).

Next, install using `pip` the necessary library:

```bash
pip install -r requirements.txt
```

## Usage

To start the program, navigate to the directory where the script is located and run:

```bash
python port_mapping.py
```

You will be prompted to enter:
- The Host or Network (e.g., 255.255.255.255 or google.com)
- The Port Range (e.g., 1-65535)
- The Timeout in seconds (default is 1 second)
- The Number of Threads (default is 100)
- Whether to Show Closed Ports (Y for yes, n for no)

After entering the required information, the program will begin scanning and display the results in real-time.

## Example

```bash
Enter the Host or Network (e.g., 255.255.255.255): google.com
Enter the Port Range (e.g., 1-65535): 1-1000
Enter the Timeout [1sec]: 2
Enter the Number of Threads [100]: 50
Show Closed Ports? [Y/n]: n
```

This will scan google.com for open ports in the range 1-1000, using a 2-second timeout and 50 threads, without showing closed ports.

## Contributing

Contributions to this project are welcome. Please fork the repository, make your changes, and submit a pull request.