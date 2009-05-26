import sqlite3
import threading

class ConnectionPool:

  def __init__(self, db_path, n):
    self.pool = []
    self.plock = threading.Lock()
    self.pool_size = n
    self.db_path = db_path
    for i in range(n):
      conn = sqlite3.connect(db_path)
      conn.text_factory = str
      self.pool.append(conn)

  def get_connection(self):
    self.plock.acquire()
    if len(self.pool) > 0:
      conn = self.pool.pop(0)
      self.plock.release()
      return conn
    self.plock.release()
    conn = sqlite3.connect(self.db_path)
    return conn

  def put_connection(self, conn):
    self.plock.acquire()
    if len(self.pool) < self.pool_size:
      self.pool.append(conn)
      self.plock.release()
      return
    self.plock.release()
    conn.close()

  # this needs more synchronization
  # given-away connections may still be in action
  def release(self):
    self.plock.acquire()
    for c in self.pool:
      c.close()
    self.pool = []
    self.plock.release()


__def_cpool = None

# this function should be run before any attempt to access the pool
def cpool_init(db_path, n):
  global __def_cpool
  if __def_cpool is not None:
    __def_cpool.release()
  __def_cpool = ConnectionPool(db_path, n)

def get_cpool():
  global __def_cpool
  return __def_cpool

def cpool_release():
  global __def_cpool
  if __def_cpool:
    __def_cpool.release()
    __def_cpool = None


if __name__ == '__main__':
  cpool_init("/home/l_amee/client_share/P.E.T.S/tmp/pets_def_db.sqlite3", 4)
  conn = get_cpool().get_connection()
  print conn
  get_cpool().put_connection(conn)
  get_cpool().release()
