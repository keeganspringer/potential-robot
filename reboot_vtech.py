# Automate rebooting a Vtech phone using the phones web admin panel

# List of phones to reboot
# This is a list of strings. Must be in single quotes separated with a comma.
# IP address or DNS name is fine as long as it resolves on the system the script
# is being run from.
phone_list = ['192.168.1.48', 'testphone.totaltech.help', '192.168.1.48']

# Login info
# The default values for FreePBX Endpoint Manager are user = 'admin'
# and password = '222222'. If the phone was not configured by the FreePBX
# Endpoint Manager these values will need to be changed.
user = 'admin'
password = '222222'

# Import modules
from requests.auth import HTTPBasicAuth
import requests
import logging

# enable error logging
logging.basicConfig(level=logging.ERROR)

# Create URL for each phone in phone_list. Send reboot request. Timeout after
# 5 seconds.
for i in range(len(phone_list)):
    #Set url for each phone
    url = 'http://' + phone_list[i] + '/servicing_reboot.kl1?do=reboot'
    #Send request to reboot phone
    try:
        requests.post(url, auth=HTTPBasicAuth(user, password), timeout=5)
        logging.info('Rebooted ' + phone_list[i] + '.')
    except requests.exceptions.ConnectionError:
        logging.error('Cannot connect to endpoint ' + phone_list[i] + '.')
        pass
    except requests.exceptions.ConnectTimeout:
        logging.error('Connection timed out for ' + phone_list[i] + '.')
        pass
    except:
        logging.error('Some unknown error occured.')
