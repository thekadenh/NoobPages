# Reversing S, in the context of bitcoin

Here's a sample input that generates a bunch of 0s (yoinked from a 
bitcoin thing):

`8b7659f1cf2e92e625b024504d6b4bb706fadcd6266b9919dc9d826a38cf5d2e`

**note**: the 0s in bitcoin are little endian formatted. This means
that although the hash I generated looks like this:

`fb781a1982f2fcb6b60005196f84158b0c201e2e553201000000000000000000`

the actual hash is 

`0000000000000000000132552e1e200c8b15846f190500b6b6fcf282191a78fb`

If you're curious, you can look up this exact hash on the blockchain.
This has 79 zero bits in sequence, which is about the difficulty level you
can expect right now.

For bitcoin, there's 2 stages: first you take the **serialized**
header, and run SHA-256 on it. Then, you take the output of that 
and run another SHA-256 on that specific input. 

There are input restrictions on that though. The first 256 bits 
can be either 0 or 1, and the 257th bit is a 1 (padding) and then
all bits after that up to 512 are zeros, except for 100000000 at
the end, signifying that the content length is 256 bits.

In other words, bits 257-512 of the intermediate hash must be exactly:

```
1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000
```

The intermediate hash is partially known. 

**I want to reiterate that finding some thing that, when run with SHA-256
generates your specific message string that in turn generates zeroes,
is practically impossible by brute-force.**


Anyways, with the logic before,
The values $W(8)$ through $W(15)$ are therefore also known entirely:

```
W8  10000000000000000000000000000000
W9  00000000000000000000000000000000
W10 00000000000000000000000000000000
W11 00000000000000000000000000000000
W12 00000000000000000000000000000000
W13 00000000000000000000000000000000
W14 00000000000000000000000000000000
W15 00000000000000000000000100000000
```

Ideas for solving: 
Matrices? Linear algebra like solving? tracebacks that depend on 
things, a tree-based structure? Ambiguous or quantum bits?

I think I'll make a python script that makes a tree-based diagram
detailing the dependencies of $W(63)$ on $W(62)$ and so on.

For reversing purposes, say for simplicity's sake the last 80 hash 
values must be 0. That is, at the end of H1's computation, the memory
register `f` contains 16 unknowns followed by 16 0s, the register `g`
contains 32 0s, and the register `h` contains 32 0s.

$H0$ is generated with the square roots of prime numbers. $H0$ is the 
same every single time. This means you can derive some of old $H1$.

The "old" $H1$, henceforth referred to as $H1_{old}$ 
must contain this value in the latter 16 bits of `f`, derived from
`10000000000000000 – 0110100010001100`:

`01001011101110100`

Similarly, `g` must be exactly `11100000011111000010011001010101`

and `h` must be exactly `10100100000111110011001011100111`

-----------------
## Recap -- what do we know/control about this hash?

We know $h_{63}, g_{63},$ and the latter half of $f_{63}$.   
We also know $a_{0}, b_{0}, c_{0}, d_{0}, e_{0}, f_{0}, g_{0},$ and $h_{0}$.  
We also know $W(8)$ through $W(15)$, which we cannot change.

We directly control $W(0)$ through $W(7)$, but we **do not know it**.
This is what we have to solve for at the end of the problem.

$W(16)$ through $W(63)$ are generated based off of $W(0)$ to $W(7)$
and $W(8)$ to $W(15)$, so we
indirectly control those, but we **do not know it** because we have to 
solve for $W(0)$ to $W(7)$.

I can't help but think that this is literally just a humongous system of 
equations, with like 64 variables.

Maybe think of the registers a-h as iteration-based instead of register
based (like for recursion)? e.g. $c_2$ = $b_1$ = $a_0$, so we should call them
by the same name. Careful though, because e gets updated. So there would be
two "states" that the thing could be in, a pre-update and a post-update. 
pre-update = $T_1 + T_2$ from iteration $i$, and post-update = pre-update
 + $T_1$ from iteration $i + 4$.

Maybe just call them registers `a` and `b` (for pre/post-update) and have
it store them for their respective iterations? Could do 0-7 for initial, and
8-71 for the rest?

new = old (note that iterations are offset by +3 in order to avoid
negatives in the implementation. In other words, iteration 0 in the old 
version would be iteration 3 in the new one. This changes the K and W
values you have to call.)

$a_3 = a_0, a_2 = b_0, a_1 = c_0, a_0 = d_0$

$b_3 = e_0, b_2 = f_0, b_1 = g_0, b_0 = h_0$

**Then, change the equations from**

$T1_{n} = \Sigma1(e_n) + Ch(e_n, f_n, g_n) + h_n + K_n + W_n$

$T2_{n} = \Sigma0(a_n) + Maj(a_n, b_n, c_n)$

*(note: $T1_{n}$ and $T2_{n}$ are used to calculate the values for 
iteration n+1, using values from iteration n.)*

**To the newer version:**

$T1_{n} = \Sigma1(b_{n}) + Ch(b_{n}, b_{n-1}, b_{n-2}) + b_{n-3} + K_{n-3} + W_{n-3}$

$T2_{n} = \Sigma0(a_n) + Maj(a_n, a_{n-1}, a_{n-2})$

$b_{n+1} = a_{n-3} + T1_n$

$a_{n+1} = T1_n + T2_n$

-------------

This does two things: it makes it easier to understand (you're fetching values
calculated in the previous iterations), and it only requires two arrays:
an $a$ array, and a $b$ array, instead of arrays for all the regs.

Other idea: work way up with example SHA algorithm that only does 2 iterations
of compression and 2 $W$ generations and see how long that takes to reverse

Or just build a dependency tree of the registers and kinda work your way
at it from both sides (top and bottom, since middle is unknown). For example,
the first calculated register $a_1$ in old notation is dependent on everything
in the equation $T_1$ + $T_2$, but everything is already known except for
$W(0)$. So you could say $a_1 = W(0) + C$ where $C$ is a calculated constant.
Then, repeat for $a_2, a_3, e_1, e_2, e_3, ...$ (old notation).

**QUESTION:** can you go backwards? e.g. given $b_{n+1}, b_{n+2}, b_{n+3},
b_{n+4}$ and $a_{n+1}, a_{n+2}, a_{n+3}, a_{n+4}$, could you determine
something about $a_n$ and $b_n$, and $W$?










