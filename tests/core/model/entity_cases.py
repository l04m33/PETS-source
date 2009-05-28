import uuid
import unittest
import os
import sys
try:
  sys.path += [os.environ['PETS_PATH']]
except: pass

from core import model
from db import cpool, support as supp

class ProfileCase(unittest.TestCase):

  def setUp(self):
    db_fname = './entity_test_db'
    supp.gen_db(db_fname)
    cpool.cpool_init(db_fname, 5)
    p = model.Profile()
    p.name = 'Ayumi'
    self.pid = str(uuid.uuid1())
    p.id = self.pid
    p.attr_dict['extra_info'] = 'something important'
    p.save()

  def testSave(self):
    pd = model.Profile.load_all('.')
    self.assertEqual(len(pd), 1)
    self.assertEqual(pd[self.pid].id, self.pid)
    self.assertEqual(pd[self.pid].attr_dict['extra_info'], 'something important')

  def testUpdate(self):
    p = model.Profile.load_all('.')[self.pid]
    p.name = 'modified'
    del p.attr_dict['extra_info']
    p.attr_dict['new_extra_info'] = '123456789'
    p.update()
    np = model.Profile.load_all('.')[self.pid]
    self.assertEqual(np.id, self.pid)
    self.assertEqual(np.name, 'modified')
    self.assertRaises(KeyError, np.attr_dict.__getitem__, 'extra_info')
    self.assertEqual(np.attr_dict['new_extra_info'], '123456789')

  def tearDown(self):
    db_fname = './entity_test_db'
    cpool.cpool_release()
    if os.path.isfile(db_fname):
      os.remove(db_fname)


if __name__ == '__main__':
  unittest.main()

