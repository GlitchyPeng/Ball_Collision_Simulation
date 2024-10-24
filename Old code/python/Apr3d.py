import math

n = int(input())
k = int(0)

for i in range(1, n+1):
	k = k + math.factorial(i)

print(k)
