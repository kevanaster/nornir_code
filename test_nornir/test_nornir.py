from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result, print_title
from nornir.plugins.tasks.networking import netmiko_send_config, netmiko_send_command
from nornir_functions import set_nornir_credential, display_nornir_results, configDict

def netmiko_show(show_task, title, command_str, textfsm_enable=False, fsmtemplate=None):
    show_task.run(task=netmiko_send_command, command_string=command_str, name=title, textfsm_template=fsmtemplate, use_textfsm=textfsm_enable)


def netmiko_config(config_task, title, config_list):
    config_task.run(task=netmiko_send_config, config_commands=config_list, name=title, config_mode_command="configure terminal")
    

nr = InitNornir("config.yaml")
for key, host in nr.inventory.hosts.items():
    if host.hostname is None:
        host.hostname = key
host = nr.filter(name='aruba_lab1')
set_nornir_credential(host)



print_title("Nornir Test 'Playbook'")

# Get Aruba Info
# results_show = host.run(task = netmiko_show, 
#                     title="Get Interfaces", 
#                     command_str='show run')

# Config Aruba
# results_config = host.run(task = netmiko_config, 
#                     config_list=["interface gigabitethernet 0/0/4", "description nornir_test_success"],
#                     title="Config Interface")


# print_result(results_show)
# conf = configDict(results_show['aruba_lab1'][1].result)
# for key in list(conf):
#     if not key.startswith('interface'):
#         conf.pop(key, None)

# config_update = {}
# for key, val in conf.items():
#     if 'port-channel' in key:
#         for item in conf['key']:
#             if item.startswith('trusted vlan'):
#                 if '1-4094' not in item:

#             if '200' not in 
        
#print_result(results_config)

# print_title("Changed Items")
# display_nornir_results(results_config)
