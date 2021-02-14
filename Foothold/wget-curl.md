# wget & curl

`wget` and `curl` can both be used to form requests to HTTP and
HTTPS servers, and also to deal with cookies.

## curl

By default, curl sends a get request and sends a raw
response to the terminal.

Important flags:

- `-v` - Verbose. Prints the get request, as well as other
useful information. Add on multiple `v`'s to increase the
verbosity. Good for debugging.
- Do an auth login with `curl http://username:password@xxxx.com/`
or `curl -u username:password -L http://xxxx.com/`
- `-L` - follows redirects.
- Add in `?param=x` to the end of the url in order to send in
parameters.
- `-d` - Does a `POST` request (probably with `-L`).  
```
curl -d 'username=username&password=password' -L http://xxxx.com/login.php
```
- `--cookie-jar` specifies where you want to store the cookies.
Feel free to point this to `/dev/null` unless cookies are
important for some reason. This option makes the subsequent
HTTP requests return the cookies.
	- Saving it to a file with `--cookie-jar cookies.txt`
enables cookies to be reused later with `--cookie cookies.txt`
- `-H` can be used to specify any header type. For example,
`curl -H 'Content-Type: application/json' -d ...` would change
the content type to JSON.
- `-X` specifies the request method (OPTIONS, PUT, DELETE)
are good examples of when this would be used.
	- Use `curl -X OPTIONS http://xxxx.com/` to see if the page
is vulnerable to `PUT` or `DELETE` attacks.
	- Do `curl -X PUT -d @test.txt http://xxxx.com/test.txt`
to upload xxx.txt to a web server. The `@` reads the file.
	- Do `curl -X DELETE http://xxxx.com/test.txt` to delete
the file.




Example of full request (that would have worked for the web
challenge I did on HTB):

```
curl -H 'Content-Type: application/json' -d '{ "username" : "admin", "password" : "password" }' --cookie-jar /dev/null -L  http://inlanefreight.com/login.php
```

