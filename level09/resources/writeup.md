# Level09

## Analysis

Entering this level we list files in the directory we found 2 files:
- 32-bit executable owned by `flag09` with suid bit set
- a regular file containing some data

![alt text](/level09/resources/images/directory_listing.png)


outputing the content of the file we can see that it contains displayable/non-displayable characters

![alt text](/level09/resources/images/tokencontent.png)


executing the program without arguments results in message that we should provide one argument

passing `token` file we get a string `tmphr`

![alt text](/level09/resources/images/program_execution.png)



the program doesn't specify that we should pass a file, which means we can try different types of arguments

after some experimentation with the binary we found that the program treats the input as string,  iterates over it and shift each character by a value, the value start with `0` and increment by `1`

hence why the program dislayed `tpmhr` when passing `token`

![alt text](/level09/resources/images/experimentation.png)

Here is a small illustration of how the program works.

![alt text](/level09/resources/images/illustration.png)


looking back at the content `token` , maybe the its content is the ouput of `level09` with a given string


let's try to reverse the content of `token` to get the initial string



## Cracking process

the first problem that we are going encouter is the non displayable character, which are a result of a character being with a value and the result is invalid UTF-8 sequences , which means we can't reshift using the asccii character we need a more consistent data representation like binary or hexadecimal for a more abstract way to represent binary



to represent the content of `token` in hexadecimal we are going to use the `hd` command or `hexdump -C` which displays the output in hex and its ascii representation


![alt text](/level09/resources/images/hexoutput.png)

looking through the output we can see bytes seperated with space and  represented in hex along side an ascii representation.

we're going to store all these bytes in a string exept from the `0a` which represents newline reverse shift using a python script


![alt text](image.png)

running the script we get a proper string : `f3iji1ju5yuevaus41q1afiuq`

we switch to the user `flag09` run `getflag` command and we get the password for the next level: `s5cAJpM8ev6XHw998pRWG728z`

![alt text](/level09/resources/images/flag.png)
