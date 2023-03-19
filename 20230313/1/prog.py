import cowsay
from io import StringIO
import shlex as sh
import cmd
import socket, sys

new_monster = cowsay.read_dot_cow(StringIO("""
$the_cow = <<EOC;
         $thoughts
          $thoughts
    ,_                    _,
    ) '-._  ,_    _,  _.-' (
    )  _.-'.|\\--//|.'-._  (
     )'   .'\/o\/o\/'.   `(
      ) .' . \====/ . '. (
       )  / <<    >> \  (
        '-._/``  ``\_.-'
  jgs     __\\'--'//__
         (((""`  `"")))
EOC
"""))


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



def complete(text, line, begidx, endidx):
    args = sh.split(line)
    if args == ["attack"] or not args[1].startswith("with"):
        key, command = "", "attack"
    elif begidx == endidx:
        key, command = args[-1], 
    else:
        key, command = args[-2], args[0]
    
    return [s for s in COMPLETE[command][key] if s.startswith(text)]


def send_recv_serv(msg):
    s.send((msg + '\n').encode())
    ans = s.recv(1024).decode().strip().replace("'", "")

    if len(tmp := ans.split("\n")) == 3:
        if tmp[1] == "jgsbat":
            print(cowsay(tmp[1], cowfile=new_monster))
        else:
            print(cowsay(ans[1], cow=ans[2]))
    else:
        print(ans)



class cmdLine(cmd.Cmd):
    
    monsters = {}
    player_coords = [0, 0]
    prompt = '>>>'


    def encounter(self, x, y):
        name, hello, hp = self.monsters[(x, y)]
        if name == "jgsbat":
            print(cowsay.cowsay(hello, cowfile=new_monster))
        else:
            print(cowsay.cowsay(hello, cow=name))


    def do_up(self, args):
        self.player_coords[1] = (self.player_coords[1] - 1) % 10
        print(f'Moved to {tuple(self.player_coords)}')
        if tuple(self.player_coords) in self.monsters:
            self.encounter(*self.player_coords)


    def do_down(self, args):
        self.player_coords[1] = (self.player_coords[1] + 1) % 10
        print(f'Moved to {tuple(self.player_coords)}')
        if tuple(self.player_coords) in self.monsters:
            self.encounter(*self.player_coords)


    def do_left(self, args):
        self.player_coords[0] = (self.player_coords[0] - 1) % 10
        print(f'Moved to {tuple(self.player_coords)}')
        if tuple(self.player_coords) in self.monsters:
            self.encounter(*self.player_coords)

    
    def do_right(self, args):
        self.player_coords[0] = (self.player_coords[0] + 1) % 10
        print(f'Moved to {tuple(self.player_coords)}')
        if tuple(self.player_coords) in self.monsters:
            self.encounter(*self.player_coords)


    def do_addmon(self, args):
        args = sh.split(args)
        if len(args) != 8:
            print("Unknown command")
            return
        name = args[0]
        hello = args[args.index("hello") + 1]
        hp = int(args[args.index("hp") + 1])
        x, y = int(args[args.index("coords") + 1]), int(args[args.index("coords") + 2])
        if name not in cowsay.list_cows():
            print("Cannot add unknown monster")
            return
        print(f'Added monster {name} to {(x, y)} with {hp} hp saying {hello}')
        if (x, y) in self.monsters:
            print('Replaced the old monster')
        self.monsters[(x, y)] = (name, hello, hp)


    def do_attack(self, args):
        
        name = "monster"
        weapon = "sword"

        if args := sh.split(args):
            match args:
                case name, _, weapon:
                    name = name
                    weapon = weapon
                case _, weapon:
                    weapon = weapon
                case name:
                    name = name[0]
        
        if weapon not in WEAPONS:
                    print("Unknown weapon")
                    return 0
        
        if name not in cowsay.list_cows() + ["jgsbat"]:
                print("Unknown monster")
                return 0
        
        if tuple(self.player_coords) not in self.monsters:
            print(f"No {name} here")
            return
        name, hello, hp = self.monsters[tuple(self.player_coords)]
        if hp <= WEAPONS[weapon]:
            damage = hp
            hp = 0
        else:
            damage = WEAPONS[weapon]
            hp -= WEAPONS[weapon]
        print(f"Attacked {name}, damage {damage} hp")
        if hp == 0:
            print(f"{name} died")
            self.monsters.pop(tuple(self.player_coords))
        else:
            print(f"{name} now has {hp}")
            self.monsters[tuple(self.player_coords)] = (name, hello, hp)


    def complete_attack(self, text, line, begidx, endidx):
        return complete(text, line, begidx, endidx)


    def do_EOF(self, args):
        'End command line'
        return 1
    

    def do_exit(self, args):
        'End command line'
        return 1

def main():
    print(s.recv(1024).decode().strip())
    cmdLine().cmdloop()


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 1337))
        s.send("Connect\n".encode())
        print('<<< Welcome to Python-MUD 0.1 >>>')
        main()

