# level 00

in this level just like any other ctf
we ran a search for the files owned by the user flag00

using

```
ls -la $(find / -user flag00 2>/dev/null)
----r--r-- 1 flag00 flag00 15 Mar  5  2016 /rofs/usr/sbin/john
----r--r-- 1 flag00 flag00 15 Mar  5  2016 /usr/sbin/john
```

normal search for files owned by that specific user 

after trying the key we got. the kety was denied and after a certain search time searching we found out that the key was encrypted using caecar cypher and wrote a script  
