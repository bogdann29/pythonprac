import cowsay
import shlex
import asyncio
from random import choice
import threading
from typing import Optional
from time import sleep

WEAPONS = {
    "sword": 10,
    "spear": 15,
    "axe": 20,
}

COMPLETE = {
    "attack": {
        "with": ["sword", "spear", "axe"],
        "": cowsay.list_cows() + ["jgsbat"],
    },
}


class Client:
    client_list = {}

    def __init__(self, name: str, host: int, port: int) -> None:
        self.name = name
        self.host = host
        self.port = port
        self.hero = None
        self.writer = None
        Client.client_list[name] = self

    @staticmethod
    def connect(name: str, host: int, port: int) -> bool:
        if name in Client.client_list:
            return False

        _ = Client(name, host, port)
        return True

    @staticmethod
    def usr(name: str):
        if name in Client.client_list:
            return Client.client_list[name]

    @staticmethod
    def disconnect(name: str) -> None:
        if Client.usr(name):
            Client.client_list.pop(name)

    def broadcast(self, msg: str) -> None:
        for _, obj in filter(lambda u: u[0] != self.name, Client.client_list.items()):
            obj.writer.write(msg)


class Hero:
    def __init__(self, x : int = 0 , y : int = 0) -> None:
        self.x = x
        self.y = y


class Monster:
    monsters = []
    def __init__(self, name: str, hello_string : str, hp : int, x : int, y : int):
        self.name = name
        self.message = hello_string
        self.hp = hp
        self.x = x
        self.y = y
        Monster.monsters.append(self)


class Game:
    ways = {
        "up": (0, 1),
        "down": (0, -1),
        "right": (1, 0),
        "left": (-1, 0),
    }

    def __init__(self, hero : Optional[Client]) -> None:
        self.dungeon = [[None] * 10 for j in range(10)]
        self.hero = hero

    def addmon(self, monster : Optional[Monster]) -> str:
        ret_msg = f'Added monster {monster.name} to ({monster.x}, {monster.y}) saying {monster.message}'
        if self.dungeon[monster.x][monster.y]:
            ret_msg = f'Added monster {monster.name} to ({monster.x}, {monster.y}) saying {monster.message}\n Replaced the old monster'

        self.dungeon[monster.x][monster.y] = monster
        return ret_msg

    def encounter(self, x: int, y: int) -> list:
        if self.dungeon[x][y].name == "jgsbat":
            return [self.dungeon[x][y].message, "jgsbat"]
        else:
            return [self.dungeon[x][y].message, self.dungeon[x][y].name]

    def change_hero_coords(self, way: str) -> str:
        x, y = Game.ways(way)
        self.hero.x = (self.hero.x + x) % 10
        self.hero.y = (self.hero.y + y) % 10

        msg = [f'Moved to ({self.hero.x}, {self.hero.y})']
        if self.dungeon[self.hero.x][self.hero.y] is not None:
            t, n = self.encounter(self.hero.x, self.hero.y)
            msg += cowsay.cowsay(message=t, cow=n)
        return msg

    def attack(self, x: int, y: int, name: str, dmg : int):
        msg = ["No monster here"]
        flag = False
        if isinstance(self.dungeon[x][y], Monster):
            monster = self.dungeon[x][y]

            if monster.name == name:
                if monster.hp < dmg:
                    dmg = monster.hp

                monster.hp -= dmg
                msg = [f'Attacked {monster.name}, damage {dmg} hp']

                if monster.hp == 0:
                    msg += [f'{monster.name} died']
                    self.dungeon[x][y] = None
                else:
                    self.dungeon[x][y].hp = monster.hp
                    msg += [f'{monster.name} now has {monster.hp} hp']
                flag = True
            else:
                msg = [f'No {name} here']

        return "\n".join(msg), flag


def monster_moving(delay : int = 30) -> None:

    dang = Game(None)
    monsters = Monster.monsters

    while True:
        if monsters:
            monster = choice(monsters)
            x, y = monster.x, monster.y

            move = choice(list(Game.ways.items()))
            
            _x, _y = move[1][0], move[1][1]
            nx, ny = (x + _x) % 10, (y + _y) % 10

            if not Game.field[nx][ny]:
                msg = f"{monster.name} moved one cell {move[0]}"
                monster.x, monster.y = nx, ny
                Game.field[nx][ny] = monster
                Game.field[x][y] = None

                for _, obj in Client.client_list.items():
                    obj.writer.write(msg.encode())

                t, n = dang.encounter(*monster.coords)
                msg = cowsay.cowsay(message=t, cow=n)
                for _, obj in filter(
                    lambda u: tuple(u[1].hero.pos) == monster.coords,
                    Client.client_list.items(),
                ):
                    obj.writer.write(msg.encode())

            else:
                continue

        sleep(delay)


async def echo(reader, writer):
    host, port = writer.get_extra_info("peername")

    data = await reader.readline()
    user = data.decode().strip()

    if not Client.connect(user, host, port):
        writer.write(f"Login {user} is already taken.\n".encode())
        print(f"Disconnect {host}:{port}")
        writer.close()
        await writer.wait_closed()
    else:
        client = Client.usr(user)
        client.hero = Hero()
        client.writer = writer

        writer.write(str(Client.usr(user)).encode())
        client.broadcast((f"New user: {user}").encode())

        dungeon = Game(client)

        while not reader.at_eof():
            data = await reader.readline()
            msg = shlex.split(data.decode().strip())
            ans = ""
            print(msg)
            match msg:
                case way if len(way) == 1 and way[0] in Game.ways:
                    ans = "\n".join(dungeon.change_hero_coords(way[0]))
                    writer.write(ans.encode())
                    await writer.drain()

                case ["addmon", *args]:
                    print("Addmon")
                    if len(args) == 8:
                        if args[0] in cowsay.list_cows() or args[0] == "jgsbat":
                            ans = dungeon.add_monster(
                                Monster(args[0],
                                    args[args.index("hello") + 1],
                                    int(args[args.index("hp") + 1]),
                                    int(args[args.index("coords") + 1]),
                                    int(args[args.index("coords") + 2]),
                                        )
                            )
                        print(ans)
                        client.broadcast((client.name + ": " + ans).encode())

                case ["attack", *args]:
                    print("Attack")
                    ans = dungeon.attack(client.hero.x, client.hero.y, args[0], int(args[1]))
                    print(ans)
                    if ans[1]:
                        client.broadcast((client.name + ": " + ans[0]).encode())
                    else:
                        writer.write(ans[0].encode())
                        await writer.drain()

                case ["sayall", *text]:
                    client.broadcast((client.name + ": " + " ".join(text).strip()).encode())

                case ["quit"]:
                    break

                case _:
                    ans = "Error"

        client.broadcast((f"Dissconnect: {client.name}").encode())
        writer.write("Goodbye".encode())
        Client.disconnect(user)
        writer.close()
        await writer.wait_closed()


async def main():
    thrd = threading.Thread(target=monster_moving, args=(30,))
    thrd.start()

    server = await asyncio.start_server(echo, "0.0.0.0", 1337)
    async with server:
        await server.serve_forever()

