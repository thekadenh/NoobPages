# HTTP Methods & Codes

## Methods

- `GET` requests a specific resource.
- `POST` Uploads files and sends information to 
websites in the form of binary data.

### Post requests

Potential injection method: If you need to do 
something like an SQL injection and you need to
send something like:

	username=admin&password[$ge]=0

The server won't parse it because of the square 
brackets. So, change the content type to JSON. 
Then, you can send:

	{ "username" : "admin", "password" : {"$ge":"0"} }

This is called a **Content Type Modification Attack.**


- `HEAD` requests the headers that would be returned
if a `GET` request was made to the server. Usually,
this is used to check the length of the server's
response before downloading things from it.
- `PUT` is pretty much the same as post, but
it has a shitton of vulnerabilities if it isn't 
handled correctly. **One might be able to upload
a malicious file onto a server with this**. `PUT`
is disabled by default.

One example of `PUT` being used in this way is this
CTF I did for HTB academy:

*Create a file named "flag.php" with contents ``'<?=`cat /flag.txt`;?>'`` and request it to get the flag.*

I then used burpsuite to send a PUT request 
(although `curl` would have been far easier) and 
then retrieved the file with `wget`. The end 
result was this:

'[flag]'

where [flag] was the flag.

- `DELETE` lets users delete a resource on the 
server. As you might expect, this is catastrophic
without proper handling. `DELETE` is disabled by
default.
- `OPTIONS` returns information about the server,
such as the methods that are accepted by it.
This is a good way to enumerate.

There are more methods, but these are the ones
that one would expect to see most often.

Additionally, `curl` can be used to do all of 
these different types of requests, so you don't
have to use burpsuite.

## Response codes

- 1** - Provides info, continues request
- 2** - Returned when request succeedes
- 3** - Returned when server redirects you
- 4** - Returned when request is bad or server
doesn't know what to do with it
- 5** - Returned when there's a problem with the
server

One thing to note is that some server providers
(AWS, Cloudflare) have implemented their own
custom response codes.