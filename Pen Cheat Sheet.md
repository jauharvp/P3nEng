### Check IP based on the interface

```
ip a | grep "<interface>" | grep "inet" | awk '{print $2}'

ip a | grep "eth0" | grep "inet" | awk '{print $2}'

```
