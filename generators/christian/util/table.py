import tablehelper

ATTRIBS = '''
XML TYPE      | ATTRIBUTES ALLOWED
module        | suppressWarnings
tab group     | f
tab           | f
GUI/data element   | b, c, e, ec, f, l, lc, t
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

<opts>          | 1 <= <opt>            |

<str>           | 0 <= app <= 1         |
<str>           | 0 <= fmt <= 1         |
<str>           | 0 <= pos <= 1         |

<col>           | 1 <= GUI/data element      |

<opt>           | 0 <= <desc> <= 1      |
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

<opt>                | desc        | <desc>
'''

# Types (t attribute in module.xml schema) of menu-like items
MENU_TS = [
    'checkbox',
    'dropdown',
    'list',
    'picture',
    'radio'
]

# Types (t attribute in module.xml schema) where <desc> is allowed to go
DESC_TS = [
    'audio',
    'camera',
    'checkbox',
    'dropdown',
    'file',
    'input',
    'list',
    'picture',
    'radio',
    'video'
]

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
        'autonum'   : '<Next___REPLACE__ t="input" b="decimal"\
                                       f="readonly notnull"/>',
        'gps'       : '<Colgroup_GPS t="group"/>              \
                       <Latitude     t="input" f="readonly"/> \
                       <Longitude    t="input" f="readonly"/> \
                       <Northing     t="input" f="readonly"/> \
                       <Easting      t="input" f="readonly"/>',
        'search'    : '<Search f="readonly nodata">    \
                         <cols>                        \
                           <Search_Term t="input"/>    \
                           <Search_Button t="button"/> \
                         </cols>                       \
                         <Entity_Types t="input"/>     \
                         <Entity_List t="list"/>       \
                       </Search>',
        'timestamp' : '<Timestamp t="input" f="readonly nodata"/>'
}

ARCH16N = '''
A_next_ID_has_not_been_entered_please_provide_one=A next ID has not been entered. Please provide one.
Accuracy=Accuracy
Alert=Alert
All=All
Any_unsaved_changes_will_be_lost=Any unsaved changes will be lost
Clean_Synced_Files=Clean synced files
Confirm_Deletion=Confirm Deletion
Delete=Delete
Delete_Cancelled=Delete cancelled
Disable_External_GPS=Disable External GPS
Disable_Internal_GPS=Disable Internal GPS
Disable_Sync=Disable Sync
Duplicate=Duplicate
Duplicated_record=Duplicated record
Easting=Easting
Easting=Easting
Enable_External_GPS=Enable External GPS
Enable_Internal_GPS=Enable Internal GPS
Enable_Sync=Enable Sync
Entity_List=Entity List
Entity_Types=Entity Types
External_GPS_Disabled=External GPS disabled
External_GPS_Enabled=External GPS enabled
GPS_Not_Initialised=GPS Not Initialised
GPS_is_no_longer_initialised=GPS is no longer initialised
GPS_is_not_initialised=GPS is not initialised
Internal_GPS=Internal GPS
Internal_GPS_Disabled=Internal GPS disabled
Internal_GPS_Enabled=Internal GPS enabled
Latitude=Latitude
Latitude=Latitude
Longitude=Longitude
Longitude=Longitude
New=New
New_record_created=New record created
Northing=Northing
Northing=Northing
Please_Enable_Bluetooth=Please enable bluetooth
Position=Position
Press_OK_to_Delete_this_Record=Press OK to delete this record
Previous_status=Previous status
Search=Search
Search_Term=Search Term
Sync_Disabled=Sync disabled
Sync_Enabled=Sync enabled
Take_From_GPS=Take From GPS
This_record_is_unsaved_and_cannot_be_duplicated=This record is unsaved and cannot be duplicated
Validate=Validate
Warning=Warning
You_must_save_this_tabgroup_first=You must save this tab group first
no_GPS_position_could_be_found=no GPS position could be found
off=off
on=on
on_and_bluetooth_connected=on and bluetooth connected
on_and_bluetooth_disconnected=on and bluetooth disconnected
'''

ATTRIBS       = tablehelper.parseTable(ATTRIBS)
ATTRIB_VALS   = tablehelper.parseTable(ATTRIB_VALS)
CARDINALITIES = tablehelper.parseTable(CARDINALITIES)
TYPES         = tablehelper.parseTable(TYPES)
ARCH16N       = ARCH16N.splitlines()
