# sed

```
sed '[condition(s)(optional)] 
[mode(optional)]/[source/to-be-searched pattern(mandatory)]/
[to-be-replaced pattern(depends on mode you use; if no mode then by
 default it is optional)]/[args/flags to operate on the pattern searched
(optional)]'
```

`sed [flags] '[conditions] [mode] / [source] / [dest] / [args]'`

`[mode]` can be either s or y (most common), where s is the substitute mode.
this is the most common mode, and it replaces `dest` with `source`.

`[args]` can be:

- `/g` - every change is global.
- `/i` - case insensitive (can be combined with other flags, like `/gi`)
- `/d` - delete the pattern found (deletes entire line)
- `/p` - prints any matching patterns (duplicates occur if not `-n` flag)
- `/1, /2, /3, /4, ...` - perform ops on nth occurrence of a line.
you can also combine this with g (`/3g`) to do every 3rd occurrence of
the line globally.

`[conditions]` can be a lot of things. For the purposes of this basic guide,
you can do a range `1,3` which takes in all lines from 1 to 3 of the file.

`sed -n '3,5p'` prints the lines in range 3, 5. In this instance, `p` takes 
duplicates of lines 3-5, and `-n` deletes everything except for those
duplicates.

Conversely, `sed '3,5d'` prints everything except for lines 3-5.  

You can also view multiple ranges like this:

`sed -n -e '1,2p' -e '4,5p' -e ...`

This is a command to replace every 2nd and up occurrence of 'a' with 'B':  
(you would do the 2nd only with /2)

`sed 's/a/B/2g'`

`[source]` and `[dest]`: 

### You can make these regex expressions. Yup.

----

There's a lot to learn regarding sed, especially since it can be used in 
tandem with regex to produce some very powerful results. I won't get into that
here though.






