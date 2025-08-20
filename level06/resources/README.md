# Level06

## Analysis

When entring the level we found a `32-bit executable` `leve06` with a setuid bit set as `flag06` which means we need to exploit this binary to execute the `getflag` command

![image showing a list of files in /home/user/level06 directory](image.png)
![image showing the file type a file which results in a 32-bit executable](image-1.png)

accompagning this binary there is also a php script `level06.php` that should be explaining what the binary does

![image of the content of php script](image-2.png)

that's a messy code let's format it so we can understand it better .

![image showing the php code from level06.php](image-8.png)

let's go through this code :

the script takes 2 arguments `$argv[1]` `$argv[2]` which get passed to `fucntion x($y, $z)`

throughout the function `x` the variable `$z` will no be used, so let's focus on `$y`
`$y` get passed to `file_get_contents` which is a built-in PHP function used to read the entire contents of a file into a string meaning that `$argv[1] has to take a file to be read from`


This next line contains `preg_replace()` which is a function in PHP that performs a regular expression search and replace , its searches `subject` for matches to `pattern` and replaces them with `replacement`.
![alt text](image-7.png)
we will only focus on the follwing arguments : `$pattern` `$replacement` `$subject`  
here is a little break of pattern `/(\[x (.*)]\)/e` from [RegExr](https://regexr.com/) : ![alt text](image-4.png)
![alt text](image-5.png)
![alt text](image-6.png)
![](image-3.png)
as shown in the images above the pattern matches `[` and everything `(.*)` after it then matches `]` 
the first and second `()` splits what's matched into capturing groups in our example `Group1 : [x adfasdf]` and `Group2 : asdfadsf`
so which Group will be replaced ?

**\2 regex** 
if we take a closer look at the parameter of the function `"y(\"\\2\")"` `\2` is used for backreferencing. This means it refers to the content matched by the second capturing group in the regular expression so the result will be `"y("asdfasdf")"`

**/e modifer**
`/e` makes the replacement `"y("asdfasdf")"` executed as php code.

I think we found a crack if we can make the replacement as php code we can execute `getflag` as the following 

### Vulnerability

Let's understand more the vulnerability, here are soe code snippets from [Exploiting PHP PCRE Functions](https://www.madirish.net/402) 


this is a normal 
![](image-10.png)
![](image-14.png)


but this will not work because The PCRE (Perl Compatible Regular Expression) engine will prevent straightforward command injection
![alt text](image-12.png)
![alt text](image-13.png)

Using the backtick operators is the perfect solution because PCRE doesn't actually escape these,
![alt text](image-9.png)

## Cracking process

now let's try to simulate the execution of  `level06.php` in our local machine with all the informations that we have gathered 

![alt text](image-16.png)
![alt text](image-17.png)

It didn't work, let's remove the doubel quotes inside `y` and make the parameter takes the replacement like the `strtoupper` example

![](image-15.png)
![alt text](image-18.png)

when removing the double quotes the command worked but why ?

