import cowsay
from io import StringIO
import shlex as sh
import cmd

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
        if tuple(self.player_coords) not in self.monsters:
            print("No monster here")
            return
        name, hello, hp = self.monsters[tuple(self.player_coords)]
        if hp <= 10:
            damage = hp
            hp = 0
        else:
            damage = 10
            hp -= 10
        print(f"Attacked {name}, damage {damage} hp")
        if hp == 0:
            print(f"{name} died")
            self.monsters.pop(tuple(self.player_coords))
        else:
            print(f"{name} now has {hp}")
            self.monsters[tuple(self.player_coords)] = (name, hello, hp)


    def do_EOF(self, args):
        'End command line'
        return 1
    

    def do_exit(self, args):
        'End command line'
        return 1


if __name__ == '__main__':
    print('<<< Welcome to Python-MUD 0.1 >>>')
    cmdLine().cmdloop()

