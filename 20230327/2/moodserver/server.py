import cowsay
import shlex
import asyncio


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

    def __init__(self, name, host, port):
        self.name = name
        self.host = host
        self.port = port
        self.hero = None
        self.writer = None
        Client.client_list[name] = self

    @staticmethod
    def connect(name, host, port):
        if name in Client.client_list:
            return False

        _ = Client(name, host, port)
        return True

    @staticmethod
    def usr(name):
        if name in Client.client_list:
            return Client.client_list[name]

    @staticmethod
    def disconnect(name):
        if Client.usr(name):
            Client.client_list.pop(name)

    def broadcast(self, msg):
        for _, obj in filter(lambda u: u[0] != self.name, Client.client_list.items()):
            obj.writer.write(msg)


class Hero:
    def __init__(self, x=0, y=0) -> None:
        self.x = x
        self.y = y


class Monster:
    def __init__(self, name, hello_string, hp, x, y):
        self.name = name
        self.message = hello_string
        self.hp = hp
        self.x = x
        self.y = y


class Game:
    ways = {
        "up": (0, 1),
        "down": (0, -1),
        "right": (1, 0),
        "left": (-1, 0),
    }

    def __init__(self, hero):
        self.dungeon = [[None] * 10 for j in range(10)]
        self.hero = hero

    def addmon(self, monster):
        ret_msg = f'Added monster {monster.name} to ({monster.x}, {monster.y}) saying {monster.message}'
        if self.dungeon[monster.x][monster.y]:
            ret_msg = f'Added monster {monster.name} to ({monster.x}, {monster.y}) saying {monster.message}\n Replaced the old monster'

        self.dungeon[monster.x][monster.y] = monster
        return ret_msg

    def encounter(self, x, y):
        if self.dungeon[x][y].name == "jgsbat":
            return [self.dungeon[x][y].message, "jgsbat"]
        else:
            return [self.dungeon[x][y].message, self.dungeon[x][y].name]

    def change_hero_coords(self, way):
        x, y = Game.ways(way)
        self.hero.x = (self.hero.x + x) % 10
        self.hero.y = (self.hero.y + y) % 10

        msg = [f'Moved to ({self.hero.x}, {self.hero.y})']
        if self.dungeon[self.hero.x][self.hero.y] is not None:
            msg += self.encounter(self.hero.x, self.hero.y)
        return msg

    def attack(self, x, y, name, dmg):
        msg = ["No monster here"]
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
            else:
                msg = [f'No {name} here']

        return "\n".join(msg)


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
    server = await asyncio.start_server(echo, "0.0.0.0", 1337)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
