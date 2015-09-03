import sys

def parseArchLine(line):
    parsed = line.split('=')

    # Normalisation steps
    if len(parsed) < 2:                                                      # 1
        parsed = ['', '']
    parsed[1] = parsed[1].replace('\n', '')                                  # 2

    return parsed

################################################################################
#                                     MAIN                                     #
################################################################################
if len(sys.argv) < 2:
    sys.stderr.write('Specify arch16n file as argument\n')
    exit()
archFilename = sys.argv[1]

archKV = {}

# Load arch16n file into dict
for line in open(archFilename, 'r'):
    k, v = parseArchLine(line)
    if k == '':
        continue
    archKV[k] = v

# Transform dict to sorted list
archLines = []
for k, v in archKV.iteritems():
    archLines.append(k + "=" + v)
archLines.sort()

# Print list of arch16n entires
for line in archLines:
    print line
