
class LogDict(dict):

  def __init__(self, *args, **kwargs):
    dict.__init__(self, *args, **kwargs)
    self.del_list = []
    self.ins_list = []
    self.upd_list = []

  def __delitem__(self, item):
    dict.__delitem__(self, item)
    if item not in self.ins_list:
      if item in self.upd_list:
        self.upd_list.remove(item)
      self.del_list.append(item)
    else:
      self.ins_list.remove(item)

  def __setitem__(self, item, value):
    if dict.has_key(self, item):
      if item not in self.ins_list:
        self.upd_list.append(item)
    else:
      if item in self.del_list:
        self.del_list.remove(item)
        self.upd_list.append(item)
      else:
        self.ins_list.append(item)
    dict.__setitem__(self, item, value)

  def reset_stat(self):
    self.ins_list = []
    self.upd_list = []
    self.del_list = []

