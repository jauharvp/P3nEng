

We have an ideal way to analyse the traffic (egress) from our instance to make our infrastructure cost free. especialy in cloud. Cloud providers charges an amount based on the region and zone.

## So here is the best practice for the analysing traffic.
### Install tcpdump and whois

 ```sudo apt-get update sudo apt-get install tcpdump sudo apt-get install whois
 ```
### Capture 10000 packets with tcpdump and save it to /tmp/nw.cap

```
sudo tcpdump -i eth0 -c 10000 -w /tmp/nw.cap
```
### Parse the capture file and sort hosts by bytes transferred
```
sudo tcpdump -nr /tmp/nw.cap | awk '{print }' | grep -oE '[0-9]{1,}.[0-9]{1,}.[0-9]{1,}.[0-9]{1,}' | sort | uniq -c | sort -n

```

### Look up the ownership of a few IP addresses with whois

```
whois xxx.xxx.xxx.xxx

```
