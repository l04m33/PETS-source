import gtk
from gtk import glade

import sys
import os

fn = sys.argv[1]
ffn = os.path.split(fn)[-1]
ffn = ffn[:-6]

x = glade.XML(fn)
w = x.get_widget(ffn)
w.connect('destroy', gtk.main_quit)
w.show_all()
gtk.main()
