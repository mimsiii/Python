import os
import time

while True:
  print("Prime number")
  time.sleep(0.7)

  x = int(input("Provide a number: "))
  primes = []
  n = 1

  while int(len(primes)) < x:
    n += 1
    found = True

    for num in range(2, n):
      if n % num == 0:
        found = False
        break

    if found == True:
      primes.append(n)

  time.sleep(0.7)
  print(primes[x - 1])
  time.sleep(0.7)

  input("Press any key to continue...")
  os.system('clear')