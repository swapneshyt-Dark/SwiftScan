# **Fast Port Scanner**

>Simple port scanner, for times when you can't use nmap. There are times, lets say in red teaming where use of traditional tools has been blocked. During such times we can use our own coded tools.

# **Usage**
```
 
             A simple, fast, lightweight port scanner.
 

Usage: Fast_Port_Scanner.py [targets] [ports] 

positional arguments:
  
1.     host        [target ip]
2.     port        [port] 
          
optional arguments:                                                                                                                                                            
     -h, --help  show this help message and exit

Examples:
    
1.   Fast_Port_Scanner.py github.com 1-10000
2.   Fast_Port_Scanner.py github.com 85-1050
3.   Fast_Port_Scanner.py github.com 23-443
4.   Fast_Port_Scanner.py github.com all     ==>  all= 1-65535
5.   Fast_Port_Scanner.py github.com [NONE]  ==>  Default = 1-1000
```

# **Required Library**
- pyfiglet
```
pip install pyfiglet 
```
- sockets
```
pip install sockets
```
- threaded
```
pip install threaded
```
- futures
```
pip install futures
```
- DateTime
```
pip install DateTime
```
- argparse
```
pip install argparse
```
# **Installing Fast Port Scanner**(Linux)
```
[git clone https://github.com/swapneshyt-Dark/SwiftScan.git
```
