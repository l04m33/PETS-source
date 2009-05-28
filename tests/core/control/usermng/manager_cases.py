import uuid
import unittest
import os
import sys
try:
  sys.path += [os.environ['PETS_PATH']]
except: pass

from core import model
from core.control import usermng

class ProfileManagerCase(unittest.TestCase):

  def setUp(self):
    self.pm = usermng.ProfileManager('.')
    np0 = model.Profile()
    np0.name = 'Saya'
    self.np0_id = str(uuid.uuid1())
    np0.id = self.np0_id
    np1 = model.Profile()
    np1.name = 'Ayumi'
    self.np1_id = str(uuid.uuid1())
    np1.id = self.np1_id
    self.pm.add_profile(np0)
    self.pm.add_profile(np1)

  def testAdd(self):
    np = model.Profile()
    pid = str(uuid.uuid1())
    np.name = 'Ai'
    np.id = pid
    np.attr_dict['extra_attr'] = 'something important'
    self.pm.add_profile(np)
    pd = self.pm.load_profiles()
    self.assertEqual(len(pd), 3)
    self.assertEqual(pd[pid].id, pid)
    self.assertEqual(pd[pid].attr_dict['extra_attr'], 'something important')

  def testLoad(self):
    pd = self.pm.load_profiles()
    self.assertEqual(len(pd), 2)

  def testDel(self):
    pd = self.pm.load_profiles()
    for k, v in pd.items():
      if k != self.np1_id:
        self.pm.del_profile(v)
    pd = self.pm.load_profiles()
    self.assertEqual(len(pd), 1)

  def testSetGet(self):
    self.assertEqual(self.pm.get_cur_profile().id, self.np1_id)
    pd = self.pm.load_profiles()
    self.pm.set_cur_profile(pd[self.np0_id])
    self.assertEqual(self.pm.get_cur_profile().id, self.np0_id)

  def tearDown(self):
    pd = self.pm.load_profiles()
    self.pm.set_cur_profile(None)
    for k, v in pd.items():
      self.pm.del_profile(v)


if __name__ == '__main__':
  unittest.main()
