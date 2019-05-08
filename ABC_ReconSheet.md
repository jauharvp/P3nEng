### Nmap Default port scan ###

nmap -sV -A -oA ```OutPut_File``` ```<IP>```

### Nmap Full port scan ###

nmap -p- -sV -A -oA ```OutPut_File``` ```<IP>```

### Web Scanner using Nikto ###

nikto -host ```<IP/Host>``` --output --Format ```type of output/ html / text```

### Dirs3arch - Directory listing ###

python3 dirs3arch.pu -u ```hostname/ web url``` ----simple-report=```SIMPLEOUTPUTFILE```
