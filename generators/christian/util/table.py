import tablehelper

# The globals defined here are mostly used for validation, however, `ARCH16N`
# is used elsewhere. The `table.py` file should arguably be merged with
# `consts.py`.

# A (string representation of a) table of allowed attributes for each XML type.
# XML Types are explained in `consts.py`.
ATTRIBS = '''
XML TYPE           | ATTRIBUTES ALLOWED
module             | suppressWarnings, test_mode
tab group          | f
tab                | f
group              | t, s
GUI/data element   | b, c, e, ec, f, l, lc, ll, lq, t, s, vp, i, sp, su
markdown           |
cols               | f
opts               |
str                |
col                | f
opt                | p, sp, su
app                |
author             | f
autonum            |
desc               |
fmt                |
gps                | f
logic              |
pos                |
rels               |
search             |
timestamp          | f
'''

# A (string representation of a) table of allowed values for each XML attribute.
ATTRIB_VALS = '''
ATTRIBUTE    | ALLOWED VALUES (ONE-OF)     | ALLOWED VALUES (MANY-OF)
b            | date, decimal, string, time |
c            |                             |
ec           | $link-tabgroup              |
f            |                             | autonum, hidden, id, noannotation, nocertainty, nodata, nolabel, noscroll, nosync, nothumb, nothumbnail, notnull, noui, nowire, readonly, user, persist, persist!, htmldesc, noautosave
i            |                             | $link-gui
l            | $link-all                   |
lc           | $link-all                   |
ll           | $link-all                   |
p            |                             |
sp           |                             |
su           |                             |
t            | audio, button, camera, checkbox, dropdown, file, gpsdiag, group, input, list, map, picture, radio, table, video, viewfiles, web, webview |
vp           | $link-gui                   |
'''

# Constraints on the number of elements which can be within other elements.
CARDINALITIES = '''
PARENT XML TYPE | DIRECT CHILD COUNT    | DESCENDANT COUNT
document        | 1 <= module <= 1      |

module          | 1 <= tab group        |
module          | 0 <= logic   <= 1     |
module          | 0 <= rels    <= 1     |
module          | 0 <= css     <= 1     |

tab group       | 1 <= tab              |
tab group       | 0 <= desc     <= 1    |
tab group       | 0 <= search   <= 1    |
tab group       | 0 <= fmt      <= 1    |

tab             | 0 <= autonum     <= 1 |
tab             | 0 <= cols             |
tab             | 0 <= gps         <= 1 |
tab             | 0 <= author      <= 1 |
tab             | 0 <= timestamp   <= 1 |

GUI/data element | 0 <= desc     <= 1      |
GUI/data element | 0 <= opts     <= 1      |
GUI/data element | 0 <= str      <= 1      |
GUI/data element | 0 <= markdown <= 1      |

opts          | 1 <= opt              |

str            | 0 <= app <= 1         |
str            | 0 <= fmt <= 1         |
str            | 0 <= pos <= 1         |

col           | 1 <= GUI/data element      |

opt            | 0 <=  desc  <= 1      |
opt            | 0 <=  opt             |
'''

# Used by the validator suggest XML types
TYPES = '''
PARENT XML TYPE      | PATTERN     | MATCH XML TYPE
document             | /           | module

module               | /[^a-z]/    | tab group
module               | logic       | <logic>
module               | rels        | <rels>
module               | css         | <css>

tab group            | /[^a-z]/    | tab
tab group            | desc        | <desc>
tab group            | search      | <search>
tab group            | fmt         | <fmt>

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
GUI/data element     | markdown    | <markdown>

<str>                | app         | <app>
<str>                | fmt         | <fmt>
<str>                | pos         | <pos>

<opts>               | opt         | <opt>

<opt>                | opt         | <opt>

<opt>                | desc        | <desc>
'''

# Arch 16n entries which should be included in every module
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
Please_enter_data_first=Please enter data first and let a save occur.
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
The_current_record_has_not_been_saved_yet=The current record has not been saved yet. Press 'OK' to create a new record without waiting for any new data to be saved.
err_load_entity_head=Record Could Not Be Loaded
err_load_entity_body=A record with the provided UUID could not be found.
please_fill_out_the_following_fields=Please fill out the following fields:\\n
all_fields_contain_valid_data=All fields contain valid data!
validation_results=Validation Results



perf_mode_head=Performance Testing Mode Enabled
perf_mode_body=This module has been compiled with performance testing mode enabled. Performance testing mode adds some features which help to benchmark queries, however it may reduce the responsiveness of the module.\\n\\nTo disable performance testing mode, delete test_mode="true" from this module's module.xml file then recompile it.

perf_create_on_head=Record Creation Enabled!
perf_create_on_body=Record creation is now enabled during this session. Records can be created via the action bar.


perf_dummy_head=Create Dummy Records?
perf_dummy_body_1=Do you wish to create dummy records? Tapping 'OK' will create
perf_dummy_body_2=new entities. Entity creation takes a few minutes.\\n\\nIf you would not like to create any dummy records, tap 'Cancel' to dismiss this message.


perf_dummy_busy_head=Creating Entities...
perf_dummy_busy_body=entities are currently being created. This can take a few minutes. During this time the module may appear to freeze. Please wait.


perf_digest_1_head=Record Digest
perf_digest_1_body_1=entities have been successfully created.
perf_digest_1_body_2=The total number of entities on this device, by type, is as follows:\\n\\n

perf_digest_2_head=Display a Record Digest?
perf_digest_2_body=Would you like to display the number of records present on this device? Tap 'OK' to display them, or 'Cancel' to dismiss this message.


valid_control_head=Invalid Field(s) Found
valid_control_body_1=The following fields are invalid:\\n
valid_control_body_2=You must enter data into these fields to proceed.

this_module=this module
each=each


perf_rec_num_body_1=How many
perf_rec_num_body_2=records should be created in
perf_rec_num_body_3=?\\n\\nTap 'OK' to set a new value, or 'Cancel' to retain the previous one. Tap anywhere outside this dialogue box to dismiss it and skip this wizard's record creation step.

perf_wiz_head=Welcome to The Record Creation Wizard
perf_wiz_body=The record creation wizard will guide you through the process of creating dummy records.\\n\\nThe first step is to set the number of records you want to create. Tap 'OK' to do so, or 'Cancel' exit the wizard.

create_dummy_records=Create Dummy Records
display_record_digest=Display Record Digest
enable_record_creation=Enable Record Creation

perf_update_head=Update Successful
perf_update_body_1=The updated record quantities are as follows:\\n
perf_update_body_2=\\n\\nThese quantities will result in a total of
perf_update_body_3=records and
perf_update_body_4=photos being created. There is
perf_update_body_5=MB of free space on this device, of which the created photos will use
perf_update_body_6=MB.\\n\\nTap 'OK' to proceed, or 'Cancel' otherwise.


signup_head=Signup Successful
signup_body=You have successfuly signed up. You may now log in as the newly created user.

load_scanned_err_head=Could Not Load Record
load_scanned_err_body=No record could be found on this device which corresponds to the QR code or barcode you have scanned. This might be because this device has not been synchronised with the server. Synchronisation can be enabled via the action bar, which appears as an elipsis at the top-right of the screen. Please try scanning the QR code or barcode again once synchronisation is complete.

perf_dummy_err_head=Could Not Begin Record Creation Wizard
perf_dummy_err_body=The record creation wizard could not begin because syncing could not be automatically disabled. Please disable it manually and try again.

Saved_Map_Configuration=Saved Map Configuration
Loaded_Map_Configuration=Loaded Map Configuration

toast_saved=saved

inc_field_head=Starting ID Not Valid
inc_field_body_1=The starting ID for 
inc_field_body_2= should be an integer. The number you entered has been rounded before being incremented.
inc_field_body_3= should be an integer. The contents of this field could not be incremented.
'''

# Turn the string representations above into more expressive data types (e.g.
# tables get parsed into lists of lists).
ATTRIBS       = tablehelper.parseTable(ATTRIBS)
ATTRIB_VALS   = tablehelper.parseTable(ATTRIB_VALS)
CARDINALITIES = tablehelper.parseTable(CARDINALITIES)
TYPES         = tablehelper.parseTable(TYPES)
ARCH16N       = tablehelper.parseArch16n(ARCH16N)
