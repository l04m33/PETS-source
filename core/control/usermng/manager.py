import os
from os import path
import db
from db import cpool
from db import support as supp
from core.model import Profile


class CannotDeleteCurrentProfileError(Exception):
  pass


class ProfileManager:

  def __init__(self, prof_dir):
    self.__cur_prof = None
    self.__prof_dir = prof_dir

  def add_profile(self, profile):
    profile._check_integrity()
    profile.db_fname = path.join(self.__prof_dir, profile.id)
    supp.gen_db(profile.db_fname)
    self.set_cur_profile(profile)
    profile.save()

  def del_profile(self, profile):
    cprof = self.get_cur_profile()
    if profile.id == cprof.id:
      raise CannotDeleteCurrentProfileError("profile is in use");
    db_fname = None
    if profile.db_fname:
      db_fname = profile.db_fname
    else:
      db_fname = path.join(self.prof_dir, profile.id)
    os.remove(db_fname) # XXX: this is somewhat dangerous, notification or sth. needed

  def load_profiles(self):
    return Profile.load_all(self.__prof_dir)

  def set_cur_profile(self, profile):
    self.__cur_prof = profile
    db_fname = None
    if profile.db_fname:
      db_fname = profile.db_fname
    else:
      db_fname = path.join(self.prof_dir, profile.id)
    cpool.cpool_release()
    cpool.cpool_init(db_fname, 5)
    # XXX: send out the 'alive' announcement

  def get_cur_profile(self):
    return self.__cur_prof
