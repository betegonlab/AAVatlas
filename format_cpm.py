import io
import sys

titers = ['e7','e8','e9','e10','e11','e12','e13']

fileIn = sys.argv[1]
if fileIn[-5:] != '.orig':
    print("Input file must have .orig extension")
    exit()
fh = open(fileIn)
fileOut = fileIn[:-5]
print(fileOut)

fhOut = open(fileOut, "w")
serotype = ''
header_line = fh.readline()
fhOut.write('serotype,cell_type,'+','.join(titers)+"\n")

data = {}
for line in fh:
    serotype_titer, cell_type, cells, cpm = line.strip().split(',')
    serotype, titer = serotype_titer.split('_')
    if cell_type not in data:
        data[cell_type] = {}
    data[cell_type][titer] = cpm


for ct in data:
    cpms = []
    for t in titers:
        if t in data[ct]:
            cpms.append(data[ct][t])
        else:
            cpms.append('0')
    dataline = ','.join([serotype, ct, ','.join(cpms)])
    fhOut.write(dataline+"\n")

fh.close()
