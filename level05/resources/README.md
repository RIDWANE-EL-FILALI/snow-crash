# 📜 Level05 Writeup

## Level Overview

**Category:** Privilege Escalation / Cron Job Exploitation

**Description:**

The challenge involves exploiting a scheduled task (cron job) that automatically executes scripts from a specific directory with elevated privileges. This requires understanding Access Control Lists (ACLs), cron job scheduling, and file system permissions to achieve privilege escalation.

## Analysis

### **Initial Investigation**

Upon entering this level, we discover an email file containing information about an automated task:

**Cron Job Configuration:**
```bash
*/2 * * * * su -c "sh /usr/sbin/openarenaserver" - flag05
```

**Cron Schedule Analysis:**

| Field | Value | Meaning |
|-------|--------|---------|
| `*/2` | Every 2 minutes | Minutes field |
| `*` | Every hour | Hours field |
| `*` | Every day | Day of month field |
| `*` | Every month | Month field |
| `*` | Every day of week | Day of week field |
| Command | `su -c "sh /usr/sbin/openarenaserver" - flag05` | Execute script as flag05 user |

✅ **Key Finding:** Script `/usr/sbin/openarenaserver` runs every 2 minutes with `flag05` privileges.

### **Permission Analysis**

Attempting to examine the script reveals interesting permission behavior:

```bash
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

**Access Control Lists (ACL) Analysis:**

| Permission Type | User/Group | Access Rights | Significance |
|----------------|------------|---------------|--------------|
| **user::** | flag05 (owner) | `rwx` | Full read, write, execute |
| **user:level05** | level05 | `r--` | **Special read access granted** |
| **group::** | flag05 group | `r-x` | Read and execute |
| **other::** | All others | `---` | No access |

**ACL Security Implications:**
- **Standard Permissions:** Would normally deny access to `level05` user
- **Extended ACLs:** Grant specific read permissions to `level05`
- **Privilege Context:** Script runs with `flag05` privileges when executed by cron

✅ **Conclusion:** ACLs provide `level05` user with read access to the privileged script.

### **Script Analysis**

Reading the `/usr/sbin/openarenaserver` script reveals its functionality:

```bash
#!/bin/sh

for i in /opt/openarenaserver/* ; do
	(ulimit -t 5; bash -x "$i")
	rm -f "$i"
done
```

**Script Functionality Breakdown:**

| Component | Function | Security Impact |
|-----------|----------|----------------|
| `for i in /opt/openarenaserver/*` | Iterate through all files in directory | **Any file placed here gets executed** |
| `(ulimit -t 5; bash -x "$i")` | Execute in subshell with 5-second limit | Commands run with `flag05` privileges |
| `rm -f "$i"` | Delete file after execution | Evidence cleanup |

**Execution Flow:**
1. **Directory Scan:** Script scans `/opt/openarenaserver/` directory
2. **File Execution:** Each file is executed as a bash script
3. **Privilege Context:** Execution occurs with `flag05` user privileges
4. **Cleanup:** Files are automatically deleted after execution
5. **Timing:** Process repeats every 2 minutes via cron

**Vulnerability Assessment:**
- **Write Access:** If we can write to `/opt/openarenaserver/`, we can inject code
- **Privilege Escalation:** Injected code runs with `flag05` privileges
- **Persistence:** Cron ensures regular execution opportunities

## Exploitation Process

### **Attack Strategy**

The vulnerability lies in the automatic execution of any files placed in `/opt/openarenaserver/` with elevated privileges. We can exploit this by:

1. **Creating a malicious script** that executes `getflag`
2. **Placing it in the monitored directory** `/opt/openarenaserver/`
3. **Waiting for cron execution** (maximum 2 minutes)
4. **Retrieving the output** from our designated location

### **Payload Creation**

We create a simple bash script to retrieve the flag:

**Script: `test.sh`**
```bash
#!/bin/bash
getflag > /var/crash/test.txt
```

**Script Analysis:**
- **Command:** `getflag` - Retrieves the flag for current privilege level
- **Output Redirection:** `> /var/crash/test.txt` - Saves output to accessible file
- **File Location:** `/var/crash/` - Directory with appropriate write permissions

### **Deployment and Execution**

**Step 1: Deploy Payload**
```bash
# Place our script in the monitored directory
cp test.sh /opt/openarenaserver/
```

**Step 2: Wait for Cron Execution**
- **Maximum Wait Time:** 2 minutes (cron interval)
- **Execution Process:** Cron triggers script as `flag05` user
- **Automatic Cleanup:** Original script file is deleted after execution

**Step 3: Retrieve Results**
```bash
# Check the output file
cat /var/crash/test.txt
```

### **Successful Exploitation**

The cron job successfully executes our injected script with `flag05` privileges, and the flag is written to our specified output file.

**Execution Timeline:**
1. **T+0:** Script placed in `/opt/openarenaserver/`
2. **T+≤2min:** Cron job triggers execution
3. **T+≤2min+5sec:** Script execution completes (5-second ulimit)
4. **T+≤2min+5sec:** Output file contains flag
5. **T+≤2min+6sec:** Original script file is deleted

## Conclusion

**Vulnerability Summary:**
This level demonstrates a privilege escalation vulnerability through insecure cron job configuration that automatically executes user-controlled files with elevated privileges.

**Attack Vector Analysis:**

| Component | Vulnerability | Exploitation Method |
|-----------|---------------|-------------------|
| **Cron Job** | Runs with elevated privileges | Leveraged for privilege escalation |
| **Directory Monitoring** | Executes all files in directory | File injection attack vector |
| **File Permissions** | Write access to monitored directory | Payload deployment mechanism |
| **ACL Configuration** | Read access to script source | Information disclosure for analysis |

**Security Lessons:**
1. **Cron Security:** Scheduled tasks should not execute user-controlled content
2. **Directory Permissions:** Monitored directories must have restricted write access
3. **Privilege Separation:** Automated processes should run with minimal privileges
4. **Input Validation:** Scripts should validate content before execution

**Mitigation Strategies:**
- **Restricted Directories:** Use directories with limited write permissions
- **File Validation:** Implement content verification before execution
- **Privilege Dropping:** Execute scripts with reduced privileges
- **Logging and Monitoring:** Track all automated script executions
- **Secure Defaults:** Avoid executing arbitrary files from shared directories

**Attack Classification:** Scheduled Task Privilege Escalation

**Flag Retrieved:** Successfully obtained `flag05` credentials through cron job exploitation.