from xml.dom import minidom

class UnknownSQLError(Exception):
  pass

__xml_path = 'sql_statements.xml'

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


if __name__ == '__main__':
  import sys
  qname = sys.argv[1]
  print get_sql(qname)
