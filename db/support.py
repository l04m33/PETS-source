import sqlite3
from os import path
from xml.dom import minidom

class UnknownSQLError(Exception):
  pass

__xml_path = path.join(path.split(__file__)[0], 'sql_statements.xml')

__xml_file = open(__xml_path)
_sql_dom = minidom.parse(__xml_file).firstChild
__xml_file.close()
del __xml_file

_dbs = filter(lambda n: n.nodeType != n.TEXT_NODE, _sql_dom.childNodes)

def get_sql(qname):
  qname = qname.strip()
  comps = filter(None, qname.split('.'))
  if(len(comps) == 0):
    raise UnknownSQLError("no such sql statement: '%s'" % qname)

  cur_list = _dbs
  for c in comps:
    match = None
    cur_list = filter(lambda n: n.nodeType != n.TEXT_NODE, cur_list)
    for e in cur_list:
      if c == e.tagName:
        match = e; break
    if match is None:
      raise UnknownSQLError("no such sql statement: '%s'" % qname)
    cur_list = match.childNodes

  return match.firstChild.nodeValue


__schema_path = path.join(path.split(__file__)[0], 'db_schema.sql')

def gen_db(db_path):
  fsql = open(__schema_path)
  conn = sqlite3.connect(db_path)
  conn.executescript(fsql.read())
  conn.close()
  fsql.close()


if __name__ == '__main__':
  import sys
  qname = sys.argv[1]
  print get_sql(qname)
