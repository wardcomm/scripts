import sys
# argument = int(500)
drive_size = sys.argv[1]
print(drive_size)
math = 1024 * 1024 * 1024 / 4096
print(math)
answer = int(drive_size) * 4096 * int(math)
print(answer)