# Testing stuff for SHA256

Input - `a`

## Buffer

Added buffer makes it 448 bits (512-64), add a 1 and then
add a load of zeros until it hits 448 bits. the 64 bits at the
end is devoted to content length. This is how it works for shorter
strings, which is what I'll be focusing on, but I'd need to reverse
it for longer strings as well if I wanted this to work for bitcoin things.

```
0110000110000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
```

Then, add the buffer size at the end (it's 8 long since it's just a, which
is 01100001 in binary (97 ascii).

```
01100001100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000
```

## Message blocks

In this step, blocks are created. In this case, only block 0 is created,
since there's only one block. This is the same as the previous thing,
so no changes are made.

## Message schedule creation -- blocks 0-15

```
----------------
  message schedule:
  ----------------
  W0  01100001100000000000000000000000
  W1  00000000000000000000000000000000
  W2  00000000000000000000000000000000
  W3  00000000000000000000000000000000
  W4  00000000000000000000000000000000
  W5  00000000000000000000000000000000
  W6  00000000000000000000000000000000
  W7  00000000000000000000000000000000
  W8  00000000000000000000000000000000
  W9  00000000000000000000000000000000
  W10 00000000000000000000000000000000
  W11 00000000000000000000000000000000
  W12 00000000000000000000000000000000
  W13 00000000000000000000000000000000
  W14 00000000000000000000000000000000
  W15 00000000000000000000000000001000

```

This is the same thing as previous, but chopped up into 32-bit chunks.
Again, this is just the raw input but formatted in this way.

## Message schedule creation -- blocks 16-63

There is a recursive function that creates each new block W:

W(X) = $\sigma_1(W(X-2))$ + $W(X-7)$ + $\sigma_0(W(X-15))$ + $W(X-16)$

This gets extremely complicated, extremely quickly.

The $\sigma_0$ function is as follows:

```
def sigma_0(bits):
	x1 = right_circular_rotate(bits, 7) # rotates it right 7 bits, circling
	x2 = right_circular_rotate(bits, 18) # rotates it right 18 bits, circling
	x3 = logical_right_shift(bits, 3) # rightshifts right 3 bits, replacing
	# leftmost bits with zeros
	x4 = XOR(x1, x2)
	answer = XOR(x3, x4)
	return(answer)
```

The XORs look pretty bad, but we can make a simple truth table:

| x1 | x2 | x3 | (x1 ^ x2) ^ x3 |
| ----------- | ----------- | ----------- | ----------- |
| 0 | 0 | 0 | 0 | 
| 0 | 0 | 1 | 1 |
| 0 | 1 | 0 | 1 | 
| 0 | 1 | 1 | 0 |
| 1 | 0 | 0 | 1 | 
| 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 0 | 
| 1 | 1 | 1 | 1 |

Then, we come to the stunning realization that it's only true
if the sum of the three is an odd number (either 1 or 3). Otherwise,
if the sum of the three is even (either 0 or 2) it's false.

The $\sigma_1$ function is as follows:

```
def sigma_1(bits):
	x1 = right_circular_rotate(bits, 17) # rotates it right 17 bits, circling
	x2 = right_circular_rotate(bits, 19) # rotates it right 19 bits, circling
	x3 = logical_right_shift(bits, 10) # rightshifts right 10 bits, replacing
	# leftmost bits with zeros
	x4 = XOR(x1, x2)
	answer = XOR(x3, x4)
	return(answer)
```

This is identical to the $\sigma_0$ function, but they changed the values.

$W(16)$, in this example, would be equal to $W(0)$ because these shift 
functions essentially don't care about zeros, but our original $W(0)$ 
is added and it isn't zero. This is very well demonstrated in the 
github repository with the animations.

`W16 01100001100000000000000000000000`

$W(17)$ is again met with mostly zeros, but the $\sigma_1$ operation 
does actually work on $W(15)$, since it is non-zero (size of 8).
The lone bit is shifted right 17 and 19 times, and when xor'd 
becomes 2 bits. This is added to the rest of the terms (nothing), so
the answer becomes this.

```
x:       00000000000000000000000000001000
ROTR 17: 00000000000001000000000000000000
ROTR 19: 00000000000000010000000000000000 XOR
 SHR 10: 00000000000000000000000000000000 XOR
         --------------------------------
σ1(x):   00000000000001010000000000000000
```

$W(18)$ is zeros except for the $\sigma_1$ function, which is used
on W16. This creates a lot more ones than the other one.

```
x:       01100001100000000000000000000000
         --------------------------------
ROTR 17: 00000000000000000011000011000000
ROTR 19: 00000000000000000000110000110000 XOR
 SHR 10: 00000000000110000110000000000000 XOR
         --------------------------------
σ1(x):   00000000000110000101110011110000

```

It keeps on only using $\sigma_1$ until iteration 22. At this point,
it adds W15 (1000) to the answer.

Then, it keeps using this add until iteration 30, where it finally 
implements $\sigma_0$ on W15. $W(30) = \sigma_1(W(28)) + W(23) + \sigma_0(W(15))$

Then, on iteration 31, it comes full circle and adds in $W(15)$ as well.

This continues until $W(63)$. On every iteration in between, everything 
is used. Technically, it was used on every iteration past $W(15)$, but
since everything was zeros because of my really short input I didn't 
count it.

# Compression

8 "memory registers" are set, with values `a` through `h`.
Initially, these are set to $2^{32} * after\_decimal(\sqrt{\{2, 3, 5, 7, 11, 13, 17, 18\}})$
which are the first primes (in order to get an irrational 
result). This pseudo-randomizes the bits in the initial memory registers.
Note that after_decimal returns all the things after decimal place,
so $\sqrt{2}$ would be not 1.414..., but 0.414...

In decimal:

```
a = 1779033703
  b = 3144134277
  c = 1013904242
  d = 2773480762
  e = 1359893119
  f = 2600822924
  g = 528734635
  h = 1541459225
```

In binary:

```
a = 01101010000010011110011001100111
  b = 10111011011001111010111010000101
  c = 00111100011011101111001101110010
  d = 10100101010011111111010100111010
  e = 01010001000011100101001001111111
  f = 10011011000001010110100010001100
  g = 00011111100000111101100110101011
  h = 01011011111000001100110100011001
```

## Constant generation

We generate 64 constants to assist in compression, from the 
cube roots of the prime numbers, just like the previous example.
I'm not going to go into this too much, but here is an example
of how this works for the first few primes:

```
0  = 01000010100010100010111110011000
1  = 01110001001101110100010010010001
2  = 10110101110000001111101111001111
3  = 11101001101101011101101110100101
4  = 3√11  =   00111001010101101100001001011011
5  = 3√13  =   35133468772075727
6  = 3√17  = 2.571281590658235
```

These are the $K$ values.

## Ch algorithm (choose)

```
def choose(x_bits, y_bits, z_bits):
	# assumes everything is the same length
	for i=0; i<len(x_bits); i++: # bad notation, it's pseudocode anyways
		if(x_bit[i] == 1):
			answer[i] = y_bits[i]
		elif(x_bit[i] == 0):
			answer[i] = z_bits[i]		
```

chooses the y bit if x bit=1, and the z bit if x bit=0.

## Maj algorithm (majority)

Not much to say, takes in 3 inputs. if sum of the bits is 0 or 1, returns 0.
If sum of the bits is 2 or 3, returns 1. Basically returns the majority of the bits.

## $\Sigma_0$ algorithm

```
def Sigma_0(bits):
	x1 = right_circular_rotate(bits, 2) # rotates it right 2 bits, circling
	x2 = right_circular_rotate(bits, 13) # rotates it right 13 bits, circling
	x3 = right_circular_rotate(bits, 22) # rotates it right 22 bits, circling
	x4 = XOR(x1, x2)
	answer = XOR(x3, x4)
	return(answer)
```

## $\Sigma_1$ algorithm

```
def Sigma_1(bits):
	x1 = right_circular_rotate(bits, 6) # rotates it right 6 bits, circling
	x2 = right_circular_rotate(bits, 11) # rotates it right 11 bits, circling
	x3 = right_circular_rotate(bits, 25) # rotates it right 25 bits, circling
	x4 = XOR(x1, x2)
	answer = XOR(x3, x4)
	return(answer)
```

## Compression cont'd

$T_1 = \Sigma_1(e) + Choose(e, f, g) + h + K(n) + W(n)$

$T_2 = \Sigma_0(a) + Maj(a, b, c)$

where n is the iteration.  
Then, it shifts all the resters down once (`b` becomes `a`, `c` becomes
`b`,
etc, `h` becomes `g`) and the information that was once in `a` is lost.  
Then, the following operations are performed.

`a` = $T_1 + T_2$.

`e` = `e` + $T1$.

This repeats 63 more times.

At the very end, the original $H_0$ generated with the square roots is
added to our brand new $H_1$ that we just generated (`a` = `a` from $H_0$
+ `a` from $H_1$, `b` = `b` + `b`, `c` = `c` + `c`, etc.)

This results in $H_1 = H_1 + H_0$ for each letter.

In this case, $H_1$ is the final hash value.

The hash is generated by concatenating
`a, b, c, d, e, f, g, h` together at the very end from $H_1$.






Final output - `ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb`
