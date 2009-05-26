from os import path
import sqlite3
import db

class IncompleteDataError(Exception):
  pass

class Profile:

  def __init__(self):
    self.id = None
    self.name = None
    self.db_fname = None
    self.attr_dict = dict()

  def save(self):
    self._check_integrity()
    pda = db.ProfileAttrDA()
    pda.begin_transaction()
    pda.save_row(('id', self.id))
    pda.save_row(('name', self.name))
    for k, v in self.attr_dict:
      pda.save_row((k, v))
    pda.end_transaction()

  def update(self):
    self._check_integrity()
    pda = db.ProfileAttrDA()
    pda.begin_transaction()
    pda.update_row(('id', self.id))
    pda.update_row(('name', self.name))
    for k, v in self.attr_dict.items():
      pda.update_row((k, v))
    pda.end_transaction()

  @classmethod
  def load_all(cls, prof_dir):
    # ------------------------
    def walker_func(dct, dirname, fnames):
      tpda = db.ProfileAttrDA()
      while fnames:
        fn = path.join(dirname, fnames.pop())
        if path.isfile(fn):
          tpda._conn = sqlite3.connect(fn) # XXX: well this is a dirty trick....
          prof = None
          try:
            attr_lst = tpda.load_all()
            td = dict(attr_lst)
            prof = Profile()
            prof.id = td['id']
            del td['id']
            prof.name = td['name']
            del td['name']
            prof.db_fname = fn
            prof.attr_dict = td
          except:
            continue
          finally:
            tpda._conn.close()
          dct[prof.id] = prof
    # ------------------------
    prof_dct = dict()
    path.walk(prof_dir, walker_func, prof_dct)
    return prof_dct

  def _check_integrity(self):
    if (self.id is None) or (self.name is None):
      raise IncompleteDataError("missing 'name' or 'id'")

