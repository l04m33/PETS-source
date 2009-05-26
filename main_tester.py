import uuid

from core.control import usermng
from core import model

pm = usermng.ProfileManager('/home/l_amee/.VirtualBox/client_share/P.E.T.S/tmp/tmp')

print '######## testing for profile loader....'
print pm.load_profiles()
print
print '######## testing for profile adder....'
np = model.Profile()
np.id = str(uuid.uuid1())
np.name = 'testing_name'
pm.add_profile(np)
print 'successful'
print np.db_fname
print
print '######## testing for profile deleter....'
old_p = [e for e in pm.load_profiles().items() if e[0] != np.id][0][1]
pm.set_cur_profile(old_p)
pm.del_profile(np)
print 'successfule'

