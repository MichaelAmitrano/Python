#!/usr/bin/env python
# Created 8/15/2021
# Last edited: 8/20/2021
import subprocess
import optparse
import re


# Takes user arguments and parses them.
def get_arguments():
    # Handling user input.
    parser = optparse.OptionParser()    # Creates a new parsing instance.
    parser.add_option('-i', '--interface', dest='interface', help="Interface that you want to change the address on.")
    parser.add_option('-m', '--mac', '--MAC', dest='new_MAC', help="Enter a MAC address that is different from the original.")
    return parser.parse_args()  # Returns parsed input.


# Function that changes the MAC address.
def change_mac(interface, new_mac):
    # Run Linux commands to change the MAC address.
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['ifconfig', interface, 'up'])


# Uses a regular expression (regex) to find the new MAC address within the ifconfig output.
# Please visit 'https://pythex.org/' for more information.
def find_mac(interface):
    results = subprocess.check_output(['ifconfig', interface])  # Runs 'ifconfig {interface}' in the command line.
    mac_regex = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', str(results))  # Searches the output using the regex.

    # Checks to see if there was a MAC address found in the output.
    if mac_regex:
        return mac_regex.group(0)
    else:
        print("Error: could not find MAC.")


# Assigning variables to functions.
(options, arguments) = get_arguments()
current_mac = find_mac(options.interface)

# Main process.
try:
    print(f"Changing MAC address on interface {options.interface} to {options.new_MAC} now...\n")
    change_mac(options.interface, options.new_MAC)  # Executes the function with the parsed arguments.

    # Checks to see if the new MAC matches the old one.
    if current_mac != options.new_MAC:
        print(f"MAC address successfully changed to {options.new_MAC}.")
    else:
        print("The inserted MAC matches the old one, so it was not changed.")

# Error handling.
except TypeError:
    print("Please enter the command correctly, use '--help' for more info."
          "\nExample command: python mac_changer.py -i eth0 -m 00:11:22:33:44:55")
