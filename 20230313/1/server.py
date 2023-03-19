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

class Hero:
    def __init__(self, x = 0, y = 0) -> None:
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
    
    player = Hero()
    dungeon = Game(player)

    while not reader.at_eof():
        data = await reader.readline()
        msg = shlex.split(data.decode().strip())
        ans = ""
        print(msg)
        match msg:
            case way if len(way) == 1 and way[0] in Game.ways:
                ans = "\n".join(dungeon.change_hero_coords(way[0]))

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
                ans = dungeon.attack(player.x, player.y, args[0], int(args[1]))

            case ["Connect"]:
                ans = "<<< Welcome to Python-MUD 0.1 >>>"

            case _:
                ans = "Error"

        writer.write(ans.encode())
        await writer.drain()
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(echo, "0.0.0.0", 1337)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())