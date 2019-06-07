from netmiko import ConnectHandler
import os
import textfsm

def turn_on_ssh(ip, username, password, secret):
    telnet_details = {'device_type':'cisco_ios_telnet',
    'ip': ip,
    'username' : username,
    'password' : password,
    'secret' : secret}

    telnet_cmds = ['crypto key gen rsa', 'yes', '2048']

    telnet_session = ConnectHandler(**telnet_details)
    print(telnet_session.enable())
    print(telnet_session.send_config_set(telnet_cmds))

class voiceConfig(object):
    def __init__(self, ip, username, password, port=22, secret=''):
        self.ip = ip
        self.username = username
        self.password = password
        self.secret = secret
        self.port = port

        details = {
                'device_type' : 'cisco_ios',
                'ip' : ip,
                'username' : username,
                'password' : password,
                'port' : port
            }

        if not secret:
            print("Secret has not been configured for the specified device, function may fail...")
        else:
            details['secret'] = secret

        self.ssh_session = self.connect(details)
        self.ssh_session.enable()

    #Establish SSH Session function
    def connect(self, conn_details):
        session = ConnectHandler(**conn_details)
        return(session)

    #Creates VLAN and returns the vlan ID
    def createVlan(self, vlanid, vlanname):
        cmds = ['vlan %s' %(vlanid), 'name %s' %(vlanname)]
        print(self.ssh_session.send_config_set(cmds))
        return(vlanid)

    #Predefined commands to only allow SSH
    def onlyAllowSSH(self):
        cmds = ['line vty 0 15', 'transport input ssh']
        print(self.ssh_session.send_config_set(cmds))

    #This function must meet the following requirements:
    #Voice VLAN will be configured on ports that are both: statically defined as an ACCESS PORT, and match the accesslvan you want it to be configured on (Stops voice vlan being configured on other vlan ports eg like wireless)
    def assign_voicevlan(self, voicevlan, accessvlan):
        data = self.ssh_session.send_command('show interface switchport')
        output = self.textfsm_extractor('show_interface_switchport', data)
        
        ports_config = [] #New list to store our new configuration to be sent over SSH
        print(output)

        for count,interface in enumerate(output):
            if(interface['mode'] == 'static access' and interface['vlan'] == accessvlan): #static access is administratively defined under the interface configuration 'switchport mode access'
                ports_config.append('interface %s' %(interface['interface']))
                ports_config.append('switchport voice vlan %s' %(voicevlan))

        print(self.ssh_session.send_config_set(ports_config))

    #Simple write text file function
    def writeTextFile(_name, _text):
        fileName = ("{0}.txt".format(_name))
        file = open(fileName,'w')

        file.write(_text)
        file.close()

    def textfsm_extractor(self, template_name, raw_text):
        textfsm_data = list()
        fsm_handler = None

        template_path = '{0}.template'.format(template_name)

        with open(template_path) as f:
            fsm_handler = textfsm.TextFSM(f)

            for obj in fsm_handler.ParseText(raw_text):
                entry = {}
                for index, entry_value in enumerate(obj):
                    entry[fsm_handler.header[index].lower()] = entry_value
                textfsm_data.append(entry)
            return(textfsm_data)

username = input("Username: ")
password = input("Password: ")
secret = input("Secret: ")

vlan_voice = input("Input voice vlan: ")
vlan_data = input("Input data vlan to match: ")

if __name__ == "__main__":
    with open('devices.txt','r') as file:
        devices = file.readlines()

        for ip in devices:
            print("Configuring device: " + ip)
            mgr = voiceConfig(ip, username, password, 22, secret)
            mgr.onlyAllowSSH() #Only allow SSH Function
            voice_vlan = mgr.createVlan(vlan_voice,'PY_VOIP') #Create Voice VLAN
            mgr.assign_voicevlan(vlan_voice, vlan_data) #Assign VLAN 80 if interface is in VLAN 130, and is in access mode