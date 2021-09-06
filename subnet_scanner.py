#!/usr/bin/env python
# Created 8/20/2021
# Last edited: 9/5/2021
import argparse
import scapy.all as scapy


# Takes user arguments and parses them.
def get_arguments():
    parser = argparse.ArgumentParser()  # Creates a new parsing instance.
    # Handling user input.
    parser.add_argument('--ip', dest='ip', help="Enter IP address with subnet mask.")
    return parser.parse_args()


# Function that creates ARP request and uses it on a specified IPv4 address.
def scan(ip):
    arp_request = scapy.ARP(pdst=ip)  # Variable that contains an instance of an ARP packet. 'pdst' sets field to IP.
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')  # Variable that contains an instant of an Ethernet frame for the broadcast address.
    arp_request_broadcast = broadcast / arp_request  # Combines the ARP packet and frame type.
    answered_list = scapy.srp(arp_request_broadcast, timeout=1)[0]  # Sends packets and stores any responses/answers.

    # Iterates through the ARP responses and displays the second element of the response.
    client_list = []  # Creates a list.
    for each_element in answered_list:
        client_dict = {"IP Address": each_element[1].psrc, "MAC Address": each_element[1].hwsrc}  # Creates dictionary.
        client_list.append(client_dict)  # Creates a list of dictionaries.
        return client_list


# Prints desired results and handles errors.
def print_results(results_list):
    print("\nIP Address\t\tMAC Address\n-----------------------------------------")  # Header.
    if results_list is not None:  # If the list has content execute.
        for every_client in results_list:
            print(f"{every_client['IP Address']}\t\t{every_client['MAC Address']}")
    else:
        print("\nIncorrect IP address entered, please enter the IP with it's subnet mask. Ex: 192.168.1.0/24")


options = get_arguments()
scan_results = scan(options.ip)
print_results(scan_results)
