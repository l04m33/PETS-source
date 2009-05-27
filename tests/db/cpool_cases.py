import unittest
import sqlite3
import os
import sys
try:
  sys.path += [os.environ['PETS_PATH']]
except: pass

from db import cpool

class InitReleaseCase(unittest.TestCase):

  def testInitRelease(self):
    cpool.cpool_init('./cpool_test_db', 99)
    self.assertTrue(isinstance(cpool.get_cpool(), cpool.ConnectionPool))
    cpool.cpool_release()
    self.assertEqual(cpool.get_cpool(), None)

  def tearDown(self):
    if os.path.isfile('./cpool_test_db'):
      os.remove('./cpool_test_db')


class ConnectionPoolCase(unittest.TestCase):

  def testInit(self):
    cp = cpool.ConnectionPool('./cpool_test_db', 99)
    self.assertEqual(len(cp.pool), 99)
    cp.release()
    self.assertEqual(len(cp.pool), 0)

  def testGetPutConn(self):
    cp = cpool.ConnectionPool('./cpool_test_db', 99)
    c = cp.get_connection()
    self.assertTrue(isinstance(c, sqlite3.Connection))
    self.assertEqual(len(cp.pool), 98)
    cp.put_connection(c)
    self.assertEqual(len(cp.pool), 99)
    cp.release()
    self.assertEqual(len(cp.pool), 0)


if __name__ == '__main__':
  unittest.main()

