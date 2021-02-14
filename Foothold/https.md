# HTTP vs HTTPS

HTTP is transferred between the client machine and
the server by **cleartext**, whereas HTTPS is transferred 
using an encrypted connection.  
This allows programs like Wireshark to perform a
**MITM** attack on HTTP pages.

HTTP is hosted on port 80 by default.  
HTTPS is hosted on port 443 by default.

The client and server both send a few messages back
and forth, and then a key exchange occurs. This could 
possibly be intercepted.

## HTTP Downgrade attacks
-------------------
These can be performed by downgrading HTTPS connections
to HTTP connections. You set up an MITM and proxy all
traffic through the attacker's host. This results in a 
cleartext data transfer.