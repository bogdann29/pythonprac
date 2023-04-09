import cowsay
from io import StringIO
import shlex as sh
import cmd
import socket
import sys
import threading
import readline


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


class cmdLine(cmd.Cmd):

    def do_up(self, args):
        s.send(("up\n").encode())

    def do_down(self, args):
        s.send(("down\n").encode())

    def do_left(self, args):
        s.send(("left\n").encode())

    def do_right(self, args):
        s.send(("right\n").encode())

    def do_addmon(self, args):
        args = sh.split(args)
        if len(args) != 8:
            print("Unknown command")
            return
        if args[0] not in cowsay.list_cows():
            print("Cannot add unknown monster")
            return
        msg = 'addmon ' + sh.join(args)
        s.send((msg.strip() + '\n').encode)

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
        s.send((" ".join(["attack", nm, str(WEAPONS[wpn])]) + "\n").encode())

    def do_sayall(self, args):
        message = "sayall " + args + '\n'
        s.send(message.encode())

    def do_EOF(self, args):
        'End command line'
        return 1

    def do_quit(self, args):
        s.send("quit\n".encode())
        self.onecmd("exit")

    def do_exit(self, args):
        'End command line'
        return 1


def get_response():
    while True:
        ans = s.recv(2048).decode()
        if ans:
            if ans.strip() == "Goodbye":
                break

            print("\n" + ans + "\n")
            print(f"\n{cmdline.prompt}{readline.get_line_buffer()}", end="", flush=True)


def main():
    print(s.recv(1024).decode().strip())
    global cmdline
    cmdline = cmdLine()
    game = threading.Thread(target=get_response, args=())
    game.start()
    cmdLine().cmdloop()


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 1337))
        s.send(f"{sys.argv[1]}\n".encode())
        print('<<< Welcome to Python-MUD 0.1 >>>')
        main()
