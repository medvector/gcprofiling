from sys import argv  
import re
def main():
	f = open(argv[1], "r")
	text = f.readlines()
	f.close()
	m = re.compile(r"(\d*,\d*): \[(Full )?GC (\d*)K->(\d*)K\((\d*)K\), (\d*,\d*) secs\]$")
	l = []
	for line in text:
		l.append(m.search(line))
	s = "data"
	i = 0
	script = open("data.sh", "w")
	prolog = '''#!/bin/bash

gnuplot << EOP

set terminal jpeg size 1300,200
set output "time.jpg"
set xtics 0.05
set mxtics 10
set format x "%4.3f"
set grid x y 
set grid mxtics 
plot '''
	script.write(prolog)
	for match in l:
		starttime = match.group(1).replace(',', '.')
		duration = match.group(6).replace(',', '.')
		endtime = float(starttime) + float(duration)
		g = open(s + str(i), "w")
		g.write(starttime + " 1\n")
		g.write(str(endtime) +" 1\n")
		g.close()
		if (i != 0):
			script.write(", ")
		script.write('"' + s + str(i) + '" w l lw 7 notitle')
		i += 1
	script.write("\n \nEOP\n")
	script.close()
if __name__ == '__main__':
	main()