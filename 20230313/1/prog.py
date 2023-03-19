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

    def do_up(self, args):
        send_recv_serv("up")


    def do_down(self, args):
        send_recv_serv("down")


    def do_left(self, args):
        send_recv_serv("left")

    
    def do_right(self, args):
        send_recv_serv("right")


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
        nm = None
        wpn = "sword"
        match args := sh.split(args):    
            case [name, "with", weapon]:
                if weapon not in WEAPONS:
                    print("Unknown weapon")
                    return
                wpn = weapon
                nm = name
            case [name]:
                nm = name
            case _:
                print("Invalid arguments")
                return
        send_recv_serv(" ".join(["attack", nm, str(WEAPONS[wpn])]))
        

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

