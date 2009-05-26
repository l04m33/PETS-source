import pygtk
pygtk.require('2.0')
import gtk

from core import model
from core.control import usermng


def make_menu(icon, button, time):

  image_size = gtk.ICON_SIZE_MENU

  menu = gtk.Menu()

  itm_add_prof = gtk.ImageMenuItem('_Add a new profile')
  add_prof_img = gtk.Image()
  add_prof_img.set_from_stock(gtk.STOCK_ADD, image_size)
  itm_add_prof.set_image(add_prof_img)
  #itm_add_prof.connect('activate', btn_add_prof_press, None)
  menu.append(itm_add_prof)

  itm_quit = gtk.ImageMenuItem('_Quit')
  quit_img = gtk.Image()
  quit_img.set_from_stock(gtk.STOCK_QUIT, image_size)
  itm_quit.set_image(quit_img)
  itm_quit.connect('activate', gtk.main_quit)
  menu.append(itm_quit)

  menu.show_all()
  menu.popup(None, None, gtk.status_icon_position_menu, button,
             time, icon)

if __name__ == '__main__':
  notify_icon = gtk.status_icon_new_from_stock(gtk.STOCK_CONNECT)
  notify_icon.connect('popup-menu', make_menu)
  #notify_icon.connect('activate', btn_play_press, None)

  gtk.main()
