### 1. Nmap Default port scan ###

nmap -sV -A -oA ```OutPut_File``` ```<IP>```

### 2. Nmap Full port scan ###

nmap -p- -sV -A -oA ```Output_File``` ```<IP>```

### 3. Web Scanner using Nikto - If Web service is enabled on default or custom port ###

nikto -host ```<IP/Host>``` --output --Format ```type of output/ html / text```

### 4. Dirs3arch - Directory listing - If Web service is enabled on default or custom port ###

python3 dirs3arch.pu -u ```hostname/ web url:port``` ----simple-report=```SIMPLEOUTPUTFILE```
