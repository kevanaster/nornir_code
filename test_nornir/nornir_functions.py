import re
from getpass import getpass
from colorama import Fore

def set_nornir_credential(nr, username=None, password=None):
    """
    Method to establish Nornir credentials
    :param nr: Nornir object to append credentials to
    :param username: username for Nornir object if already defined
    :param password: password for Nornir object if already defined
    """
    if not username:
        username = input("Enter username: ")
    if not password:
        while True:
            password = getpass()
            confirm = getpass("Confirm Password:")
            if password == confirm:
                break
            else:
                print("Password does not match confirm.\n")

    for host_obj in nr.inventory.hosts.values():
        host_obj.username = username
        host_obj.password = password


def menu(task_name):
    """
    Method to create a padded menu for tasks
    Returns padded string for printing. 
    :param task_name: String for task name
    """
    task_name = Fore.GREEN + '==== ' + Fore.RESET + task_name + Fore.GREEN + ' '    
    return '{s:=<60}'.format(s=task_name)


def display_nornir_results(nr_result):
    """
    Method to display task changes and failures
    Prints directly to terminal
    :param nr_result: Nornir MultiResult object
    """
    print(menu('Interface Update'))
    for host in nr_result:
        if not nr_result[host].failed:
            if nr_result[host].changed:
                print(Fore.YELLOW + f'{host}: True')
            else:
                print(Fore.GREEN + f'{host}: False')
        else:
            print(Fore.RED + f'{host}: FAILED')


def configDict(config):
    """
    Method to convert configuration string into dictionary
    returns dictionary of configuration 
    :param config: string object containing configuration
    """
    config_dict = {}
    line_number = 0
    if type(config) == str:
        config_object = config.splitlines()
    else:
        return "ERROR: config not type str"
    for index, line in enumerate(config_object):
        if not bool(re.match("^\s|!", line)):
            line_number = index
            config_dict[line] = []
        elif bool(re.match("^\s", line)):
            config_dict[config_object[line_number]].append(line.strip())
    return config_dict

def diffConfig(current_config, new_config):
    """
    Method to find differences in new_config compared to current_config
    returns dictionary of configuration differences
    :param current_config: dict object containing configuration
    :param new_config: dict object containing new/proposed configuration
    """
    diff = {}
    for parent in new_config:
        # Check for Parent
        if parent in current_config:
            if len(new_config[parent]) != 0:
                for line in new_config[parent]:
                    if line not in current_config[parent]:
                        if parent not in diff:
                            diff[parent] = []
                        diff[parent].append('  ' + line)
                for line in current_config[parent]:
                    if line not in new_config[parent]:
                        if parent not in diff:
                            diff[parent] = []
                        diff[parent].append('  no ' + line)
        else:
            diff[parent] = []
            if len(new_config[parent]) != 0:
                for line in new_config[parent]:
                    if parent not in diff:
                        diff[parent] = []
                    diff[parent].append('  ' + line)
    return diff
