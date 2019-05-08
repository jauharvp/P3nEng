### 1. Nmap Default port scan ###

nmap -sV -O -A ```<IP>``` -oA ```OutPut_File``` 

### 2. Nmap Full port scan ###

nmap -p- -sV -O -A ```<IP>``` -oA ```Output_File```

### 3. Web Scanner using Nikto - If Web service is enabled on default or custom port ###

nikto -host ```<IP/Host>:port``` --output --Format ```type of output/ html / text```

### 4. Dirs3arch - Directory listing - If Web service is enabled on default or custom port ###

python3 dirs3arch.pu -u ```hostname/ web url:port``` ----simple-report=```SIMPLEOUTPUTFILE```
