import os
import time

while True:
  print("FIZZBUZZ game")
  time.sleep(0.7)

  x = int(input("Provide a number: "))
  time.sleep(0.7)

  for num in range(1, x + 1):
    if num % 3 == 0 and num % 5 == 0:
      print("FIZZBUZZ")
    elif num % 3 == 0:
      print("FIZZ")
    elif num % 5 == 0:
      print("BUZZ")
    else:
      print(num)

  time.sleep(0.7)
  input("Press any key to continue...")
  os.system('clear')