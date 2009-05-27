import unittest
import os
import sys
sys.path += [os.environ['PETS_PATH']]

from db import da, cpool
from db import support as supp


class BaseDACase(unittest.TestCase):

  def setUp(self):
    db_fname = './da_test_db'
    supp.gen_db(db_fname)
    cpool.cpool_release()
    cpool.cpool_init(db_fname, 5)

  def testTransaction(self):
    bda = da.BaseDA()
    bda.begin_transaction()
    bda.rollback()
    bda.end_transaction()
    self.assertRaises(da.NoActiveConnectionError, bda.end_transaction)
    self.assertRaises(da.NoActiveConnectionError, bda.rollback)

  def tearDown(self):
    db_fname = './da_test_db'
    cpool.cpool_release()
    if os.path.isfile(db_fname):
      os.remove(db_fname)


class LocalFileDACase(unittest.TestCase):

  def setUp(self):
    db_fname = './da_test_db'
    supp.gen_db(db_fname)
    cpool.cpool_release()
    cpool.cpool_init(db_fname, 5)
    self.lfda = da.LocalFileDA()
    self.file_hash = 'file_hash'
    self.seg_hashs = ('seg_hash0', 'seg_hash1')

    row = (self.file_hash, 'full_name', 'name', 4096, '2009-01-01 09:09:09', 7168)
    seg_row0 = (self.seg_hashs[0], 0, self.file_hash, True)
    seg_row1 = (self.seg_hashs[1], 4096, self.file_hash, False)
    self.lfda.begin_transaction()
    self.lfda.save_row(row)
    self.lfda.save_seg_row(seg_row0)
    self.lfda.save_seg_row(seg_row1)
    self.lfda.end_transaction()

  def testSaveLoad(self):
    row = (self.file_hash + '_new', 'full_name', 'name', 4096, '2009-01-01 09:09:09', 7168)
    seg_row0 = (self.seg_hashs[0] + '_new', 0, self.file_hash + '_new', True)
    seg_row1 = (self.seg_hashs[1] + '_new', 4096, self.file_hash + '_new', False)
    self.lfda.begin_transaction()
    self.assertEqual(self.lfda.save_row(row), 1)
    self.assertEqual(self.lfda.save_seg_row(seg_row0), 1)
    self.assertEqual(self.lfda.save_seg_row(seg_row1), 1)
    self.lfda.end_transaction()

    self.lfda.begin_transaction()
    self.assertEqual(self.lfda.load_by_hash(self.file_hash + '_new').fetchall()[0], row)
    self.assertEqual(self.lfda.load_seg_by_hash(self.seg_hashs[0] + '_new').fetchall()[0], seg_row0)
    self.assertEqual(self.lfda.load_seg_by_hash(self.seg_hashs[1] + '_new').fetchall()[0], seg_row1)
    self.assertEqual(len(self.lfda.load_all().fetchall()), 2)
    self.assertEqual(len(self.lfda.load_all_segs().fetchall()), 4)
    self.assertEqual(len(self.lfda.load_by_hash('doesntexist').fetchall()), 0)
    self.assertEqual(len(self.lfda.load_seg_by_hash('doesntexist').fetchall()), 0)
    self.lfda.end_transaction()

  def testUpdateLoad(self):
    row = (self.file_hash, 'modified', 'name', 4096, '2009-09-09 09:09:09', 7168)
    seg_row0 = (self.seg_hashs[0], 0, self.file_hash, False)
    seg_row1 = (self.seg_hashs[1], 4096, self.file_hash, True)
    self.lfda.begin_transaction()
    self.assertEqual(self.lfda.update_row(row), 1)
    self.assertEqual(self.lfda.update_seg_row(seg_row0), 1)
    self.assertEqual(self.lfda.update_seg_row(seg_row1), 1)
    self.lfda.end_transaction()

    self.lfda.begin_transaction()
    self.assertEqual(self.lfda.load_by_hash(self.file_hash).fetchall()[0], row)
    self.assertEqual(self.lfda.load_seg_by_hash(self.seg_hashs[0]).fetchall()[0], seg_row0)
    self.assertEqual(self.lfda.load_seg_by_hash(self.seg_hashs[1]).fetchall()[0], seg_row1)
    self.lfda.end_transaction()

  def testDeleteLoad(self):
    self.lfda.begin_transaction()
    self.assertEqual(self.lfda.del_seg_by_hash(self.seg_hashs[0]), 1)
    self.assertEqual(self.lfda.del_seg_by_hash(self.seg_hashs[1]), 1)
    self.assertEqual(self.lfda.del_by_hash(self.file_hash), 1)
    self.lfda.end_transaction()

    self.lfda.begin_transaction()
    self.assertEqual(len(self.lfda.load_all().fetchall()), 0)
    self.assertEqual(len(self.lfda.load_all_segs().fetchall()), 0)
    self.lfda.end_transaction()

  def tearDown(self):
    db_fname = './da_test_db'
    del self.lfda
    cpool.cpool_release()
    if os.path.isfile(db_fname):
      os.remove(db_fname)


class ProfileAttrDACase(unittest.TestCase):

  def setUp(self):
    db_fname = './da_test_db'
    supp.gen_db(db_fname)
    cpool.cpool_release()
    cpool.cpool_init(db_fname, 5)
    self.pada = da.ProfileAttrDA()

    row = ('nonsense_name', 'nonsense_value')
    self.pada.begin_transaction()
    self.pada.save_row(row)
    self.pada.end_transaction()

  def testSaveLoad(self):
    row = ('new_name', 'new_value')
    self.pada.begin_transaction()
    self.assertEqual(self.pada.save_row(row), 1)
    self.pada.end_transaction()

    self.pada.begin_transaction()
    self.assertEqual(self.pada.load_by_name('new_name').fetchall()[0], row)
    self.assertEqual(len(self.pada.load_all().fetchall()), 2)
    self.pada.end_transaction()

  def testUpdateLoad(self):
    row = ('nonsense_name', 'valuable_value')
    self.pada.begin_transaction()
    self.assertEqual(self.pada.update_row(row), 1)
    self.pada.end_transaction()

    self.pada.begin_transaction()
    self.assertEqual(self.pada.load_by_name('nonsense_name').fetchall()[0], row)
    self.pada.end_transaction()

  def testDeleteLoad(self):
    self.pada.begin_transaction()
    self.assertEqual(self.pada.del_by_name('nonsense_name'), 1)
    self.pada.end_transaction()

    self.pada.begin_transaction()
    self.assertEqual(len(self.pada.load_all().fetchall()), 0)
    self.pada.end_transaction()

  def tearDown(self):
    db_fname = './da_test_db'
    del self.pada
    cpool.cpool_release()
    if os.path.isfile(db_fname):
      os.remove(db_fname)


if __name__ == '__main__':
  unittest.main()

