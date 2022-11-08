#!/usr/bin/env python3

import os
import re
import subprocess


class MacChanger:
    def __init__(self):
        self.interfaces_dict = {}
        interfaces = os.listdir('/sys/class/net')
        for i in range(0, len(interfaces)):
            self.interfaces_dict[str(i+1)] = interfaces[i]
        self.selected_interface = ""
        self.new_MAC_address = ""

    def show_available_interfaces(self):
        msg = f"Choose interface :"
        for num, interface in self.interfaces_dict.items():
            msg += f"\n{num}. {interface}"
        msg += f"\nInterface [1-{len(self.interfaces_dict)}] >> "
        return msg

    def get_interface(self):
        while True:
            try:
                self.selected_interface = self.interfaces_dict[input(self.show_available_interfaces())]
                return True
            except KeyError:
                print("\n[!] Please select the correct interface number!\n")
                continue
            
    def get_new_MAC_address(self):
        if self.get_interface():
            while True:
                self.new_MAC_address = input(f"Plase enter new MAC address for '{self.selected_interface}' >> ")
                if re.match("([A-Za-z0-9]+(:[A-Za-z0-9]+)+)", self.new_MAC_address):
                    return True
                else:
                    print(f"\n[!] Please enter valid MAC address for interface {self.selected_interface}\n")
 
    def change_MAC_address(self):
        while True:
            if self.get_new_MAC_address():
                try:
                    subprocess.call(["sudo", "ifconfig", self.selected_interface, "down"])
                    subprocess.check_output(["sudo", "ifconfig", self.selected_interface, "hw", "ether", self.new_MAC_address])
                except subprocess.CalledProcessError:
                    print("\n[!] Error. Try to set another MAC address\n")
                    continue

                subprocess.call(["sudo", "ifconfig", self.selected_interface, "up"])
                return True

    def start(self):
        if os.getuid() != 0:
            print("[!] Please launch this script with superuser rights")
        else:
            if self.change_MAC_address():
                print(f"\n[!] MAC address for interface '{self.selected_interface}' successfully changed to {self.new_MAC_address}\n")

MacChanger().start()