# 📜 Level13 Writeup
## Level Overview

**Category:** Binary Exploitation / Reverse Engineering

**Description:**  
We are given a binary `level13` on the SnowCrash VM. When executed, the program checks the current user’s UID using `getuid()`. If the UID matches `4242`, it runs a hidden function (`ft_des`) that reveals the flag. Otherwise, it prints an error and exits.

The challenge: **our actual UID is 2013, not 4242.**  
We must trick the program into believing our UID is `4242`.

---

## Observing System Calls

Before disassembling, we can observe the binary’s system calls using `ltrace`:

```bash
level13@SnowCrash:~$ ltrace ./level13
__libc_start_main(0x804858c, 1, 0xbffff7f4, 0x80485f0, 0x8048660 <unfinished ...>
getuid()                                                                    = 2013
getuid()                                                                    = 2013
printf("UID %d started us but we we expe"..., 2013UID 2013 started us but we we expect 4242
)                         = 42
exit(1 <unfinished ...>
+++ exited (status 1) +++
```

## The Binary Behavior

Running the binary:

```bash
level13@SnowCrash:~$ ./level13
UID 2013 started us but we expect 4242
```
The program terminates because the check fails.

## Disassembly Analysis
Switch GDB to Intel syntax for easier reading:
```
(gdb) set disassembly-flavor intel
(gdb) disassemble main
```

Output (excerpt):
```
0x08048595 <+9>:     call   0x8048380 <getuid@plt>
0x0804859a <+14>:    cmp    eax,0x1092       ; compare eax with 4242
0x0804859f <+19>:    je     0x80485cb        ; if equal, jump to success
```

Key points:

* `call getuid` → result stored in `EAX.`
* `cmp eax, 0x1092` → checks if UID == `4242`.
* If equal → jump to the success branch (`ft_des`).
* Otherwise → program calls `printf` and `exit`.

📌 Conclusion: If we can modify `EAX` to `4242` right after the `getuid` call, the program will take the success path.


## Exploitation in GDB

Here’s the full session:
```
level13@SnowCrash:~$ gdb ./level13
GNU gdb (Ubuntu/Linaro 7.4-2012.04-0ubuntu2.1) 7.4-2012.04
...
Reading symbols from /home/user/level13/level13...(no debugging symbols found)...done.
(gdb) set disassembly-flavor intel
(gdb) disassemble main
Dump of assembler code for function main:
   0x0804858c <+0>:     push   ebp
   0x0804858d <+1>:     mov    ebp,esp
   0x0804858f <+3>:     and    esp,0xfffffff0
   0x08048592 <+6>:     sub    esp,0x10
   0x08048595 <+9>:     call   0x8048380 <getuid@plt>
   0x0804859a <+14>:    cmp    eax,0x1092
   0x0804859f <+19>:    je     0x80485cb <main+63>
   ...
End of assembler dump.
(gdb) break *0x0804859a
Breakpoint 1 at 0x804859a
(gdb) run
Starting program: /home/user/level13/level13

Breakpoint 1, 0x0804859a in main ()
(gdb) print $eax
$1 = 2013
(gdb) set $eax = 4242
(gdb) continue
Continuing.
your token is 2A31L79asukciNyi8uppkEuSx
[Inferior 1 (process 2934) exited with code 050]
```

## Conclusion

The binary relies on a UID check via `getuid()`.
By disassembling, we found where the program compares `EAX` against `4242`.
Using a breakpoint, we stopped execution before the check, changed `EAX` from `2013` to `4242`, and continued.
This bypassed the UID check and revealed the flag.

Final Flag:
```
2A31L79asukciNyi8uppkEuSx
```