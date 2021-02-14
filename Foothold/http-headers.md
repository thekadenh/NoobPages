# HTTP Headers

HTTP headers can be split into 5 groups.

## General Headers
These headers describe the message. They're
not particularly meaningful, but they provide
key information to the server.  
Some examples of general headers are:

```
Date: Sun, 06 Aug 2020 08:49:37 GMT
Connection: keep-alive
```

[More about general headers](https://www.w3.org/Protocols/rfc2616/rfc2616-sec4.html)

## Entity Headers
These headers are used to describe what content
is being transferred.  
Example:

```
Content-Length: 26012
Content-Type: text/html; charset=ISO-8859-4
Content-Encoding: gzip
```

[More about entity headers](https://www.w3.org/Protocols/rfc2616/rfc2616-sec7.html)

## Request Headers

Request headers are what the client sends in an
HTTP request. These detail what the server needs
to know about the client in order to provide
a good response.

Example:

```
Host: www.inlanefreight.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko)
Cookie: cookie1=298zf09hf012fh2; cookie2=u32t4o3tb3gg4
Accept: text/plain
Referer: https://www.hackthebox.eu/
Authorization: BASIC cGFzc3dvcmQK
```

[More about request headers](https://tools.ietf.org/html/rfc7231#section-5)

## Response Headers

Response headers, as you would expect, are used
in the server's response (doesn't relate to 
message content).

Example:

```
Server: Apache/2.2.14 (Win32)
Set-Cookie: name1=value1,name2=value2; Expires=Wed, 09 Jun 2021 10:18:14 GMT
WWW-Authenticate: BASIC realm="localhost"

```

**NOTE**: the **`Server`** field is used by programs 
such as `nmap` in order to enumerate the server.
Additionally, the The **`WWW-Authenticate`** header
notifies the client about the type of authentication
required to access the requested resource.

[More about response headers](https://tools.ietf.org/html/rfc7231#section-6)

## Security Headers

These headers, which are ***the most important headers***,
help servers deal with various attacks. But, it also
gives the users valuable info, and even could help
enumerate possible attack vectors.

Example:

```
Content-Security-Policy: script-src 'self'
Strict-Transport-Security: max-age=31536000
Referrer-Policy: origin
```

`Content-Security-Policy` is, in short, the website's
policy regarding externally injected resources. 
This means javascript, .sh, and other resources.
This helps prevent cross-site-scripting attacks.

***If this is missing or changed, consider doing a
cross-site scripting attack.***

`Strict-Transport-Security` is how the browser
prevents you from using HTTP (instead of HTTPS).

`Referrer-Policy` is how the browser avoids 
accidentally disclosing potentially compromising or
sensitive URLs while someone browses the website.

[More about security headers (CLICK!)](https://owasp.org/www-project-secure-headers/)

