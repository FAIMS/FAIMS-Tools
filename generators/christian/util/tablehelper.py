import re

def parseTable(table):
    table = table.strip()
    table = table.split('\n')
    table = table[1:]
    table = [re.split(' *\| *', i) for i in table]
    table = [i for i in table if i != ['']]
    for rowIdx in range(len(table)):
        for colIdx in range(len(table[rowIdx])):
            cell = table[rowIdx][colIdx]
            if re.match('.*,', cell):
                table[rowIdx][colIdx] = [x.strip() for x in cell.split(',')]

    # Special treatment of tables with cardinalities
    hasCardinalities = False
    for i in range(len(table)):
        for j in range(1, len(table[i])):
            if '<=' in table[i][j]:
                hasCardinalities |= True
    if not hasCardinalities:
        return table

    for i in range(len(table)):
        for j in range(1, len(table[i])):
            regMin  = '(([0-9]+)\s+<=\s+)?'
            regType = '(\<?[a-zA-Z][a-zA-Z \/]*[a-zA-Z]\>?)'
            regMax  = '(\s+<=\s+([0-9]+))?'
            reg     = regMin + regType + regMax
            m = re.search(reg, table[i][j])

            if m:
                min  = m.group(2)
                type = m.group(3)
                max  = m.group(5)

                if min:
                    min = int(min)
                if max:
                    max = int(max)

                lim = [min,  type, max]
            else:
                lim = [None, None, None]

            table[i][j] = lim
    return table

def parseArch16n(arch16n):
    arch16nLines = arch16n.splitlines()
    arch16nDict = {}

    for line in arch16nLines:
        splittedLine = line.split('=', 1)

        if len(splittedLine) != 2:
            continue

        key, val = splittedLine
        arch16nDict[key] = val

    return arch16nDict
