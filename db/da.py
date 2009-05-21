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

  def save_row(self, row):
    self.__check_conn()
    self.__conn.execute(supp.get_sql('local_files.insert') % row)

  def del_by_hash(self, hash):
    self.__check_conn()
    self.__conn.execute(supp.get_sql('local_files.delete_by_pk') % (hash,))

  def save_seg_row(self, seg_row):
    self.__check_conn()
    self.__conn.execute(supp.get_sql('local_segs.insert') % seg_row)

  def del_seg_by_hash(self, seg_hash):
    self.__check_conn()
    self.__conn.execute(supp.get_sql('local_segs.delete_by_pk') % (seg_hash,))

  def __check_conn(self):
    if self.__conn is None:
      raise NoActiveConnectionError("maybe you should 'begin_transaction()' before calling this")



if __name__ == '__main__':
  cpool.cpool_init('/home/l_amee/client_share/P.E.T.S/tmp/pets_def_db.sqlite3', 5)

  # testing for the LocalFileDA
  lfda = LocalFileDA()

  lfda.begin_transaction()
  lfda.save_row(('file_hash', 'full_name', 'name', 4096, '2009', 8192))
  lfda.save_seg_row(('seg_hash', 0, 'file_hash', 'true'))
  lfda.save_seg_row(('seg_hash1', 4096, 'file_hash', 'false'))
  lfda.end_transaction()

  lfda.begin_transaction()
  lfda.del_seg_by_hash('seg_hash')
  lfda.del_seg_by_hash('seg_hash1')
  lfda.del_by_hash('file_hash')
  lfda.end_transaction()
