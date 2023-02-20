import cowsay

monsters = {}
player_coords = [0, 0]


def encounter(x, y):
    cowsay.cow(monsters[(x, y)])


while s := input():
    inp = s.split()
    mv = 0
    if inp[0] == 'up':
        player_coords[1] = (player_coords[1] - 1) % 10
        print(f'Moved to {tuple(player_coords)}')
        mv = 1
    elif inp[0] == 'down':
        player_coords[1] = (player_coords[1] + 1) % 10
        print(f'Moved to {tuple(player_coords)}')
        mv = 1
    elif inp[0] == 'left':
        player_coords[0] = (player_coords[0] - 1) % 10
        print(f'Moved to {tuple(player_coords)}')
        mv = 1
    elif inp[0] == 'right':
        player_coords[0] = (player_coords[0] + 1) % 10
        print(f'Moved to {tuple(player_coords)}')
        move = 1
    elif inp[0] == 'addmon':
        x, y, *hello = inp[1:]
        hello = ' '.join(hello)
        x = int(x)
        y = int(y)
        print(f'Added monster to {(x, y)} saying {hello}')
        if (x, y) in monsters:
            print('Replaced the old monster')
        monsters[(x, y)] = hello

    if mv == 1 and tuple(player_coords) in monsters:
        encounter(*player_coords)


