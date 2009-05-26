import uuid

from core.control import usermng
from core import model

pm = usermng.ProfileManager('/home/l_amee/.VirtualBox/client_share/P.E.T.S/tmp/tmp')
print '######## testing for profile loader....'
print pm.load_profiles()
print '######## testing for profile adder....'
np = model.Profile()
np.id = str(uuid.uuid1())
np.name = 'testing_name'
pm.add_profile(np)
print 'successful'
