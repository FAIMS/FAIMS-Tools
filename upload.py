import cookielib
import mechanize
import os
import sys
import urllib2
from   mimetypes import MimeTypes

################################################################################

filenameArch16n    = 'english.0.properties'
filenameCss        = 'ui_styling.css'
filenameDataSchema = 'data_schema.xml'
filenameUiLogic    = 'ui_logic.bsh'
filenameUiSchema   = 'ui_schema.xml'
filenameValidation = 'validation.xml'

filenames = [
        filenameArch16n,
        filenameCss,
        filenameDataSchema,
        filenameUiLogic,
        filenameUiSchema,
        filenameValidation]

username = 'faimsadmin@intersect.org.au'
password = 'Pass.123'

server = 'dev'
url    = 'http://%s.fedarch.org' % server

################################################################################

# The module location can be set manually or be determined automatically
if len(sys.argv) > 1:
    # Set module location from manually-given argument
    moduleLocation = sys.argv[1]
    moduleLocation = os.path.abspath(moduleLocation)
else:
    # Set module location to that of this script
    moduleLocation = os.path.realpath(__file__)
    moduleLocation = os.path.dirname(moduleLocation)
# Determine module name
moduleName = moduleLocation.split(os.sep)
moduleName = moduleName[-1]

# Check that all the given paths really exist
if not os.path.exists(moduleLocation):
    print 'ERROR: given module location does not exist'
    exit()

isMissing = False
for f in filenames:
    if not os.path.exists(moduleLocation + os.sep + f):
        print 'ERROR: Cannot find %s' % f
        isMissing = True
if isMissing:
    exit()

# Initialisation of `magic` module
mime = MimeTypes()
mime.add_type('text/plain', '.bsh')
mime.add_type('text/plain', '.properties')

# Make browser
br = mechanize.Browser()

# Initialisation of `mechanize` module (Some stuff I copied from Stack Overflow)
cookiejar = cookielib.LWPCookieJar()
br.set_cookiejar      (cookiejar)
br.set_handle_gzip    (True)
br.set_handle_equiv   (True)
br.set_handle_gzip    (True)
br.set_handle_redirect(True)
br.set_handle_referer (True)
br.set_handle_robots  (False)

################################################################################

def addFile(br, filename, inputName):
    fullFilename = moduleLocation + os.sep + filename
    mimetype     = mime.guess_type(filename)
    mimetype     = mimetype[0]

    br.form.add_file(open(fullFilename), mimetype, filename, name=inputName)

def addFiles(br, doUploadDataSchema):
    addFile    (br, filenameArch16n    , 'project_module[arch16n]')
    addFile    (br, filenameCss        , 'project_module[css_style]')
    if doUploadDataSchema:
        addFile(br, filenameDataSchema , 'project_module[data_schema]')
    addFile    (br, filenameUiLogic    , 'project_module[ui_logic]')
    addFile    (br, filenameUiSchema   , 'project_module[ui_schema]')
    addFile    (br, filenameValidation , 'project_module[validation_schema]')

################################################################################

# Get login form and fill it out
print 'Creating/uploading module with the name "%s"...' % moduleName
print

print 'Downloading login form...'
res = br.open(url)

br.select_form(nr=0)
br['user[email]']    = username
br['user[password]'] = password

# Submit yer good ol' form
print 'Submitting login form...'
print
res = br.submit()

# Determine if module's already been uploaded. (Yes, I know I've misused the
# try-except statement.)
print 'Downloading update/create form...'
try:
    # The module's already been uploaded
    linkText = moduleName
    res      = br.follow_link(text_regex=linkText)

    linkText = 'Edit Module'
    res      = br.follow_link(text_regex=linkText)

    print 'Submitting update form...'
    print
    br.select_form(nr=0)
    addFiles(br, doUploadDataSchema=False)
    res = br.submit()
except:
    # We need to create a new module
    linkText = 'Create Module'
    res      = br.follow_link(text_regex=linkText)

    print 'Submitting create form...'
    print
    br.select_form(nr=0)
    br['project_module[name]'] = moduleName
    addFiles(br, doUploadDataSchema=True)
    res = br.submit()
print 'All done!'
