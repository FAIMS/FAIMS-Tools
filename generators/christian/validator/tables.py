import datatransformers

ATTRIBS = '''
XML TYPE      | ATTRIBUTES ALLOWED
module        |
tab group     | f
tab           | f
GUI/data element   | b, c, ec, f, l, lc, t
<cols>        | f
<opts>        |
<str>         |
<col>         | f
<opt>         | p
<app>         |
<author>      |
<autonum>     |
<desc>        |
<fmt>         |
<gps>         |
<logic>       |
<pos>         |
<rels>        |
<search>      |
<timestamp>   |
'''

ATTRIB_VALS = '''
ATTRIBUTE    | ALLOWED VALUES (ONE-OF)     | ALLOWED VALUES (MANY-OF)
b            | date, decimal, string, time |
c            |                             |
f            |                             | autonum, hidden, id, noannotation, nocertainty, nodata, nolabel, noscroll, nosync, nothumb, nothumbnail, notnull, noui, readonly, user
l            | $link-all                   |
ec           | $link-tabgroup              |
lc           | $link-tabgroup              |
t            | audio, button, camera, checkbox, dropdown, file, gpsdiag, group, input, list, map, picture, radio, table, video, viewfiles, web, webview |
p            |                             |
'''

CARDINALITIES = '''
PARENT XML TYPE | DIRECT CHILD COUNT    | DESCENDANT COUNT
document        | 1 <= module <= 1      |

module          | 1 <= tab group        |
module          | 0 <= <logic> <= 1     |
module          | 0 <= <rels>  <= 1     |

tab group       | 1 <= tab              |
tab group       | 0 <= <desc>   <= 1    |
tab group       | 0 <= <search> <= 1    |

tab             |                       | 1 <= GUI/data element
tab             | 0 <= <autonum>   <= 1 |
tab             | 0 <= <cols>           |
tab             | 0 <= <gps>       <= 1 |
tab             | 0 <= <author>    <= 1 |
tab             | 0 <= <timestamp> <= 1 |

GUI/data element     | 0 <= <desc> <= 1      |
GUI/data element     | 0 <= <opts> <= 1      |
GUI/data element     | 0 <= <str>  <= 1      |

<cols>          |                       | 1 <= GUI/data element
<cols>          | 1 <= <col>            |

<opts>          | 1 <= <opt>            |

<str>           | 0 <= app <= 1         |
<str>           | 0 <= fmt <= 1         |
<str>           | 0 <= pos <= 1         |

<col>           | 1 <= GUI/data element      |

<opt>           | 0 <= <opt>            |
'''

TYPES = '''
PARENT XML TYPE      | PATTERN     | MATCH XML TYPE
document             | /           | module

module               | /[^a-z]/    | tab group
module               | logic       | <logic>
module               | rels        | <rels>

tab group            | /[^a-z]/    | tab
tab group            | desc        | <desc>
tab group            | search      | <search>

tab                  | /[^a-z]/    | GUI/data element
tab                  | author      | <author>
tab                  | autonum     | <autonum>
tab                  | cols        | <cols>
tab                  | gps         | <gps>
tab                  | timestamp   | <timestamp>

<cols>               | /[^a-z]/    | GUI/data element
<cols>               | col         | <col>

<col>                | /[^a-z]/    | GUI/data element

GUI/data element     | desc        | <desc>
GUI/data element     | opts        | <opts>
GUI/data element     | str         | <str>

<str>                | app         | <app>
<str>                | fmt         | <fmt>
<str>                | pos         | <pos>

<opts>               | opt         | <opt>

<opt>                | opt         | <opt>
'''

REPLACEMENTS_BY_T_ATTRIB = {
        'audio'  : '<__REPLACE__        t="dropdown"/>\
                    <Button___REPLACE__ t="button"/>',
        'camera' : '<__REPLACE__        t="dropdown"/>\
                    <Button___REPLACE__ t="button"/>',
        'file'   : '<__REPLACE__        t="dropdown"/>\
                    <Button___REPLACE__ t="button"/>',
        'video'  : '<__REPLACE__        t="dropdown"/>\
                    <Button___REPLACE__ t="button"/>',
}
REPLACEMENTS_BY_TAG = {
        'author'    : '<Author t="input" f="readonly nodata"/>',
        'gps'       : '<Colgroup_GPS t="group"/>              \
                       <Latitude     t="input" f="readonly"/> \
                       <Longitude    t="input" f="readonly"/> \
                       <Northing     t="input" f="readonly"/> \
                       <Easting      t="input" f="readonly"/>',
        'search'    : '<Search f="readonly">           \
                         <cols>                        \
                           <Search_Term t="input"/>    \
                           <Search_Button t="button"/> \
                         </cols>                       \
                         <Entity_Types t="input"/>     \
                         <Entity_List t="list"/>       \
                       </Search>',
        'timestamp' : '<Timestamp t="input" f="readonly nodata"/>'
}

ATTRIBS       = datatransformers.parseTable(ATTRIBS)
ATTRIB_VALS   = datatransformers.parseTable(ATTRIB_VALS)
CARDINALITIES = datatransformers.parseTable(CARDINALITIES)
TYPES         = datatransformers.parseTable(TYPES)
