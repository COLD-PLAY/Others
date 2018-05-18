from scapy.all import *

netgateIP = '192.168.1.1'
netgateMAC = 'f4:83:cd:fc:e0:16'
oneplusIP = '192.168.1.103'
oneplusMAC = 'c0:ee:fb:e7:b4:fe'
computerIP = '192.168.1.120'
computerMAC = '80:A5:89:29:B3:91'

# pkt0 = Ether(src=[computerMAC],dst=[oneplusMAC]) \
# 	/ ARP(computerMAC, netgateIP, hwdst=oneplusMAC, pdst=oneplusIP, op=2)
# pkt1 = Ether(src=[computerMAC],dst=[netgateMAC]) \
# 	/ ARP(computerMAC, oneplusIP, hwdst=netgateMAC, pdst=netgateIP, op=2)
# sendp(pkt0, inter=2, iface='eth0')

lan = '113.54.193.0/24'
 
ans, unans = srp(Ether(dst="FF:FF:FF:FF:FF:FF")/ARP(pdst=lan), timeout=5)
for snd, rcv in ans:
	cur_mac = rcv.sprintf("%Ether.src%")
	cur_ip  = rcv.sprintf("%ARP.psrc%")
	print(cur_mac + ' - ' +cur_ip)