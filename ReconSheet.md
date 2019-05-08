###Nmap Default port scan

nmap -sV -A -oA LightWeigh_Default ```<IP>```

###Nmap Full port scan

nmap -p- -sV -A -oA LightWeigh_Default ```<IP>```

###Web Scanner using Nikto

nikto -host ```<IP/Host>``` --output --Format ```type of output/ html / text``` 
