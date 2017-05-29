RESERVED_XML_TYPE = '__RESERVED_XML_TYPE__'
RESERVED_IGNORE   = '__RESERVED_IGNORE__'

SEP_FLAGS = ' '

ATTRIB_TEST_MODE = 'test_mode'
ATTRIB_B         = 'b'
ATTRIB_C         = 'c'
ATTRIB_E         = 'e'
ATTRIB_EC        = 'ec'
ATTRIB_F         = 'f'
ATTRIB_I         = 'i'
ATTRIB_L         = 'l'
ATTRIB_LL        = 'll'
ATTRIB_LC        = 'lc'
ATTRIB_LQ        = 'lq'
ATTRIB_P         = 'p'
ATTRIB_S         = 's'
ATTRIB_T         = 't'
ATTRIB_VP        = 'vp'
ATTRIBS = [
        v for k, v in dict(globals()).iteritems()
        if k.startswith('ATTRIB_')
]

BIND_DATE    = 'date'
BIND_DECIMAL = 'decimal'
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


FLAG_AUTONUM      = 'autonum'
FLAG_HIDDEN       = 'hidden'
FLAG_ID           = 'id'
FLAG_NOANNOTATION = 'noannotation'
FLAG_NOCERTAINTY  = 'nocertainty'
FLAG_NODATA       = 'nodata'
FLAG_NOLABEL      = 'nolabel'
FLAG_NOSCROLL     = 'noscroll'
FLAG_NOSYNC       = 'nosync'
FLAG_NOTHUMB      = 'nothumb'
FLAG_NOTHUMBNAIL  = 'nothumbnail'
FLAG_NOTNULL      = 'notnull'
FLAG_NOUI         = 'noui'
FLAG_PERSIST      = 'persist'
FLAG_PERSIST_OW   = 'persist!'
FLAG_READONLY     = 'readonly'
FLAG_USER         = 'user'
FLAGS = [
        v for k, v in dict(globals()).iteritems()
        if k.startswith('FLAG_')
]

TAG_APP       = 'app'
TAG_AUTHOR    = 'author'
TAG_AUTONUM   = 'autonum'
TAG_COLS      = 'cols'
TAG_COL       = 'col'
TAG_DESC      = 'desc'
TAG_FMT       = 'fmt'
TAG_GPS       = 'gps'
TAG_GROUP     = 'group'
TAG_LOGIC     = 'logic'
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

TYPE_APP       = 'app'
TYPE_AUTHOR    = 'author'
TYPE_AUTONUM   = 'autonum'
TYPE_COLS      = 'cols'
TYPE_COL       = 'col'
TYPE_DESC      = 'desc'
TYPE_FMT       = 'fmt'
TYPE_GPS       = 'gps'
TYPE_GROUP     = 'group'
TYPE_GUI_DATA  = 'GUI/data element'
TYPE_LOGIC     = 'logic'
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
UI_TYPE_VIDEO     = 'video'
UI_TYPE_VIEWFILES = 'viewfiles'
UI_TYPE_WEB       = 'web'
UI_TYPE_WEBVIEW   = 'webview'
UI_TYPES = [
        v for k, v in dict(globals()).iteritems()
        if k.startswith('UI_TYPES_')
]

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

GUI_DATA_UI_TYPES = [
        TYPE_AUTHOR,
        TYPE_COLS,
        TYPE_GPS,
        TYPE_GROUP,
        TYPE_GUI_DATA,
        TYPE_TIMESTAMP,
]

ORIGINAL_TAG = '__ORIGINAL_TAG__'
AUTONUM_DEST = '__AUTONUM_DEST__'
LINK_SIGNUP  = 'signup'
