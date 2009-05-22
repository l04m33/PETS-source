import sqlite3
import support as supp
import cpool


class NoActiveConnectionError(Exception):
  pass


class BaseDA:

  def __init__(self):
    self._conn = None
    self.cpool = cpool.get_cpool()

  def begin_transaction(self):
    if self._conn is not None:
      self._conn.rollback()
    self._conn = self.cpool.get_connection()

  def end_transaction(self):
    self._check_conn()
    self._conn.commit()
    self.cpool.put_connection(self._conn)
    self._conn = None

  def rollback(self):
    self._check_conn()
    self._conn.rollback()

  def _check_conn(self):
    if self._conn is None:
      raise NoActiveConnectionError("maybe you should 'begin_transaction()' before calling this")


class LocalFileDA(BaseDA):

  def load_by_hash(self, hash):
    self._check_conn()
    cur = self._conn.execute(
        supp.get_sql('local_files.select_by_pk'), (hash,))
    return cur

  def load_all(self):
    self._check_conn()
    cur = self._conn.execute(
        supp.get_sql('local_files.select_all'))
    return cur

  def load_seg_by_hash(self, hash):
    self._check_conn()
    cur = self._conn.execute(
        supp.get_sql('local_segs.select_by_pk'), (hash,))
    return cur

  def load_all_segs(self):
    self._check_conn()
    cur = self._conn.execute(
        supp.get_sql('local_segs.select_all'))
    return cur

  def load_segs_by_file(self, file_hash):
    self._check_conn()
    cur = self._conn.execute(
        supp.get_sql('local_segs.select_by_fk'), (file_hash,))
    return cur

  def save_row(self, row):
    self._check_conn()
    cur = self._conn.execute(
        supp.get_sql('local_files.insert'), row)
    return cur.rowcount

  def update_row(self, row):
    self._check_conn()
    cur = self._conn.execute(
        supp.get_sql('local_files.update'), row[1:] + (row[0],))
    return cur.rowcount

  def del_by_hash(self, hash):
    self._check_conn()
    cur = self._conn.execute(
        supp.get_sql('local_files.delete_by_pk'), (hash,))
    return cur.rowcount

  def save_seg_row(self, seg_row):
    self._check_conn()
    cur = self._conn.execute(
        supp.get_sql('local_segs.insert'), seg_row)
    return cur.rowcount

  def update_seg_row(self, seg_row):
    self._check_conn()
    cur = self._conn.execute(
        supp.get_sql('local_segs.update'), seg_row[1:] + (seg_row[0],))
    return cur.rowcount

  def del_seg_by_hash(self, seg_hash):
    self._check_conn()
    cur = self._conn.execute(
        supp.get_sql('local_segs.delete_by_pk'), (seg_hash,))
    return cur.rowcount


class ProfileAttrDA(BaseDA):

  def save_row(self, row):
    self._check_conn()
    cur = self._conn.execute(
        supp.get_sql('prof_attrs.insert'), row)
    return cur.rowcount

  # well, we locate the to-be-modified row by looking at their PK
  def update_row(self, row):
    self._check_conn()
    cur = self._conn.execute(
        supp.get_sql('prof_attrs.update'), (row[1], row[0]))
    return cur.rowcount

  def load_by_name(self, name):
    self._check_conn()
    cur = self._conn.execute(
        supp.get_sql('prof_attrs.select_by_pk'), (name,))
    return cur

  def load_all(self):
    self._check_conn()
    cur = self._conn.execute(
        supp.get_sql('prof_attrs.select_all'))
    return cur

  def del_by_name(self, name):
    self._check_conn()
    cur = self._conn.execute(
        supp.get_sql('prof_attrs.delete_by_pk'), (name,))
    return cur.rowcount


if __name__ == '__main__':
  import hashlib
  s = hashlib.sha1()
  s.update("empty")

  cpool.cpool_init('/home/l_amee/client_share/P.E.T.S/tmp/pets_def_db.sqlite3', 5)

  print "---------- testing for the LocalFileDA ----------"
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

  print
  print "---------- testing for the ProfileAttrDA ----------"
  pada = ProfileAttrDA()

  pada.begin_transaction()
  pada.save_row(('test1', 'test value 1'))
  pada.save_row(('uuid', '123-456-789'))
  pada.end_transaction()

  pada.begin_transaction()
  print pada.load_by_name('uuid').fetchall()
  print pada.load_all().fetchall()
  pada.end_transaction()

  pada.begin_transaction()
  pada.del_by_name('uuid')
  pada.del_by_name('test1')
  pada.end_transaction()
