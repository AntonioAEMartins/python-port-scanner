from datetime import datetime
import socket
from colorama import Fore, Style, init
import os
import threading
from queue import Queue

init()

THREADS = 100
queue = Queue()

def print_boxed(msg, color=Fore.GREEN):
    border = '+' + '-' * (len(msg) + 2) + '+'
    print(color + border)
    print(f'| {msg} |')
    print(border + Style.RESET_ALL)

def selectInput():
    print("This program will help you map open ports on a network or host.")
    host = input(Fore.YELLOW + "Enter the Host or Network (e.g., 255.255.255.255): " + Style.RESET_ALL)
    host = socket.gethostbyname(host)
    port_range = input(Fore.YELLOW + "Enter the Port Range (e.g., 1-65535): " + Style.RESET_ALL)
    timeout = input(Fore.YELLOW + "Enter the Timeout [1sec]: " + Style.RESET_ALL)
    if not timeout:
        timeout = 1
    else:
        timeout = int(timeout)
    number_threads = input(Fore.YELLOW + f"Enter the Number of Threads [100]: " + Style.RESET_ALL)
    if not number_threads:
        number_threads = 100
    else:
        number_threads = int(number_threads)
    show_error_output = input(Fore.YELLOW + "Show Closed Ports? [Y/n]: " + Style.RESET_ALL)
    if show_error_output.lower() == "n":
        show_error_output = False
    else:
        show_error_output = True
    print_boxed(f"Mapping Host: {host} - Port Range: {port_range} - Timeout: {timeout} sec - Threads: {number_threads} - Show Error Output: {show_error_output}")
    port_start_range, port_end_range = port_range.split("-")
    port_range = range(int(port_start_range), int(port_end_range) + 1)
    return host, port_range, timeout, number_threads, show_error_output

def tcp_port_scanner(host, timeout=1, show_error_output=False):
    while not queue.empty():
        port = queue.get()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            try:
                result = s.connect_ex((host, port))
                service_name = "Unknown"
                if result == 0:
                    try:
                        service_name = socket.getservbyport(port)
                    except OSError:
                        pass
                    print(Fore.GREEN + f"Port {port} is open, Service Name: {service_name}" + Style.RESET_ALL)
                else:
                    if (show_error_output):
                        print(Fore.RED + f"Port {port} is closed" + Style.RESET_ALL)
            except socket.timeout:
                print(Fore.YELLOW + f"Timeout connecting to port {port}" + Style.RESET_ALL)
            except socket.error:
                print(Fore.RED + f"Couldn't connect to port {port}" + Style.RESET_ALL)
            except KeyboardInterrupt:
                print(Fore.RED + "You pressed Ctrl+C" + Style.RESET_ALL)
                os._exit(1)
            finally:
                queue.task_done()

def main():
    print(Fore.CYAN + "-" * 64)
    print("Port Mapping Started - Created by Antonio Amaral Egydio Martins")
    print("-" * 64 + Style.RESET_ALL)
    t1 = datetime.now()
    host, port_range, timeout, number_threads, show_error_output = selectInput()

    for port in port_range:
        queue.put(port)
    
    for t in range(number_threads):
        thread = threading.Thread(target=tcp_port_scanner, args=(host,timeout,show_error_output))
        thread.daemon = True 
        thread.start()

    queue.join()

    t2 = datetime.now()
    print_boxed(f"Mapping Completed in {t2 - t1}", Fore.CYAN)

if __name__ == "__main__":
    main()
