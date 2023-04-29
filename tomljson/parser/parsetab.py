
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ARRAY_TABLES_HEADER BOOLEAN CHILD_HEADER COMMA COMMENT DATE DOT EQUAL FLOAT INTEGER LBRACKET LCURLY NEWLINE RBRACKET RCURLY SPACE STRING TABLE_HEADER VARIABLEdocument : toml\n    | toml documenttoml : content\n    | array\n    | table\n    | inline_table\n    | array_tablesarray_tables : ARRAY_TABLES_HEADER content\n    | ARRAY_TABLES_HEADER array_tableschild : CHILD_HEADER contentinline_table : LCURLY contents RCURLY\n    | LCURLY RCURLYtable : TABLE_HEADER content\n    | TABLE_HEADER childcontents : contents COMMA content\n    | contentcontent : assignment\n    | content assignmentassignment : VARIABLE value\n    | VARIABLE array\n    | VARIABLE inline_tablearray : DOT LBRACKET array RBRACKET\n    | DOT LBRACKET values RBRACKET\n    | DOT LBRACKET RBRACKETvalues : value COMMA values\n    | valuevalue : STRING\n    | INTEGER\n    | FLOAT\n    | BOOLEAN\n    | DATE'
    
_lr_action_items = {'DOT':([0,2,3,4,5,6,7,8,13,15,16,17,18,21,23,24,25,26,27,28,29,30,31,32,34,37,38,40,41,],[9,9,-3,-4,-5,-6,-7,-17,9,-18,9,-13,-14,-12,-8,-9,-19,-20,-21,-27,-28,-29,-30,-31,-24,-10,-11,-22,-23,]),'TABLE_HEADER':([0,2,3,4,5,6,7,8,15,17,18,21,23,24,25,26,27,28,29,30,31,32,34,37,38,40,41,],[10,10,-3,-4,-5,-6,-7,-17,-18,-13,-14,-12,-8,-9,-19,-20,-21,-27,-28,-29,-30,-31,-24,-10,-11,-22,-23,]),'LCURLY':([0,2,3,4,5,6,7,8,13,15,17,18,21,23,24,25,26,27,28,29,30,31,32,34,37,38,40,41,],[11,11,-3,-4,-5,-6,-7,-17,11,-18,-13,-14,-12,-8,-9,-19,-20,-21,-27,-28,-29,-30,-31,-24,-10,-11,-22,-23,]),'ARRAY_TABLES_HEADER':([0,2,3,4,5,6,7,8,12,15,17,18,21,23,24,25,26,27,28,29,30,31,32,34,37,38,40,41,],[12,12,-3,-4,-5,-6,-7,-17,12,-18,-13,-14,-12,-8,-9,-19,-20,-21,-27,-28,-29,-30,-31,-24,-10,-11,-22,-23,]),'VARIABLE':([0,2,3,4,5,6,7,8,10,11,12,15,17,18,19,21,22,23,24,25,26,27,28,29,30,31,32,34,37,38,39,40,41,43,],[13,13,13,-4,-5,-6,-7,-17,13,13,13,-18,13,-14,13,-12,13,13,-9,-19,-20,-21,-27,-28,-29,-30,-31,-24,13,-11,13,-22,-23,13,]),'$end':([1,2,3,4,5,6,7,8,14,15,17,18,21,23,24,25,26,27,28,29,30,31,32,34,37,38,40,41,],[0,-1,-3,-4,-5,-6,-7,-17,-2,-18,-13,-14,-12,-8,-9,-19,-20,-21,-27,-28,-29,-30,-31,-24,-10,-11,-22,-23,]),'RCURLY':([8,11,15,20,21,22,25,26,27,28,29,30,31,32,34,38,40,41,43,],[-17,21,-18,38,-12,-16,-19,-20,-21,-27,-28,-29,-30,-31,-24,-11,-22,-23,-15,]),'COMMA':([8,15,20,21,22,25,26,27,28,29,30,31,32,34,36,38,40,41,43,],[-17,-18,39,-12,-16,-19,-20,-21,-27,-28,-29,-30,-31,-24,42,-11,-22,-23,-15,]),'LBRACKET':([9,],[16,]),'CHILD_HEADER':([10,],[19,]),'STRING':([13,16,42,],[28,28,28,]),'INTEGER':([13,16,42,],[29,29,29,]),'FLOAT':([13,16,42,],[30,30,30,]),'BOOLEAN':([13,16,42,],[31,31,31,]),'DATE':([13,16,42,],[32,32,32,]),'RBRACKET':([16,28,29,30,31,32,33,34,35,36,40,41,44,],[34,-27,-28,-29,-30,-31,40,-24,41,-26,-22,-23,-25,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'document':([0,2,],[1,14,]),'toml':([0,2,],[2,2,]),'content':([0,2,10,11,12,19,39,],[3,3,17,22,23,37,43,]),'array':([0,2,13,16,],[4,4,26,33,]),'table':([0,2,],[5,5,]),'inline_table':([0,2,13,],[6,6,27,]),'array_tables':([0,2,12,],[7,7,24,]),'assignment':([0,2,3,10,11,12,17,19,22,23,37,39,43,],[8,8,15,8,8,8,15,8,15,15,15,8,15,]),'child':([10,],[18,]),'contents':([11,],[20,]),'value':([13,16,42,],[25,36,36,]),'values':([16,42,],[35,44,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> document","S'",1,None,None,None),
  ('document -> toml','document',1,'p_document','_parser.py',9),
  ('document -> toml document','document',2,'p_document','_parser.py',10),
  ('toml -> content','toml',1,'p_toml','_parser.py',18),
  ('toml -> array','toml',1,'p_toml','_parser.py',19),
  ('toml -> table','toml',1,'p_toml','_parser.py',20),
  ('toml -> inline_table','toml',1,'p_toml','_parser.py',21),
  ('toml -> array_tables','toml',1,'p_toml','_parser.py',22),
  ('array_tables -> ARRAY_TABLES_HEADER content','array_tables',2,'p_array_tables','_parser.py',27),
  ('array_tables -> ARRAY_TABLES_HEADER array_tables','array_tables',2,'p_array_tables','_parser.py',28),
  ('child -> CHILD_HEADER content','child',2,'p_child','_parser.py',33),
  ('inline_table -> LCURLY contents RCURLY','inline_table',3,'p_inline_table','_parser.py',38),
  ('inline_table -> LCURLY RCURLY','inline_table',2,'p_inline_table','_parser.py',39),
  ('table -> TABLE_HEADER content','table',2,'p_table','_parser.py',47),
  ('table -> TABLE_HEADER child','table',2,'p_table','_parser.py',48),
  ('contents -> contents COMMA content','contents',3,'p_contents','_parser.py',53),
  ('contents -> content','contents',1,'p_contents','_parser.py',54),
  ('content -> assignment','content',1,'p_content','_parser.py',61),
  ('content -> content assignment','content',2,'p_content','_parser.py',62),
  ('assignment -> VARIABLE value','assignment',2,'p_assignment','_parser.py',70),
  ('assignment -> VARIABLE array','assignment',2,'p_assignment','_parser.py',71),
  ('assignment -> VARIABLE inline_table','assignment',2,'p_assignment','_parser.py',72),
  ('array -> DOT LBRACKET array RBRACKET','array',4,'p_array','_parser.py',77),
  ('array -> DOT LBRACKET values RBRACKET','array',4,'p_array','_parser.py',78),
  ('array -> DOT LBRACKET RBRACKET','array',3,'p_array','_parser.py',79),
  ('values -> value COMMA values','values',3,'p_values','_parser.py',87),
  ('values -> value','values',1,'p_values','_parser.py',88),
  ('value -> STRING','value',1,'p_value','_parser.py',96),
  ('value -> INTEGER','value',1,'p_value','_parser.py',97),
  ('value -> FLOAT','value',1,'p_value','_parser.py',98),
  ('value -> BOOLEAN','value',1,'p_value','_parser.py',99),
  ('value -> DATE','value',1,'p_value','_parser.py',100),
]
