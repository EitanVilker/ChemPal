from mendeleev import element
import csv

# open the file in the write mode
f = open('element.csv', 'w')

# create the csv writer
writer = csv.writer(f)

for i in range(118):
	e = element(i+1)
	if e:
		row = ["ChemicalElement", e.symbol, e.name]
		writer.writerow(row)

f.close()
