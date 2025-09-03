# 📜 Level03 Writeup

## Level Overview

**Category:** Binary Exploitation / PATH Hijacking

**Description:**

The challenge requires exploiting a binary executable to gain elevated privileges and execute commands as the `flag03` user. This involves understanding SUID permissions and PATH environment variable manipulation.

## Analysis

### **Initial Investigation**

Upon entering this level, we discover a 32-bit executable named `level03` with specific ownership and permissions:

![information about the file using ls -la command](/level03/resources/images/permissions.png)

**File Properties:**
- **Owner:** `flag03` user
- **Permissions:** `-rws` (SUID bit set)
- **Significance:** Executable runs with `flag03` privileges regardless of who executes it

![type of the file using file command](/level03/resources/images/type.png)

**Binary Analysis:**
- **Architecture:** 32-bit ELF executable
- **Platform:** Linux x86 architecture
- **Compilation:** Standard C executable format

### **Runtime Behavior**

Executing the program reveals its basic functionality:

![output of the binary when executed](/level03/resources/images/output.png)

**Execution Results:**
- **Output:** "Exploit me"
- **Behavior:** Simple message display
- **Challenge:** The message itself suggests vulnerability analysis is required

### **Dynamic Analysis with ltrace**

Using `ltrace` to trace library calls reveals the program's internal operations:

![output of function calls of level03 binary with ltrace](/level03/resources/images/ltrace.png)

**Key Findings:**
- **System Call:** `system("/usr/bin/env echo Exploit me")`
- **Command Path:** Uses `/usr/bin/env` to locate `echo`
- **Vulnerability:** PATH-dependent command resolution

### **Vulnerability Analysis**

**PATH Hijacking Vulnerability:**

| Component | Analysis | Security Impact |
|-----------|----------|----------------|
| `/usr/bin/env` | Searches PATH for `echo` command | Allows custom binary substitution |
| `system()` call | Executes shell commands | Inherits SUID privileges |
| PATH dependency | Dynamic command resolution | Controllable by user environment |

**Attack Vector:**
1. `/usr/bin/env` searches directories in `PATH` environment variable
2. First matching `echo` binary is executed
3. Custom `echo` can be placed earlier in PATH
4. Malicious `echo` executes with `flag03` privileges

✅ **Conclusion:** Classic PATH hijacking vulnerability in SUID binary.

## Exploitation Process

### **Step 1: Create Malicious Binary**

We create a custom `echo` replacement that executes the desired command:

```c
#include <stdlib.h>

int main() {
   system("getflag");
   return 0;
}
```

**Code Analysis:**
- **Purpose:** Replace legitimate `echo` command
- **Payload:** Executes `getflag` to retrieve flag
- **Privilege:** Inherits SUID permissions from caller

### **Step 2: Compile the Exploit**

```bash
gcc -o echo echo.c
```

**Compilation Details:**
- **Output:** Custom `echo` binary
- **Location:** Current working directory
- **Functionality:** Executes `getflag` instead of echoing text

### **Step 3: Modify PATH Environment**

```bash
PATH=/path_to_our_echo:$PATH
```

**PATH Manipulation:**
- **Strategy:** Prepend custom directory to PATH
- **Effect:** Our `echo` is found before system `echo`
- **Result:** `/usr/bin/env echo` executes our malicious binary

### **Step 4: Execute the Exploit**

Running the `level03` binary now triggers our PATH hijacking attack:

![output of the binary exploited showing the password](/level03/resources/images/password.png)

**Exploitation Success:**
- **Trigger:** Execute original `level03` binary
- **PATH Resolution:** Custom `echo` is located and executed
- **Privilege Escalation:** Code runs with `flag03` permissions
- **Result:** Flag is successfully retrieved

## Conclusion

**Vulnerability Summary:**
The `level03` binary contained a classic PATH hijacking vulnerability due to its use of `/usr/bin/env` within a SUID context, allowing attackers to substitute legitimate system commands with malicious alternatives.

**Attack Chain Analysis:**

| Stage | Action | Technical Detail |
|-------|--------|-----------------|
| **Discovery** | Identify SUID binary | `-rws` permissions with `flag03` ownership |
| **Analysis** | Trace system calls | `ltrace` reveals PATH-dependent execution |
| **Exploitation** | Create malicious binary | Custom `echo` that executes `getflag` |
| **Deployment** | Modify PATH variable | Prepend custom directory to hijack resolution |
| **Execution** | Trigger vulnerability | Run original binary with modified environment |

**Security Lessons:**
1. **SUID Risks:** Elevated privilege binaries require careful PATH handling
2. **Absolute Paths:** Use full paths instead of relying on PATH resolution
3. **Environment Security:** Don't trust user-controlled environment variables
4. **Code Review:** Dynamic command execution in privileged contexts is dangerous

**Mitigation Strategies:**
- Use absolute paths for all system commands
- Sanitize environment variables in SUID programs
- Avoid `system()` calls in privileged executables
- Implement proper input validation and command construction

**Flag Retrieved:** Successfully obtained `flag03` credentials through PATH hijacking exploitation.