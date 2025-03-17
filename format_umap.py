import io
import sys

fileIn = sys.argv[1]
fh = open(fileIn)
fileOutUmap = "umap_"+fileIn
fileOutInfecBar = "infect_"+fileIn
fhOutUmap = open(fileOutUmap, "w")
fhOutInfecBar = open(fileOutInfecBar, "w")

header_line = fh.readline()
fhOutUmap.write("umap1,umap2,cell_type\n")
bcs = header_line.rstrip().split(',')[-6:]
print(bcs)

total_cells = 0

infected = []

for line in fh:
	total_cells += 1

	pieces = line.rstrip().split(',')
	fhOutUmap.write(','.join(pieces[1:-6])+"\n")
	if 'True' in pieces[-6:]:
		for i in range(-6,0):
			if pieces[i] == 'True':
				infected_cell = pieces
				infected_cell[3] = "Cells infected at AAV titer 10^" + bcs[i]
				fhOutUmap.write(','.join(infected_cell[1:-6])+"\n")
fh.close()
fhOutUmap.close()
fhOutInfecBar.close()
