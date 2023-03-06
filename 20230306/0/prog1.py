import cmd
from calendar import TextCalendar as tc

class cal(cmd.Cmd):

    def do_prmonth(self, arg):
        """Print a month’s calendar"""
        arg = arg.split()
        tc().prmonth(int(arg[0]), int(arg[1]))
        
    def complete_month(self, prefix, line, start, end):
        return [str(m) for m in range(1, 13) if str(m).startswith(prefix)]
    
    def do_pryear(self, arg):
        """Print the calendar for an entire year"""
        tc().pryear(int(arg))
    
    def do_quit(self, arg):
        """Quit programm"""

cal().cmdloop()

