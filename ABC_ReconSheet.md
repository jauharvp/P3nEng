### Nmap Default port scan ###

nmap -sV -A -oA ```OutPut_File``` ```<IP>```

### Nmap Full port scan ###

nmap -p- -sV -A -oA ```Output_File``` ```<IP>```

### Web Scanner using Nikto - If Web service is enabled on default or custom port ###

nikto -host ```<IP/Host>``` --output --Format ```type of output/ html / text```

### Dirs3arch - Directory listing - If Web service is enabled on default or custom port ###

python3 dirs3arch.pu -u ```hostname/ web url:port``` ----simple-report=```SIMPLEOUTPUTFILE```
