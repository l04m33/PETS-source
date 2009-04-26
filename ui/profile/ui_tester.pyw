import gtk
from gtk import glade

x = glade.XML('LoginForm.glade')
w = x.get_widget('LoginForm')
w.connect('destroy', gtk.main_quit)
w.show_all()
gtk.main()
