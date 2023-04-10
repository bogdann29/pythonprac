import sys
import os 
import gettext

popath = os.path.join(os.path.dirname(__file__), "po")
translation = gettext.translation("prog", popath, fallback=True)
_, ngettext = translation.gettext, translation.ngettext

while s := sys.stdin.readline():
    print(_("Entered {} word(s)").format(len(s.split())))
