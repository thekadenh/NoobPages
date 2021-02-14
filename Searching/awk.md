# awk

	awk [flags] [select pattern/find(sort)/commands] [input file]

Alternatively, if you have an `awk` script, you can do this:

	awk -f script.awk input.txt

To search for a pattern (same as `grep`), you do this:

	awk '/pattern/' input.txt

`-F` specifies a field separator (same thing as `FS="x"` in the 
`Begin` statement)  
`-v` specifies variables (not quite sure how it's used)  
`-D` is for debugging `awk` scripts.  
`-o` specifies the output file of `awk` (defaults to `awkprof.out`)

Built-in variables include field variables (\$1, \$2, \$3 .. \$n). 
These field variables are used to specify a piece of data 
(data separated by a delimeter defaulting to space). \$0 is the variable
for each line.

You can specify the delimiter by using `'BEGIN{FS="x"}...`, where x is
the new delimiter.

The variable `NR` is the current line count. For example,
 `awk '{print NR,$0}'`
would print the line number followed by the line itself.

By default, `awk` separates rows with \n. To customize this, do
`'BEGIN{RS="x"}...`, 
where x is the new row separator.

Specify a delimiter when outputting using `'BEGIN{OFS="x"}...`. This 
changes the spaces to whatever you want.

The actual script consists of `'BEGIN{...} {...} END{...}'` where begin and
end are optional.

Example of a "full" command:

	awk "BEGIN {FS='o'} {print $1,$3} END{print 'Total Rows=',NR}"

There are obviously more things you can do with `awk`, but these are
the basics.

