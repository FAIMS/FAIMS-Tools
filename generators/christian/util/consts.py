RESERVED_XML_TYPE  = '__RESERVED_XML_TYPE__'
RESERVED_IGNORE    = '__RESERVED_IGNORE__'
RESERVED_PROP_NAME = '__RESERVED_PROP_NAME__'

SEP_FLAGS = ' ' # What's considered a separator in the `f` attribute
SEP_DATA  = ' ' # Used to separate archent name from attrib name during data
                # schema generation

# XML attributes which the user can use in the `module.xml` file.
ATTRIB_B         = 'b'
ATTRIB_C         = 'c'
ATTRIB_E         = 'e'
ATTRIB_EC        = 'ec'
ATTRIB_F         = 'f'
ATTRIB_I         = 'i'
ATTRIB_L         = 'l'
ATTRIB_LC        = 'lc'
ATTRIB_LCQ       = 'lcq'
ATTRIB_LL        = 'll'
ATTRIB_LQ        = 'lq'
ATTRIB_P         = 'p'
ATTRIB_S         = 's'
ATTRIB_SP        = 'sp'
ATTRIB_SU        = 'su'
ATTRIB_T         = 't'
ATTRIB_TEST_MODE = 'test_mode'
ATTRIB_VP        = 'vp'
ATTRIBS = [
        v for k, v in dict(globals()).iteritems()
        if k.startswith('ATTRIB_')
]

LINK_ATTRIBS = [
        v for k, v in dict(globals()).iteritems()
        if k.startswith('ATTRIB_L')
]

BIND_DATE    = 'date'
BIND_DECIMAL = 'decimal'
BIND_INTEGER = 'integer'
BIND_LONG    = 'long'
BIND_STRING  = 'string'
BIND_TIME    = 'time'
BINDS = [
        v for k, v in dict(globals()).iteritems()
        if k.startswith('BIND_')
]

CSS_REQUIRED = 'required'
CSS = [
        v for k, v in dict(globals()).iteritems()
        if k.startswith('CSS_')
]

# Strings which the user is allowed to include in the `module.xml` file's `f`
# attribute.
FLAG_AUTONUM      = 'autonum'
FLAG_HIDDEN       = 'hidden'
FLAG_HTMLDESC     = 'htmldesc'
FLAG_ID           = 'id'
FLAG_NOANNOTATION = 'noannotation'
FLAG_NOAUTOSAVE   = 'noautosave'
FLAG_NOCERTAINTY  = 'nocertainty'
FLAG_NODATA       = 'nodata'
FLAG_NOLABEL      = 'nolabel'
FLAG_NOSCROLL     = 'noscroll'
FLAG_NOSYNC       = 'nosync'
FLAG_NOTHUMB      = 'nothumb'
FLAG_NOTHUMBNAIL  = 'nothumbnail'
FLAG_NOTNULL      = 'notnull'
FLAG_NOUI         = 'noui'
FLAG_NOWIRE       = 'nowire'
FLAG_PERSIST      = 'persist'
FLAG_PERSIST_OW   = 'persist!'
FLAG_READONLY     = 'readonly'
FLAG_USER         = 'user'
FLAGS = [
        v for k, v in dict(globals()).iteritems()
        if k.startswith('FLAG_')
]

# Tags which the user can use in the `module.xml` file.
TAG_APP       = 'app'
TAG_AUTHOR    = 'author'
TAG_AUTONUM   = 'autonum'
TAG_COL       = 'col'
TAG_COLS      = 'cols'
TAG_CSS       = 'css'
TAG_DESC      = 'desc'
TAG_FMT       = 'fmt'
TAG_GPS       = 'gps'
TAG_GROUP     = 'group'
TAG_LOGIC     = 'logic'
TAG_MARKDOWN  = 'markdown'
TAG_MODULE    = 'module'
TAG_OPT       = 'opt'
TAG_OPTS      = 'opts'
TAG_POS       = 'pos'
TAG_RELS      = 'rels'
TAG_SEARCH    = 'search'
TAG_STR       = 'str'
TAG_TIMESTAMP = 'timestamp'
TAGS = [
        v for k, v in dict(globals()).iteritems()
        if k.startswith('TAG_')
]

# XML Types -- If `module.xml` had an idiomatic XML schema, these wouldn't be
# needed because whoever writes the `module.xml` file would explicitly provide
# the so called "XML types" as XML tags. For instance,
#
#     <My_Tabgroup>
#       <My_Tab f="noscroll">
#         <My_Input t="input"/>
#       </My_Tab>
#     </My_Tabgroup>
#
# would look more like:
#
#     <tab-group name="My Tabgroup">
#       <tab name="My Tab" f="noscroll">
#         <gui-data-element name="My Input" t="input"/>
#       </tab>
#     </tab-group>
#
# Because the types aren't explicitly provided by the user, they need to be
# inferred by running `annotateWithXmlTypes`. One might expect that this
# transforms the first form (above) to the second. However
# `annotateWithXmlTypes` instead puts the XML types in an attribute named by the
# `RESERVED_XML_TYPE` variable.
#
# The reason for this weirdness is twofold: 1) it makes it easier to port old
# modules to the `module.xml` format because the latter is similar to the
# former's `ui_schema.xml`. 2) It makes the `module.xml` more concise. If either
# of these weren't the case, it'd be undeniably better to have defined
# `module.xml`'s schema idiomatically.
TYPE_CSS       = 'css'
TYPE_APP       = 'app'
TYPE_AUTHOR    = 'author'
TYPE_AUTONUM   = 'autonum'
TYPE_COL       = 'col'
TYPE_COLS      = 'cols'
TYPE_DESC      = 'desc'
TYPE_FMT       = 'fmt'
TYPE_GPS       = 'gps'
TYPE_GROUP     = 'group'
TYPE_GUI_DATA  = 'GUI/data element'
TYPE_LOGIC     = 'logic'
TYPE_MARKDOWN  = 'markdown'
TYPE_MODULE    = 'module'
TYPE_OPT       = 'opt'
TYPE_OPTS      = 'opts'
TYPE_POS       = 'pos'
TYPE_RELS      = 'rels'
TYPE_SEARCH    = 'search'
TYPE_STR       = 'str'
TYPE_TAB       = 'tab'
TYPE_TAB_GROUP = 'tab group'
TYPE_TIMESTAMP = 'timestamp'
TYPES = [
        v for k, v in dict(globals()).iteritems()
        if k.startswith('TYPE_')
]

# UI Types -- These are the strings which can appear in the `module.xml` file's
# `t` attribute.
UI_TYPE_AUDIO     = 'audio'
UI_TYPE_BUTTON    = 'button'
UI_TYPE_CAMERA    = 'camera'
UI_TYPE_CHECKBOX  = 'checkbox'
UI_TYPE_DROPDOWN  = 'dropdown'
UI_TYPE_FILE      = 'file'
UI_TYPE_GPSDIAG   = 'gpsdiag'
UI_TYPE_GROUP     = 'group'
UI_TYPE_INPUT     = 'input'
UI_TYPE_LIST      = 'list'
UI_TYPE_MAP       = 'map'
UI_TYPE_PICTURE   = 'picture'
UI_TYPE_RADIO     = 'radio'
UI_TYPE_TABLE     = 'table'
UI_TYPE_VIDEO     = 'video'
UI_TYPE_VIEWFILES = 'viewfiles'
UI_TYPE_WEB       = 'web'
UI_TYPE_WEBVIEW   = 'webview'
UI_TYPES = [
        v for k, v in dict(globals()).iteritems()
        if k.startswith('UI_TYPES_')
]

# Types (t attribute in module.xml schema) of menu-like items
MENU_UI_TYPES = [
        UI_TYPE_CHECKBOX,
        UI_TYPE_DROPDOWN,
        UI_TYPE_LIST,
        UI_TYPE_PICTURE,
        UI_TYPE_RADIO,
]

MEDIA_UI_TYPES = [
        UI_TYPE_AUDIO,
        UI_TYPE_CAMERA,
        UI_TYPE_FILE,
        UI_TYPE_VIDEO,
]

FILE_UI_TYPES = [
        UI_TYPE_AUDIO,
        UI_TYPE_CAMERA,
        UI_TYPE_FILE,
        UI_TYPE_VIDEO,
]

MEASURE_UI_TYPES = [
        UI_TYPE_INPUT
]

# UI types of composite elements. These will be expanded into multiple GUI/Data
# elements as the module is generated.
GUI_DATA_UI_TYPES = [
        TYPE_AUTHOR,
        TYPE_GPS,
        TYPE_GROUP,
        TYPE_GUI_DATA,
        TYPE_TIMESTAMP,
]

# UI types of GUI/Data elements whose parent tabs shoudl probably be flagged
# with `f="noscroll"` to avoid layout issues.
NO_SCROLL_UI_TYPES = [
        UI_TYPE_MAP,
        UI_TYPE_LIST,
]

# Types (t attribute in module.xml schema) where <desc> is allowed to go
DATA_UI_TYPES = [
    UI_TYPE_AUDIO,
    UI_TYPE_CAMERA,
    UI_TYPE_CHECKBOX,
    UI_TYPE_DROPDOWN,
    UI_TYPE_FILE,
    UI_TYPE_INPUT,
    UI_TYPE_LIST,
    UI_TYPE_PICTURE,
    UI_TYPE_RADIO,
    UI_TYPE_VIDEO
]

ORIGINAL_TAG = '__ORIGINAL_TAG__'
AUTONUM_DEST = '__AUTONUM_DEST__'
LINK_SIGNUP  = 'signup'
