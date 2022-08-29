from ...rust import Enum, make_struct, make_tuple, Dict
Pagination = make_struct("Pagination", [("start", int), ("limit", int)])

