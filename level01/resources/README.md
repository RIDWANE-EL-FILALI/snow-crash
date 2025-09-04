# 📜 Level01 Writeup

## Level Overview

**Category:** Password Hash Cracking

**Description:**

The challenge requires finding the password for `flag01`. During the filesystem investigation, we examined the `/etc/passwd` file and discovered an unusual configuration: the password hash for `flag01` was directly exposed in the file, which is a legacy practice from older Unix systems.

```bash
level00@SnowCrash:~$ cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/bin/sh
bin:x:2:2:bin:/bin:/bin/sh
sys:x:3:3:sys:/dev:/bin/sh
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/bin/sh
man:x:6:12:man:/var/cache/man:/bin/sh
lp:x:7:7:lp:/var/spool/lpd:/bin/sh
mail:x:8:8:mail:/var/mail:/bin/sh
news:x:9:9:news:/var/spool/news:/bin/sh
uucp:x:10:10:uucp:/var/spool/uucp:/bin/sh
proxy:x:13:13:proxy:/bin:/bin/sh
www-data:x:33:33:www-data:/var/www:/bin/sh
backup:x:34:34:backup:/var/backups:/bin/sh
list:x:38:38:Mailing List Manager:/var/list:/bin/sh
irc:x:39:39:ircd:/var/run/ircd:/bin/sh
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/bin/sh
nobody:x:65534:65534:nobody:/nonexistent:/bin/sh
libuuid:x:100:101::/var/lib/libuuid:/bin/sh
syslog:x:101:103::/home/syslog:/bin/false
messagebus:x:102:106::/var/run/dbus:/bin/false
whoopsie:x:103:107::/nonexistent:/bin/false
landscape:x:104:110::/var/lib/landscape:/bin/false
sshd:x:105:65534::/var/run/sshd:/usr/sbin/nologin
level00:x:2000:2000::/home/user/level00:/bin/bash
level01:x:2001:2001::/home/user/level01:/bin/bash
level02:x:2002:2002::/home/user/level02:/bin/bash
level03:x:2003:2003::/home/user/level03:/bin/bash
level04:x:2004:2004::/home/user/level04:/bin/bash
level05:x:2005:2005::/home/user/level05:/bin/bash
level06:x:2006:2006::/home/user/level06:/bin/bash
level07:x:2007:2007::/home/user/level07:/bin/bash
level08:x:2008:2008::/home/user/level08:/bin/bash
level09:x:2009:2009::/home/user/level09:/bin/bash
level10:x:2010:2010::/home/user/level10:/bin/bash
level11:x:2011:2011::/home/user/level11:/bin/bash
level12:x:2012:2012::/home/user/level12:/bin/bash
level13:x:2013:2013::/home/user/level13:/bin/bash
level14:x:2014:2014::/home/user/level14:/bin/bash
flag00:x:3000:3000::/home/flag/flag00:/bin/bash
flag01:42hDRfypTqqnw:3001:3001::/home/flag/flag01:/bin/bash
flag02:x:3002:3002::/home/flag/flag02:/bin/bash
flag03:x:3003:3003::/home/flag/flag03:/bin/bash
flag04:x:3004:3004::/home/flag/flag04:/bin/bash
flag05:x:3005:3005::/home/flag/flag05:/bin/bash
flag06:x:3006:3006::/home/flag/flag06:/bin/bash
flag07:x:3007:3007::/home/flag/flag07:/bin/bash
flag08:x:3008:3008::/home/flag/flag08:/bin/bash
flag09:x:3009:3009::/home/flag/flag09:/bin/bash
flag10:x:3010:3010::/home/flag/flag10:/bin/bash
flag11:x:3011:3011::/home/flag/flag11:/bin/bash
flag12:x:3012:3012::/home/flag/flag12:/bin/bash
flag13:x:3013:3013::/home/flag/flag13:/bin/bash
flag14:x:3014:3014::/home/flag/flag14:/bin/bash
```

The key observation is the `flag01` entry:
```
flag01:42hDRfypTqqnw:3001:3001::/home/flag/flag01:/bin/bash
```

## Analysis

### **Legacy Password Storage**

**Historical Context:** In older Unix systems, password hashes were stored directly in `/etc/passwd`. This practice was phased out for security reasons, as the passwd file is readable by all users.

**Modern Systems:** Contemporary systems use shadow passwords (`/etc/shadow`) to store hashes with restricted access permissions.

**Security Implications:**
1. **Public Accessibility:** Any user can read `/etc/passwd`, exposing password hashes
2. **Offline Attacks:** Attackers can copy hashes and perform dictionary/brute-force attacks
3. **Weak Hashing:** Legacy systems often used weaker algorithms like DES-based crypt

### **Hash Identification**

The hash `42hDRfypTqqnw` exhibits characteristics of DES-based crypt:

| Property | Value | Analysis |
|----------|--------|----------|
| Length | 13 characters | Standard DES crypt length (2 salt + 11 hash) |
| Character Set | `[a-zA-Z0-9./]` | Classic crypt alphabet |
| Format | No prefix | DES crypt (unlike `$1$` for MD5, `$6$` for SHA-512) |
| Salt | `42` | First 2 characters represent the salt |

✅ **Conclusion:** DES-based crypt hash from legacy Unix system.

### **Cracking Process**

We used John the Ripper with its default wordlist to crack the hash. The process involved:

1. **Hash Extraction:** Save the hash in proper format for John
2. **Algorithm Detection:** John automatically identified it as `descrypt`
3. **Dictionary Attack:** Used built-in wordlist for common passwords

```bash
➜  level01 git:(master) ✗ john flag
Using default input encoding: UTF-8
Loaded 1 password hash (descrypt, traditional crypt(3) [DES 512/512 AVX512F])
Will run 8 OpenMP threads
Proceeding with single, rules:Single
Press 'q' or Ctrl-C to abort, almost any other key for status
Almost done: Processing the remaining buffered candidate passwords, if any.
Proceeding with wordlist:/usr/share/john/password.lst
abcdefg          (?)
1g 0:00:00:00 DONE 2/3 (2025-08-09 15:29) 16.66g/s 750933p/s 750933c/s 750933C/s 123456..perry8
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

**Attack Statistics:**
- **Success Rate:** 1 hash cracked out of 1 (100%)
- **Time:** Less than 1 second
- **Method:** Dictionary attack with wordlist
- **Speed:** ~750,933 passwords/second

## Conclusion

The `flag01` user had their password hash exposed in `/etc/passwd` due to legacy system configuration. The hash used the weak DES-based crypt algorithm, making it vulnerable to rapid dictionary attacks.

**Vulnerability Chain:**
1. **Exposed hash** in publicly readable `/etc/passwd`
2. **Weak algorithm** (DES crypt vs. modern bcrypt/scrypt)
3. **Weak password** found in common wordlists

**Password Cracked:** 
```
abcdefg
```

**Security Lesson:** This demonstrates why modern systems use shadow passwords and stronger hashing algorithms to protect user credentials.
