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
        name, hello = self.monsters[(x, y)]
        if name == "jgsbat":
            print(cowsay.cowsay(hello, cowfile=new_monster))
        else:
            print(cowsay.cowsay(hello, cow=name))


    def do_up(self):
        self.player_coords[1] = (self.player_coords[1] - 1) % 10
        print(f'Moved to {tuple(self.player_coords)}')
        if tuple(self.player_coords) in self.monsters:
            self.encounter(*self.player_coords)

    def do_down(self):
        self.player_coords[1] = (self.player_coords[1] + 1) % 10
        print(f'Moved to {tuple(self.player_coords)}')
        if tuple(self.player_coords) in self.monsters:
            self.encounter(*self.player_coords)


    def do_left(self):
        self.player_coords[0] = (self.player_coords[0] - 1) % 10
        print(f'Moved to {tuple(self.player_coords)}')
        if tuple(self.player_coords) in self.monsters:
            self.encounter(*self.player_coords)

    
    def do_right(self):
        self.player_coords[0] = (self.player_coords[0] + 1) % 10
        print(f'Moved to {tuple(self.player_coords)}')
        if tuple(self.player_coords) in self.monsters:
            self.encounter(*self.player_coords)


    def do_EOF(self, args):
        'End command line'
        return 1
    

    def do_exit(self, args):
        'End command line'
        return 1


if __name__ == '__main__':
    print('<<< Welcome to Python-MUD 0.1 >>>')
    cmdLine().cmdloop()

