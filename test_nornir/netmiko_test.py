import netmiko
import logging
from getpass import getpass

username = 'user'
password = getpass()
aruba_template = "templates/aruba_show_switchinfo.textfsm"
devices = ['aruba_lab1']
#logging.basicConfig(filename='netmiko.log', level=logging.DEBUG)
#logger = logging.getLogger("netmiko")


for r in devices:
    router = {'device_type': 'aruba_os',
                'ip': r,
                'username': username,
                'password': password,
                'verbose': False}

    ssh_session = netmiko.ConnectHandler(**router, session_log=f'{r}_session.log')
    output = ssh_session.send_command("show switchinfo", use_textfsm=True, textfsm_template=aruba_template)
    ssh_session.disconnect()
    print(output)
