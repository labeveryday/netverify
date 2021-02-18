#!/usr/bin/env python
import ipaddress
import os
import re
import subprocess
from tabulate import tabulate


OS_TYPE = os.name


def main():
    """Pings a list of IP Addresses"""
    user_ip_list = input('Enter ip addresses: ').strip(' ')
    port_number = input('Enter port number: ').strip()
    ping_list = create_ip_list(user_ip_list)
    table = []
    for ip in ping_list:
        ping_result = ping_device(ip)
        if ping_result.returncode == 0:
            result_result = check_port(ip, port_number)
            arp = get_arp(ip)
            mac = verify_mac(arp.stdout.decode("utf-8"))
            mac = mac if mac else "Unknown"
            if result_result.returncode == 0:
                table.append([ip, mac, 'up', 'open'])
            else:
                table.append([ip, mac, 'up', 'closed'])
        else:
            table.append([ip, None, 'Down', None])
    print(tabulate(table, headers=["Device IP", "Device MAC", "Up/Down", f"Port {port_number}"]))

def create_ip_list(user_ip_list):
    """Gets the user IP and places it into a list"""
    ip_list = re.findall( r'[0-9]+(?:\.[0-9]+){3}', user_ip_list)
    return verify_ip(ip_list)

def verify_ip(ip_list):
    """Verifies user_input is IP"""
    good_ip = []
    ip_list = ip_list
    for ip in ip_list:
        if ipaddress.ip_address(ip):
            good_ip.append(ip)
    return good_ip

def verify_mac(arp):
    """Finds MAC Address in a string"""
    pattern = '((?:[0-9a-fA-F]:?){12})|([0-9a-z]{4}.){2}[0-9a-z]{4}'\
        '|([0-9A-F]{2}[:-]){5}([0-9A-F]{2})'
    return re.search(pattern, arp).group() if re.search(pattern, arp) else None


def ping_device(ip):
    """Pings a device and returns an object"""
    count = '-n' if OS_TYPE == 'nt' else '-c'
    return subprocess.run(['ping', ip, count, '4'], stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL)

    
def check_port(ip, port_number):
    """Checks for an open port of a device and returns an object"""
    if OS_TYPE == 'nt':
        return subprocess.run(['powershell.exe', 'Test-NetConnection', ip, '-P', port_number],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        return subprocess.run(['nc', '-zv', ip, port_number], stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)

def get_arp(ip):
    """Arps a device to get its MAC Address"""
    return subprocess.run(['arp', ip], capture_output=True)  # May have to add .stdout.decode("utf-8")

if __name__ == "__main__":
    main()