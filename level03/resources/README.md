### Level03 Write-up

## Level overview
**Category:** Binary Exploitation / Privilege Escalation

**Description:** Exploit a setuid binary that uses an insecure system call to escalate privileges and retrieve the flag for the next level.
## Analysis

Upon entering this level we find a 32-bit executable named level03 owned by the user `flag03` and the setuid/setgid bits set `-rws` `r-s`, which allows us to  execute it with the same privilage as the `flag03` user .

![alt text](/level03/resources/images/image.png)

Running the program a message gets printed "Exploit me". Challenge accepted.

![alt text](/level03/resources/images/image-1.png)

Let's see the function calls made by this program using `ltrace` 

![alt text](/level03/resources/images/image-2.png)

Looking through the output of `ltrace` we see that the program some instructions : 

- The program calls `geteuid()` to get the effective user ID, then uses `setreuid(geteuid(), geteuid())` and `setregid(geteuid(), geteuid())` to set both the real and effective UIDs/GIDs to the effective UID. This ensures the program runs with flag03 privileges.

>When a binary is setuid, only the effective UID changes to the owner (e.g. flag03), while the real UID stays the same as the user who executed it.

>The problem is that some library calls and shells (like the one spawned by system()) check the real UID and may drop privileges or restrict behavior if real UID ≠ effective UID.
>To avoid this, the program calls:
>setreuid(geteuid(), geteuid());
>setregid(getegid(), getegid());
>This makes the real UID/GID match the effective UID/GID, so the process runs fully as flag03 with no mismatch. Then system("/bin/sh") (or similar) gives a proper privileged shell.

- execute `/usr/bin/env echo` using `system` syscall

The vulnerability lies in the use `/usr/bin/env` before `echo` instead of (`/bin/echo`) u are forcing the `env` command to search for executables in the `PATH` variable in your environment, creating an opportunity for PATH injection.


## Cracking Process

Till now we that the `echo` command is being search in the `PATH` variable to exploit this we can :
- Create our own directory `/tmp/level03`
- Write a simple c program that executes the `getflag` command and named the executable `echo`
- Add the new directory to `PATH` environment variable.


**Exploitation Code** :

```c
#include <stdlib.h>

int main() {

  system("getflag"); 

  return 0;
}
````

**Exploitation Steps** :

![](/level03/resources/images//image.png)

and we got the password for the next level: **qi0maab88jeaj46qoumi7maus**

## Conclusion
This level demonstrates a fundamental security principle: **never trust user-controlled environment variables in privileged programs**

This vulnerability could have been prevented by:
- Using absolute paths: system("/bin/echo") instead of system("/usr/bin/env echo")
- Using execve() with a controlled environment instead of system()
