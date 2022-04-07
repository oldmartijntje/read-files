import time
with open('README.md') as file:
    line = file.readline() 
    while line:
        time.sleep(1)
        line = file.readline().strip()
        print(line)