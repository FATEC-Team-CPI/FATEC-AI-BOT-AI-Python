from pathlib import Path


with open("teste.txt", 'r') as r:
    content = r.read()
    print(Path("teste.txt").suffix)



