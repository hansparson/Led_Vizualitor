import logging
import urllib2 as urllib
import nmap

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

def scanNetwork(network):
    returnlist = []
    nm = nmap.PortScanner()
    a = nm.scan(hosts=network, arguments='-sP')
    for k, v in a['scan'].iteritems():
        if str(v['status']['state']) == 'up':
            try:
                returnlist.append([str(v['addresses']['ipv4']), str(v['addresses']['mac'])])
            except:
                pass
    return returnlist

def getDefaultInterface(returnNet=False):
    def to_CIDR_notation(bytes_network, bytes_netmask):
        network = scapy.utils.ltoa(bytes_network)
        netmask = 32 - int(round(math.log(0xFFFFFFFF - bytes_netmask, 2)))
        net = "%s/%s" % (network, netmask)
        if netmask < 16:
            return None
        else:
            return net
    for network, netmask, _, interface, address in scapy.config.conf.route.routes:
        if network == 0 or interface == 'lo' or address == '127.0.0.1' or address == '0.0.0.0':
            continue
        if netmask <= 0 or netmask == 0xFFFFFFFF:
            continue
        net = to_CIDR_notation(network, netmask)
        if interface != scapy.config.conf.iface:
            continue
        if net:
            if returnNet:
                return net
            else:
                return interface

def getGatewayIP():
    global internetAvail
    try:
        internetAvail = True
        getGateway_p = sr1(IP(dst="google.com", ttl=0) / ICMP() / "XXXXXXXXXXX", verbose=False)
        return getGateway_p.src
    except:
        internetAvail = False
        print("Cannot get gateway as not connected to internet")
        return (raw_input("Enter gateway address manually: "))

def resolveMac(mac):
    try:
        url = "http://macvendors.co/api/vendorname/"
        request = urllib.Request(url + mac, headers={'User-Agent': "API Browser"})
        response = urllib.urlopen(request)
        vendor = response.read()
        vendor = vendor.decode("utf-8")
        vendor = vendor[:25]
        return vendor
    except:
        return "N/A"

defaultInterface = getDefaultInterface()
defaultInterfaceMac = get_if_hwaddr(defaultInterface)
defaultGatewayIP = getGatewayIP()

hostsList = scanNetwork(getDefaultInterface(True))

if internetAvail:
    for i in range(0, len(hostsList)):
        mac = hostsList[i][1]
        hostsList[i].append(resolveMac(mac))

for device in hostsList:
    print device