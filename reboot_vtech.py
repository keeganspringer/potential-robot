# Automate rebooting a Vtech phone using the phones web admin panel

# This script requires the python requests and requests.auth modules. They are
# not installed by default on FreePBX 15 using the FreePBX distro. Install pip
# with 'yum install python36u-pip.noarch'. Then install the modules with
# 'pip3.6 install requests requests.auth'.

# List of phones to reboot
# This is a list of strings. Must be in single quotes separated with a comma.
# IP address or DNS name is fine as long as it resolves on the system the script
# is being run from. Leave blank if not used.
phone_list = ['testphone.example.com',
              '10.11.12.13']

# Network to reboot.
# This is also a list of strings. The script will generate a list of all IPs in
# the subnet to reboot from the network address in CIDR notation. Leave blank if
# not used.
phone_list_network = ['10.0.0.0/29']

# Login info
# The default values for FreePBX Endpoint Manager are user = 'admin'
# and password = '222222'. If the phone was not configured by the FreePBX
# Endpoint Manager these values will need to be changed.
user = 'admin'
password = '222222'

# Import modules
from requests.auth import HTTPBasicAuth
import requests
import ipaddress
import logging

# enable error logging
logging.basicConfig(level=logging.ERROR)

# Create a list of IPs for the subnet
if phone_list_network:
    network_object = ipaddress.ip_network(phone_list_network[0])
    phone_list_network = list(network_object.hosts())
    for i in range(len(phone_list_network)):
        phone_list_network[i] = str(ipaddress.IPv4Address(phone_list_network[i]))

# Create URL for each phone in reboot_list. Send reboot request. Timeout after
# 2 seconds.
def reboot_phone(reboot_list):
    for i in range(len(reboot_list)):
        #Set url for each phone
        url = 'http://' + reboot_list[i] + '/servicing_reboot.kl1?do=reboot'
        #Send request to reboot phone
        try:
            requests.post(url, auth=HTTPBasicAuth(user, password), timeout=2)
            logging.info('Rebooted ' + reboot_list[i] + '.')
        except requests.exceptions.ConnectionError:
            logging.error('Cannot connect to endpoint ' + reboot_list[i] + '.')
            pass
        except requests.exceptions.ConnectTimeout:
            logging.error('Connection timed out for ' + reboot_list[i] + '.')
            pass
        except:
            logging.error('Some unknown error occured.')

# Run function to reboot phones for the list(s) that are set.
if phone_list:
    reboot_phone(phone_list)
if phone_list_network:
    reboot_phone(phone_list_network)
