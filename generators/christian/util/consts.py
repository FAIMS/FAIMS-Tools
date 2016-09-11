RESERVED_XML_TYPE = '__RESERVED_XML_TYPE__'
RESERVED_IGNORE   = '__RESERVED_IGNORE__'



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
