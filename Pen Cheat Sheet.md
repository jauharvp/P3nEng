### 1. Check IP based on the interface

```
ip a | grep "<interface>" | grep "inet" | awk '{print $2}'

ip a | grep "eth0" | grep "inet" | awk '{print $2}'

```


### 2. Find out the root owned files in the system


```
find / -user root -perm -4000 -exec ls -ldb {} \;

```

### 3. Find out the files with SUID
```
find / -perm -u=s -type f 2>/dev/null

```


### 4. Check the process running under "root" user.
```
ps aux | grep "root"
ps -ef | grep "root"

```
