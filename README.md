# VoiceVLANConfig
Configures the voice vlan, assigns as a voice vlan to an interface if data vlan matches in the function (eg. create voice vlan 10 for access ports that are in the data vlan of 20)

### Ensure you have netmiko and textfsm installed - This has been tested in python 3.7

You don't really need to configure anything in the python file, but can add your devices (IP addresses) in the devices.txt which should be placed in the same directory as the python script, along with the textfsm regex template that gathers information with the 'show interface switchport' command.

## Ensure the following files are in the same directory as the python script:
- devices.txt
- show_interface_switchport.template

## How to use the script

It was designed with in mind to:
1. Change VTY lines to ONLY allow SSH (onlyAllowSSH() function, can be removed from the script)
2. Create VLAN
3. Apply the new vlan created as a voice vlan, on static access ports that only belond to X vlan

Beware, not much handling and checking is implemented, the only check is confirmed if:
A) the port is configured as 'switchport mode access'
B) port belongs to access vlan that you specify when running the script

No information is needed in the script, it will prompt for the following:
- username
- password
- secret
- voice vlan to configure
- data vlan ports to add the 'switchport voice vlan x' command to. (eg. any access port in vlan 100, add voice vlan 101)

## Example in Python
```python
with open('devices.txt','r') as file:
	devices = file.readlines()

    for ip in devices:
        print("Configuring device: " + ip)
        mgr = voiceConfig(ip, username, password, 22, secret)
        voice_vlan = mgr.createVlan(vlan_voice,'PY_VOIP') #Create Voice VLAN
		mgr.assign_voicevlan(vlan_voice, vlan_data)
```
