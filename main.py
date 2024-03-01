from datetime import datetime
import socket
from colorama import Fore, Style, init
import os
import threading
from queue import Queue
import ipaddress

init()

THREADS = 100
queue = Queue()

def print_boxed(msg, color=Fore.GREEN):
    border = '+' + '-' * (len(msg) + 2) + '+'
    print(color + border)
    print(f'| {msg} |')
    print(border + Style.RESET_ALL)

def select_program():
    print(Fore.CYAN + "Select the program to run:")
    print("1 - Port Scan Program")
    print("2 - Network Scan Program" + Style.RESET_ALL)
    choice = input(Fore.YELLOW + "Enter your choice (1 or 2): " + Style.RESET_ALL)
    return int(choice)

def select_input_port_scan():
    print("Port Scan Program: Map open ports on a host.")
    host = input(Fore.YELLOW + "Enter the Host (e.g., 192.168.1.1): " + Style.RESET_ALL)
    host = socket.gethostbyname(host)
    port_range = input(Fore.YELLOW + "Enter the Port Range (e.g., 1-65535): " + Style.RESET_ALL)
    return common_input_selection(host, port_range)

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

def select_input_network_scan():
    print("Network Scan Program: Map open ports on a range of network hosts.")
    network = input(Fore.YELLOW + "Enter the IP Range (e.g., 192.168.1.0/24): " + Style.RESET_ALL)
    ip_range = [str(ip) for ip in ipaddress.IPv4Network(network, strict=False)]
    port_range = input(Fore.YELLOW + "Enter the Port Range (e.g., 1-65535): " + Style.RESET_ALL)
    return ip_range, port_range

def common_input_selection(host, port_range):
    timeout = input(Fore.YELLOW + "Enter the Timeout [1sec]: " + Style.RESET_ALL) or 1
    timeout = int(timeout)
    number_threads = input(Fore.YELLOW + f"Enter the Number of Threads [100]: " + Style.RESET_ALL) or 100
    number_threads = int(number_threads)
    show_error_output = input(Fore.YELLOW + "Show Closed Ports? [Y/n]: " + Style.RESET_ALL)
    show_error_output = True if show_error_output.lower() != "n" else False
    port_start_range, port_end_range = map(int, port_range.split("-"))
    port_range = range(port_start_range, port_end_range + 1)
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

def tcp_port_scan_program():
    host, port_range, timeout, number_threads, show_error_output = selectInput()

    for port in port_range:
        queue.put(port)
    
    for t in range(number_threads):
        thread = threading.Thread(target=tcp_port_scanner, args=(host,timeout,show_error_output))
        thread.daemon = True 
        thread.start()

    queue.join()

def network_scan_program():
    print("Network Scan Program: Map open ports on a range of network hosts.")
    network = input(Fore.YELLOW + "Enter the IP Range (e.g., 192.168.1.0/24): " + Style.RESET_ALL)
    ip_range = [str(ip) for ip in ipaddress.IPv4Network(network, strict=False)]

    # Defina as configurações padrão para serem possivelmente sobrescritas pelo usuário
    saved_settings = False
    port_range = None
    timeout = 1
    number_threads = THREADS
    show_error_output = True

    for ip in ip_range:
        print_boxed(f"Scanning IP: {ip}", Fore.YELLOW)
        if not saved_settings:
            port_range_input = input(Fore.YELLOW + "Enter the Port Range (e.g., 1-65535): " + Style.RESET_ALL)
            port_start_range, port_end_range = map(int, port_range_input.split("-"))
            port_range = range(port_start_range, port_end_range + 1)

            timeout = int(input(Fore.YELLOW + "Enter the Timeout [1sec]: " + Style.RESET_ALL) or 1)
            number_threads = int(input(Fore.YELLOW + f"Enter the Number of Threads [{THREADS}]: " + Style.RESET_ALL) or THREADS)
            show_error_output_input = input(Fore.YELLOW + "Show Closed Ports? [Y/n]: " + Style.RESET_ALL)
            show_error_output = True if show_error_output_input.lower() != "n" else False

            save_settings_input = input(Fore.YELLOW + "Save settings for remaining IPs? [Y/n]: " + Style.RESET_ALL)
            saved_settings = True if save_settings_input.lower() != "n" else False

        for port in port_range:
            queue.put(port)
        for t in range(number_threads):
            thread = threading.Thread(target=tcp_port_scanner, args=(ip, timeout, show_error_output))
            thread.daemon = True
            thread.start()
        queue.join()


def main():
    print(Fore.CYAN + "-" * 64)
    print("Welcome to the Port and Network Mapping Tool - Created by Antonio Amaral Egydio Martins")
    print("-" * 64 + Style.RESET_ALL)
    t1 = datetime.now()
    choice = select_program()
    if choice == 1:
        tcp_port_scan_program()
    elif choice == 2:
        network_scan_program()
    else:
        print(Fore.RED + "Invalid choice. Exiting..." + Style.RESET_ALL)
        return
    t2 = datetime.now()
    print_boxed(f"Mapping Completed in {t2 - t1}", Fore.CYAN)

if __name__ == "__main__":
    main()
