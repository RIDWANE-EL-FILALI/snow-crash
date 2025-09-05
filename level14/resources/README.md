# 📜 Level14 Writeup
## Level Overview

**Category**: Binary Exploitation / Anti-Debugging Bypass

**Description**:
We are given the binary `getflag` on the SnowCrash VM. The binary protects itself against debugging by using the `ptrace` system call. When executed under a debugger, `ptrace(PTRACE_TRACEME, ...) `fails (returns `-1` / `EPERM`) and the program exits with a warning:
```
You should not reverse this
```

The challenge: we need to bypass the anti-debugging check to get the flag.

## Observing System Calls
Running `strace` reveals the anti-debugging check:
```
level14@SnowCrash:~$ strace getflag
...
ptrace(PTRACE_TRACEME, 0, 0x1, 0) = -1 EPERM (Operation not permitted)
write(1, "You should not reverse this\n", 28) = 28
exit_group(1)
```
The key line is:
```
ptrace(PTRACE_TRACEME, 0, 0x1, 0) = -1 EPERM
```
This means the binary detects that it is being debugged and exits immediately.

## Disassembly Analysis
```
(gdb) disassemble main
...
0x08048982 <+60>:    call   0x8048540 <ptrace@plt>
0x0804898e <+72>:    test   %eax,%eax
0x08048990 <+74>:    jns    0x80489a8 <main+98>
0x08048992 <+76>:    movl   $0x8048fa8,(%esp)
0x08048999 <+83>:    call   0x80484e0 <puts@plt>
0x0804899e <+88>:    mov    $0x1,%eax
0x080489a3 <+93>:    jmp    0x8048eb2 <main+1388>
...
```
Key points:
* `call ptrace` → result stored in `EAX`.
* `test eax,eax` / `jns` → program checks if `ptrace` succeeded.
* If failed `(EAX < 0)`, prints the anti-debug message and exits.

## Exploitation in GDB
We can bypass the anti-debugging by modifying the return value of ptrace so the program believes it succeeded:
```
gdb getflag
(gdb) catch syscall ptrace
Catchpoint 1 (syscall 'ptrace' [26])
(gdb) command 1
Type commands for breakpoint(s) 1, one per line.
End with a line saying just "end".
>set $eax = 0
>print $eax
>continue
>end
(gdb) b main
Breakpoint 2 at 0x804894a
(gdb) run
```

Explanation:

1. `catch syscall ptrace` → stop when the binary calls `ptrace`.
2. `command 1` → automatically run commands when the catchpoint triggers:
    * `set $eax = 0` → fake the return value of `ptrace` to indicate success.
    * `continue` → resume execution.
3. Break at `main` for further inspection

## Adjusting the UID Check
After bypassing the `ptrace` check, the binary checks some internal value (like UID) before giving the flag. We set it manually:
```
---Type <return> to continue, or q <return> to quit---q
(gdb) break *0x08048b0a
Breakpoint 3 at 0x8048b0a
(gdb) run
Starting program: /bin/getflag
Breakpoint 2, 0x0804894a in main ()
(gdb) continue
Catchpoint 1 (call to syscall ptrace), 0xb7fdd428 in __kernel_vsyscall ()
$1 = 0
Catchpoint 1 (returned from syscall ptrace), 0xb7fdd428 in __kernel_vsyscall ()
$2 = 0

Breakpoint 3, 0x08048b0a in main ()
(gdb) set $eax = 3014
(gdb) c
Continuing.
Check flag. Here is your token: 7QiHafiNa3HVozsaXkawuYrTstxbpABHD8CPnHJ
[Inferior 1 (process 2953) exited normally]
```

* `$eax = 3014` → manually sets the value to satisfy the binary’s internal check.
* Program continues and prints the flag.

## Conclusion
`getflag` uses `ptrace(PTRACE_TRACEME)` to detect debuggers. By:
1. Catching the `ptrace` syscall in GDB.
2. Setting its return value to `0` (pretending the call succeeded).
3. Adjusting `$eax` for the internal UID/validation check.
We bypassed the anti-debug mechanism and retrieved the flag.
```
7QiHafiNa3HVozsaXkawuYrTstxbpABHD8CPnHJ
```
