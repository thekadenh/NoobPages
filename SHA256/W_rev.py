import numpy as np

test_bits = [1,0,0,0,1,0,1,1,0,1,1,1,0,1,1,0,0,1,0,1,1,0,0,1,1,1,1,1,0,0,0,1]
test_bits2 = [1,1,0,0,1,1,1,1,0,0,1,0,1,1,1,0,1,0,0,1,0,0,1,0,1,1,1,0,0,1,1,0]

test_bits_array = np.asarray(test_bits)
test_bits_array2 = np.asarray(test_bits2)
# Use np.roll for logical right shift

#print(np.roll(test_bits_array, 1))
#print("Init, x3, final")
#print(test_bits_array2)

def sigma_0(a1):
  x1 = np.roll(a1, 7)
  x2 = np.roll(a1, 18)
  x3 = np.roll(a1, 3)
  x3[0:3] = 0
#  print(x3)
  r1 = np.bitwise_xor(x1, x2)
  r2 = np.bitwise_xor(r1, x3)
#  print(r2)
  return r2

def sigma_1(a1):
  x1 = np.roll(a1, 17)
  x2 = np.roll(a1, 19)
  x3 = np.roll(a1, 10)
  x3[0:10] = 0
#  print(x3)
  r1 = np.bitwise_xor(x1, x2)
  r2 = np.bitwise_xor(r1, x3)
#  print(r2)
  return r2

def Usigma_0(a1):
  x1 = np.roll(a1, 2)
  x2 = np.roll(a1, 13)
  x3 = np.roll(a1, 22)
 # x3[0:3] = 0
#  print(x3)
  r1 = np.bitwise_xor(x1, x2)
  r2 = np.bitwise_xor(r1, x3)
#  print(r2)
  return r2

def Usigma_1(a1):
  x1 = np.roll(a1, 6)
  x2 = np.roll(a1, 11)
  x3 = np.roll(a1, 25)
  #x3[0:10] = 0
#  print(x3)
  r1 = np.bitwise_xor(x1, x2)
  r2 = np.bitwise_xor(r1, x3)
#  print(r2)
  return r2

sigma_0(test_bits_array2)

def bits_add(a1, a2):
  carry = 0
  result = [0] * len(a1)
  #print(result)
  for i in range(len(a1) - 1, -1, -1):
    r = carry
    r += a1[i]
    r += a2[i]
    result[i] = (1 if r % 2 == 1 else 0)
    carry = 0 if r < 2 else 1
  print(result)

bits_add(test_bits_array, sigma_0(test_bits_array2))

print(Usigma_1(test_bits_array))

