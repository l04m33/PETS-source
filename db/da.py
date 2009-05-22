import sqlite3
import support as supp
import cpool


class NoActiveConnectionError(Exception):
  pass


class LocalFileDA:

  def __init__(self):
    self.__conn = None
    self.cpool = cpool.get_cpool()

  # sqlite locks the db if there's a dirty session
  # no locking should be done here
  def begin_transaction(self):
    # drop all the changes if there's already an active session
    if self.__conn is not None:
      self.__conn.rollback()
    self.__conn = self.cpool.get_connection()

  def end_transaction(self):
    self.__check_conn()
    self.__conn.commit()
    self.cpool.put_connection(self.__conn)
    self.__conn = None

  def rollback(self):
    self.__check_conn()
    self.__conn.rollback()

  def load_by_hash(self, hash):
    self.__check_conn()
    cur = self.__conn.execute(
        supp.get_sql('local_files.select_by_pk'), (hash,)
        )
    return cur

  def load_all(self):
    self.__check_conn()
    cur = self.__conn.execute(
        supp.get_sql('local_files.select_all')
        )
    return cur

  def load_seg_by_hash(self, hash):
    self.__check_conn()
    cur = self.__conn.execute(
        supp.get_sql('local_segs.select_by_pk'), (hash,)
        )
    return cur

  def load_all_segs(self):
    self.__check_conn()
    cur = self.__conn.execute(
        supp.get_sql('local_segs.select_all')
        )
    return cur

  def load_segs_by_file(self, file_hash):
    self.__check_conn()
    cur = self.__conn.execute(
        supp.get_sql('local_segs.select_by_fk'), (file_hash,)
        )
    return cur

  def save_row(self, row):
    self.__check_conn()
    self.__conn.execute(supp.get_sql('local_files.insert'), row)

  def del_by_hash(self, hash):
    self.__check_conn()
    self.__conn.execute(supp.get_sql('local_files.delete_by_pk'), (hash,))

  def save_seg_row(self, seg_row):
    self.__check_conn()
    self.__conn.execute(supp.get_sql('local_segs.insert'), seg_row)

  def del_seg_by_hash(self, seg_hash):
    self.__check_conn()
    self.__conn.execute(supp.get_sql('local_segs.delete_by_pk'), (seg_hash,))

  def __check_conn(self):
    if self.__conn is None:
      raise NoActiveConnectionError("maybe you should 'begin_transaction()' before calling this")



if __name__ == '__main__':
  import hashlib
  s = hashlib.sha1()
  s.update("empty")

  cpool.cpool_init('/home/l_amee/client_share/P.E.T.S/tmp/pets_def_db.sqlite3', 5)

  # testing for the LocalFileDA
  lfda = LocalFileDA()

  lfda.begin_transaction()
  lfda.save_row((s.digest(), u'\u5168\u540d', 'name', 4096, '2009', 8192))
  lfda.save_seg_row(('seg_hash', 0, s.digest(), 'true'))
  lfda.save_seg_row(('seg_hash1', 4096, s.digest(), 'false'))
  lfda.end_transaction()

  lfda.begin_transaction()
  print lfda.load_all().fetchall()
  print lfda.load_all_segs().fetchall()
  print lfda.load_by_hash(s.digest()).fetchall()
  print lfda.load_seg_by_hash('seg_hash').fetchall()
  print lfda.load_segs_by_file(s.digest()).fetchall()
  lfda.end_transaction()

  lfda.begin_transaction()
  lfda.del_seg_by_hash('seg_hash')
  lfda.del_seg_by_hash('seg_hash1')
  lfda.del_by_hash(s.digest())
  lfda.end_transaction()
