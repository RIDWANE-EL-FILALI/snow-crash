
# Level 02

**Objective:**  
Analyze the provided `level02.pcap` packet capture file and identify any credentials.

**Analysis:**  
I opened the file in Wireshark and filtered the traffic by following a TCP stream (`Right Click → Follow → TCP Stream`).  
Within the stream, I observed a Telnet login session. Telnet transmits data in plaintext, which allowed me to see the credentials directly.

![](/level02/resources/images/image.png)

**Extracted Credentials:**

Username: levelXX  
Password: ft_wandrNDRelL0L  

**Conclusion:**  
The login information was transmitted without encryption, allowing an attacker to capture the credentials by sniffing the network traffic.
