import cmd
import shlex

class ech(cmd.Cmd):
    
    def do_echo(self, arg):
        """echo [parameters] -- print parameters"""
        print(arg)
        
    def do_dump(self, args):
        print(self.dump)
        
    def complete_echo(self, prefix, line, start, end):
        variants = "qwe", "qwa", "qqsdf", "qwulp", "nooo!"
        self.dump = prefix, line, start, end
        return [s for s in variants if s.startswith(prefix)]
        
    def do_quit(self, arg):
        """Quit programm"""
        
    def do_EOF(elf, arg):
        return 1
        
    
ech().cmdloop()
