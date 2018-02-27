import random
rand = [' ', '-', ' ', ' ',' ', ' ']
level = ['---------------------------------']
for _ in range(1000):
    floors = ['-']
    for a in range(23):
        br = random.choice(rand)
        floors.append(br)
    floors.append('-')
    floor = ''.join(floors)
    level.append(floor)
lf = '+++++++++++++++++++++++++++++++++'
level.append(lf)
print(level)
