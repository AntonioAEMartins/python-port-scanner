# Port Mapping Program

## Overview

This program, created by Antonio Amaral Egydio Martins, is designed to map open ports on a specified host or across a network range. It utilizes multithreading to enhance the scanning process, making it faster and more efficient. Users can choose between scanning a single host or multiple hosts within a specified network range. The program allows users to specify the range of ports to scan, set a timeout for each connection attempt, configure the number of threads, and decide whether to display closed ports. The user-friendly CLI provides color-coded outputs for easy interpretation of results.

## Features

- Two modes of operation: scan a single host or a network range.
- Fast scanning with a configurable number of threads.
- Ability to set a custom timeout for connection attempts.
- Option to scan a specific range of ports.
- Option to show or hide closed ports in the output.
- Color-coded outputs for better readability.

## Requirements

- Python 3.x
- Colorama library
- ipaddress library (for network range scanning)

## Installation

Ensure Python 3 is installed on your system. Download Python from [python.org](https://www.python.org/downloads/).

Install the necessary libraries using `pip`:

```bash
pip install -r requirements.txt
```

## Usage

To start the program, navigate to the directory where the script is located and run:

```bash
python port_mapping.py
```

You will first be prompted to select the program to run:
1. Port Scan Program (for a single host)
2. Network Scan Program (for a network range)

For **Port Scan Program**, enter:
- The Host (e.g., google.com)
- The Port Range (e.g., 1-65535)
- The Timeout in seconds (default is 1 second)
- The Number of Threads (default is 100)
- Whether to Show Closed Ports (Y for yes, n for no)

For **Network Scan Program**, enter:
- The IP Range (e.g., 192.168.1.0/24)
- The Port Range (e.g., 1-65535)
- Optionally save the settings for the entire range scan

After entering the required information, the program will begin scanning and display the results in real-time.

## Example

For a single host:

```bash
Enter your choice (1 or 2): 1
Enter the Host (e.g., google.com): google.com
Enter the Port Range (e.g., 1-65535): 1-1000
Enter the Timeout [1sec]: 2
Enter the Number of Threads [100]: 50
Show Closed Ports? [Y/n]: n
```

This will scan google.com for open ports in the range 1-1000, using a 2-second timeout and 50 threads, without showing closed ports.

For a network range:

```bash
Enter your choice (1 or 2): 2
Enter the IP Range (e.g., 192.168.1.0/24): 192.168.1.0/24
Enter the Port Range (e.g., 1-65535): 1-1000
Enter the Timeout [1sec]: 2
Enter the Number of Threads [100]: 50
Show Closed Ports? [Y/n]: n
Save settings for remaining IPs? [Y/n]: Y
```

This will scan the entire network range of `192.168.1.0/24` for open ports in the range 1-1000, using a 2-second timeout and 50 threads, without showing closed ports, and will use the same settings for all IPs in the range.

## Contributing

Contributions to this project are welcome. Please fork the repository, make your changes, and submit a pull request.