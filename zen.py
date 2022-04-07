import time
file = open('README.md', 'r')
read = file.read()
splittedRead = read.split('\n')
loop = 0
while True:
    print(splittedRead[loop])
    time.sleep(1)
    loop += 1
    if loop == len(splittedRead):
        loop = 0