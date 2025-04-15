import io
import sys

fileIn = sys.argv[1]
serotype = sys.argv[2]
fh = open(fileIn+".csv")
fileOutUmap = serotype+"_umap.csv"
fileOutCellTypes = serotype+"_infected_cells.csv"
fhOutUmap = open(fileOutUmap, "w")
fhOutCellTypes = open(fileOutCellTypes, "w")

header_line = fh.readline()

fhOutCellTypes.write("serotype,cell_type," + ','.join(["10E"+x for x in header_line.rstrip().split(',')[4:]])+'\n')
fhOutUmap.write("umap1,umap2,cell_type\n")

bcs = header_line.rstrip().split(',')[-6:]

total_cells = 0

infected = {}

for line in fh:
	total_cells += 1

	pieces = line.rstrip().split(',')
	full_cell_id,umap1,umap2,celltype,e11,e7,e10,e8,e9,e12 = line.rstrip().split(',')
	if celltype not in infected:
		infected[celltype] = {}
		infected[celltype]['7'] = [float(e7)]
		infected[celltype]['8'] = [float(e8)]
		infected[celltype]['9'] = [float(e9)]
		infected[celltype]['10'] = [float(e10)]
		infected[celltype]['11'] = [float(e11)]
		infected[celltype]['12'] = [float(e12)]
	else:
		infected[celltype]['7'].append(float(e7))
		infected[celltype]['8'].append(float(e8))
		infected[celltype]['9'].append(float(e9))
		infected[celltype]['10'].append(float(e10))
		infected[celltype]['11'].append(float(e11))
		infected[celltype]['12'].append(float(e12))

	for celltype in infected:
		fhOutCellTypes.write(serotype +','+ celltype +',')
		for titer in bcs:
			fhOutCellTypes.write(sum(infected[celltype][titer])/len(infected[celltype][titer]))

	#fhOutCellTypes.write(serotype + "," + ','.join(pieces[3:-6]) + ',' + ','.join(['1' if x=="True" else '0' for x in pieces[-6:]]) + "\n")

	fhOutUmap.write(','.join(pieces[1:-6])+"\n")
	if 'True' in pieces[-6:]:
		for i in range(-6,0):
			if pieces[i] == 'True':
				infected_cell = pieces
				infected_cell[3] = "Cells infected at AAV titer 10^" + bcs[i]
				fhOutUmap.write(','.join(infected_cell[1:-6])+"\n")
fh.close()
fhOutUmap.close()
fhOutCellTypes.close()
