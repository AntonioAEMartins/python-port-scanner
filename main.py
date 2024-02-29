from datetime import datetime
import socket
from colorama import Fore, Style, init

# Inspired by: https://westoahu.hawaii.edu/cyber/forensics-weekly-executive-summmaries/writing-a-basic-port-scanner-in-python/

init()  # Initializes Colorama

def print_boxed(msg, color=Fore.GREEN):
    border = '+' + '-' * (len(msg) + 2) + '+'
    print(color + border)
    print(f'| {msg} |')
    print(border + Style.RESET_ALL)

def selectInput():
    print("This program will help you map open ports on a network or host.")
    host = input(Fore.YELLOW + "Enter the Host or Network (e.g., 255.255.255.255): " + Style.RESET_ALL)
    port_range = input(Fore.YELLOW + "Enter the Port Range (e.g., 1-65535): " + Style.RESET_ALL)
    port_start_range, port_end_range = port_range.split("-")
    port_range = range(int(port_start_range), int(port_end_range) + 1)
    return host, port_range

def tcp_port_scanner(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = s.connect_ex((host, port))
        try:
            service_name = socket.getservbyport(port)
        except OSError:
            service_name = "Unknown"
        if result == 0:
            print(Fore.GREEN + f"Port {port} is open, Service Name: {service_name}" + Style.RESET_ALL)
        else :

            print(Fore.RED + f"Port {port} is closed, Service Name: {service_name}" + Style.RESET_ALL)
        s.close()
    except socket.error:
        print(Fore.RED + "Couldn't connect to port {port}" + Style.RESET_ALL)
        return
    except KeyboardInterrupt:
        print(Fore.RED + "You pressed Ctrl+C" + Style.RESET_ALL)
        return

def main():
    print(Fore.CYAN + "-" * 64)
    print("Port Mapping Started - Created by Antonio Amaral Egydio Martins")
    print("-" * 64 + Style.RESET_ALL)
    t1 = datetime.now()
    host, port_range = selectInput()
    for port in port_range:
        tcp_port_scanner(host, port)
    t2 = datetime.now()
    print(Fore.CYAN + f"Mapping Completed in {t2 - t1}" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
