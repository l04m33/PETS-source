import unittest
import sqlite3
import os
import sys
sys.path += [os.environ['PETS_PATH']]

from db import support as supp

class SQLCase(unittest.TestCase):

  def testGetSQL(self):
    self.assertEqual(supp.get_sql('local_files.insert').strip(),
        'insert into local_files (hash, full_name, name, seg_size, mod_time, size)\n        values (?, ?, ?, ?, ?, ?);')
    self.assertEqual(supp.get_sql('local_files.select_all').strip(),
        'select * from local_files;')
    self.assertEqual(supp.get_sql('prof_attrs.insert').strip(),
        'insert into prof_attrs (name, value) values (?, ?);')
    self.assertRaises(supp.UnknownSQLError, supp.get_sql, 'local_files.doesntexist')


class DBCase(unittest.TestCase):

  def testGenDB(self):
    db_fname = './support_test_db'
    supp.gen_db(db_fname)
    self.assertTrue(os.path.isfile(db_fname))
    conn = sqlite3.connect(db_fname)
    conn.execute('select * from buddies;')
    conn.execute('select * from chat_log;')
    conn.execute('select * from exts;')
    conn.execute('select * from local_files;')
    conn.execute('select * from prof_attrs;')
    conn.execute('select * from buddy_extra;')
    conn.execute('select * from ext_prefs;')
    conn.execute('select * from file_tag;')
    conn.execute('select * from local_segs;')
    conn.execute('select * from tags;')
    conn.close()

  def tearDown(self):
    db_fname = './support_test_db'
    if os.path.isfile(db_fname):
      os.remove(db_fname)


if __name__ == '__main__':
  unittest.main()
