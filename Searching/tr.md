# tr

	tr '[a]' '[b]'

translates all instances of a into b.

	tr '[a-z]' '[A-Z]'
translates all into uppercase.

`-d` deletes the set of characters.  
`-t` concatenates instead of replaces.  
`-s` gets rid of duplicates (Hello would be HELO with
`tr -s '[a-z]' '[A-Z]'`)  
`-c` is an UNO reverse card. When used with `-d`, it deletes
everything but the set of characters.

