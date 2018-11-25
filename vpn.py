#!/usr/bin/env python

"""
Pick server and start connection with VPNGate (http://www.vpngate.net/en/)

@author Ramachandran K <ramakavanan@gmail.com>
"""

import requests, sys, tempfile, subprocess, base64, time, json

if len(sys.argv) != 2:
    print('usage: ' + sys.argv[0] + ' [country name | country code]')
    exit(1)
country = sys.argv[1]
#country = "India"

if len(country) == 2:
    i = 6 # short name for country
elif len(country) > 2:
    i = 5 # long name for country
else:
    print('Country is too short!')
    exit(1)

try:
    # Here we getting the free vpn server list
    vpn_data = requests.get('http://www.vpngate.net/api/iphone/').text.replace('\r','')
    servers = [line.split(',') for line in vpn_data.split('\n')]
    labels = servers[1]
    labels[0] = labels[0][1:]
    servers = [s for s in servers[2:] if len(s) > 1]
except:
    print('Cannot get VPN servers data')
    exit(1)

desired = [s for s in servers if country.lower() in s[i].lower()]
found = len(desired)
print('Found ' + str(found) + ' servers for country ' + country)
if found == 0:
    exit(1)

supported = [s for s in desired if len(s[-1]) > 0]
print(str(len(supported)) + ' of these servers support OpenVPN')
# We pick the best servers by score
winner = sorted(supported, key=lambda s: float(s[2].replace(',','.')), reverse=True)[0]

print("\n== Best server ==")
pairs = list(zip(labels, winner))[:-1]
for (l, d) in pairs[:4]:
    print(l + ': ' + d)

print(pairs[4][0] + ': ' + str(float(pairs[4][1]) / 10**6) + ' MBps')
print("Country: " + pairs[5][1])

print("\nLaunching VPN...")
_, path = tempfile.mkstemp()

with open(path, 'wb') as f:
    f.write(base64.b64decode(winner[-1]))
    f.write(b'\nscript-security 2\nup /etc/openvpn/update-resolv-conf\ndown /etc/openvpn/update-resolv-conf')


# launching openvpn server with the config of vpngate server information
x = subprocess.Popen(['sudo', 'openvpn', '--config', path])

try:
     #time required to connect the openvpn to connect vpn server
 time.sleep(60)
 start_time = time.time()
 url = "http://bot.whatismyipaddress.com/"
 ret = requests.get(url)
 if ret.status_code == 200:
  with open('resp', "wb") as text_file:
   text_file.write(ret.text)
 print('Time took to check Ip address  ',(time.time() - start_time))
 x.kill()
# termination with Ctrl+C
except Exception as ex:
    try:
        x.kill()
    except:
        pass
    while x.poll() != 0:
        time.sleep(1)
    print('\nVPN terminated')