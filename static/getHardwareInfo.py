import requests
import os
import platform
import wmi

def windows_pc_info():
    username = os.path.basename(__file__)[:-3] # dosyanin adi
    computer = wmi.WMI()
    computer_info = computer.Win32_ComputerSystem()[0]
    os_info = computer.Win32_OperatingSystem()[0]
    proc_info = computer.Win32_Processor()[0]
    gpu_info = computer.Win32_VideoController()[0]

    os_name = os_info.Name.encode('utf-8').split(b'|')[0]
    os_version = ' '.join([os_info.Version, os_info.BuildNumber])
    system_ram = float(os_info.TotalVisibleMemorySize) / 1048576  # KB to GB
    info = {'user': username, 'cpu': format(proc_info.Name), 'ostype' : platform.system(), 'osname': format(os_name)[2:-1], 'gpu': format(gpu_info.Name), 'ram': format(system_ram)}
    return info



if platform.system() == "Windows":
    system_info = windows_pc_info()
# elif platform.system() == "Darwin":

# elif platform.system() == "Linux":

print(str(system_info))

server_ip = 'http://localhost:5000/sysinfoget'
headers = {'Content-Type': 'application/json'}
server_return = requests.post(server_ip, headers=headers, json=system_info)

print (server_return.headers)
#{'date': 'Fri, 05 Jun 2015 17:57:43 GMT', 'content-length': '192', 'content-type': 'text/html', 'server': 'Werkzeug/0.10.4 Python/2.7.3'}