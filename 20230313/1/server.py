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


async def main():
    server = await asyncio.start_server(echo, "0.0.0.0", 1337)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())