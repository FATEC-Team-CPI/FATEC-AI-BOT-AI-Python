import os 

with open("arquivo.txt") as doc:
    print(os.path.getsize("arquivo.txt"))