# VoiceVLANConfig
Enables only SSH (ensure SSH is working for the script) and then configures a voice vlan, assigns as a voice vlan to an interface if data vlan matches in the function (eg. create voice vlan 10 for access ports that are in the data vlan of 20)

### Ensure you have netmiko and textfsm installed - This has been tested in python 3.7

## You don't really need to configure anything in the python file, but can add your devices (IP addresses) in the devices.txt which should be placed in the same directory as the python script, along with the textfsm regex template that gathers information with the 'show interface switchport' command.
