import gcstat
import re

def getMaxPause(collections):
	list = []
	for collection in collections:
		list.append(collection.duration)
	maxcol = max(list)
	for collection in collections:
		if (collection.duration == maxcol):
			return collection

def getSum(collections):
	sum = 0
	for collection in collections:
		sum += float(collection.duration)
	return sum

def getAveragePause(collections):
	return getSum(collections)/len(collections)

def getNumCollections(collections):
	return len(collections)

def getProcentTime(collections):
	return 100*getSum(collections)/(collections[len(collections) - 1].endtime)

def getYoungGCNum(collections):
	i = 0
	for collection in collections:
		if (collection.type == "minor"):
			i += 1
	return i
def getFullGCNum(collections):
	return len(collections) - getYoungGCNum(collections)

def getCollectionGCNum(collections):
	i = 0
	for collection in collections:
		if (collection.type == "collection"):
			i += 1
	return i

def getNonCollectionNum(collections):
	return len(collections) - getCollectionGCNum(collections)

def getMaxMemDistibution(collections):
	tmp1 = 100*float(collections[0].beforeMem)/float(collections[0].totalMem)
	tmp2 = 100*float(collections[0].afterMem)/float(collections[0].totalMem)
	dist = max(tmp1, tmp2)
	for i in xrange(1, len(collections)):
		tmp1 = 100*float(collections[i].beforeMem)/float(collections[i-1].totalMem)
		tmp2 = 100*float(collections[i].afterMem)/float(collections[i].totalMem)
		tmp3 = max(tmp1, tmp2)
		dist = max(dist, tmp3)
	return dist

def getMaxMemDistibutionCMS(collections):
	if (collections[0].type == "collection"):
		tmp1 = 100*float(collections[0].beforeMem)/float(collections[0].totalMem)
		tmp2 = 100*float(collections[0].afterMem)/float(collections[0].totalMem)
		dist = max(tmp1, tmp2)
	else:
		dist = 100*float(collections[0].used)/float(collections[0].totalMem)
	for i in xrange(1, len(collections)):
		if (collections[i].type == "collection"):
			tmp1 = 100*float(collections[i].beforeMem)/float(collections[i-1].totalMem)
			tmp2 = 100*float(collections[i].afterMem)/float(collections[i].totalMem)
			tmp3 = max(tmp1, tmp2)
			dist = max(dist, tmp3)
		else:
			tmp = 100*float(collections[i].used)/float(collections[i].totalMem)
			dist = max(dist, tmp)
	return dist

def getMinMemDistibution(collections):
	tmp1 = 100*float(collections[0].beforeMem)/float(collections[0].totalMem)
	tmp2 = 100*float(collections[0].afterMem)/float(collections[0].totalMem)
	dist = min(tmp1, tmp2)
	for i in xrange(1, len(collections)):
		tmp1 = 100*float(collections[i].beforeMem)/float(collections[i-1].totalMem)
		tmp2 = 100*float(collections[i].afterMem)/float(collections[i].totalMem)
		tmp3 = min(tmp1, tmp2)
		dist = min(dist, tmp3)
	return dist
def getMinMemDistibutionCMS(collections):
	if (collections[0].type == "collection"):
		tmp1 = 100*float(collections[0].beforeMem)/float(collections[0].totalMem)
		tmp2 = 100*float(collections[0].afterMem)/float(collections[0].totalMem)
		dist = min(tmp1, tmp2)
	else:
		dist = 100*float(collections[0].used)/float(collections[0].totalMem)
	for i in xrange(1, len(collections)):
		if (collections[i].type == "collection"):
			tmp1 = 100*float(collections[i].beforeMem)/float(collections[i-1].totalMem)
			tmp2 = 100*float(collections[i].afterMem)/float(collections[i].totalMem)
			tmp3 = min(tmp1, tmp2)
			dist = min(dist, tmp3)
		else:
			tmp = 100*float(collections[i].used)/float(collections[i].totalMem)
			dist = min(dist, tmp)
	return dist

def getAverageMemDistibution(collections):
	tmp1 = 100*float(collections[0].beforeMem)/float(collections[0].totalMem)
	tmp2 = 100*float(collections[0].afterMem)/float(collections[0].totalMem)
	sumdist = tmp1 + tmp2
	for i in xrange(1, len(collections)):
		tmp1 = 100*float(collections[i].beforeMem)/float(collections[i-1].totalMem)
		tmp2 = 100*float(collections[i].afterMem)/float(collections[i].totalMem)
		tmp3 = tmp1 + tmp2
		sumdist += tmp3
	return sumdist/(2*len(collections))

def getAverageMemDistibutionCMS(collections):
	c = 0
	if (collections[0].type == "collection"):
		c += 1 
		tmp1 = 100*float(collections[0].beforeMem)/float(collections[0].totalMem)
		tmp2 = 100*float(collections[0].afterMem)/float(collections[0].totalMem)
		dist = tmp1 + tmp2
	else:
		dist = 100*float(collections[0].used)/float(collections[0].totalMem)
	for i in xrange(1, len(collections)):
		if (collections[i].type == "collection"):
			c += 1
			tmp1 = 100*float(collections[i].beforeMem)/float(collections[i-1].totalMem)
			tmp2 = 100*float(collections[i].afterMem)/float(collections[i].totalMem)
			tmp3 = tmp1 + tmp2
			dist += tmp3
		else:
			tmp = 100*float(collections[i].used)/float(collections[i].totalMem)
			dist += tmp
	return dist/ (len(collections) + c)
		
def parseSerialGC(filename, collections):
	f = open(filename, "r")
	text = f.readlines()
	f.close()
	m = re.compile(r"(\d*,\d*): \[(Full )?GC (\d*)K->(\d*)K\((\d*)K\), (\d*,\d*) secs\]$")
	l = []
	for line in text:
		l.append(m.search(line))
	i = 0
	for match in l:
		starttime = match.group(1).replace(',', '.')
		duration = match.group(6).replace(',', '.')
		beforeMem = match.group(3)
		afterMem = match.group(4)
		totalMem = match.group(5)
		used = 0
		type = "major" if match.group(2) == "Full " else "minor"
		collections.append(gcstat.gcstat(i, starttime, duration, type, beforeMem,\
			afterMem, totalMem, used, "serial"))
		i += 1
def parseCMS(filename, collections):
	f = open(filename, "r")
	text = f.readlines()
	f.close()
	m = re.compile(r"(\d*,\d*): \[GC (\d*)K(\((\d*)K\))?(->(\d*)K\((\d*)K\))?, (\d*,\d*) secs\]$")
	l = []
	for line in text:
		l.append(m.search(line))
	i = 0
	for match in l:
		starttime = match.group(1).replace(',', '.')
		duration = match.group(8).replace(',', '.')
		if (match.group(3)):
			used = match.group(2)
			totalMem = match.group(4)
			beforeMem = 0 
			afterMem = 0
			type = 1
		else:
			beforeMem = match.group(2) 
			afterMem = match.group(6)
			totalMem = match.group(7)
			used = 0
			type = 0
		realType = "collection" if type == 0 else "non-collection phase"
		collections.append(gcstat.gcstat(i, starttime, duration, realType, beforeMem,\
			afterMem, totalMem, used, "CMS"))
		i += 1

def parseG1(filename, collections):
	f = open(filename, "r")
	text = f.readlines()
	f.close()
	m = re.compile(r"(\d*,\d*): \[(Full )?GC (\(System.gc\(\)\) )?(pause \(young\) )?(\d*)([KM])->(\d*)([KM])\((\d*)([KM])\), (\d*,\d*) secs\]$")
	l = []
	for line in text:
		l.append(m.search(line))
	i = 0
	for match in l:
		starttime = match.group(1).replace(',', '.')
		duration = match.group(11).replace(',', '.')
		beforeMem = match.group(5)
		if (match.group(6) == "M"):
			beforeMem = int(beforeMem) * 1024
		afterMem = match.group(7)
		if (match.group(8) == "M"):
			afterMem = int(afterMem) * 1024
		totalMem = match.group(9)
		if (match.group(10) == "M"):
			totalMem = int(totalMem) * 1024
		used = 0
		type = "major" if match.group(2) == "Full " else "minor"
		collections.append(gcstat.gcstat(i, starttime, duration, type, beforeMem,\
			afterMem, totalMem, used, "serial"))
		i += 1	

def makeMemPlot(collections, plotname):
	script = open("data.sh", "w")
	prolog = '''#!/bin/bash

gnuplot << EOP

set terminal jpeg font arial 27 size 1500,1000
set output ''' + '''"''' + plotname+ '''.jpg"
set xtics 0.5 in
set border linewidth 3
set xtics font "Arial, 27" 
set xlabel font "Times-Roman, 30" 
set ylabel font "Times-Roman, 26" 
set xlabel "time"
set ylabel "memory"
set mxtics 2
set format x "%4.1f"
set grid x y 
set grid mxtics 
set title font "Times-Roman, 26" 
plot '''
	script.write(prolog)
	g = open("data-mem", "w")
	h = open("data-totalmem", "w")
	for collection in collections:
		g.write(str(collection.starttime) + " " + str(collection.beforeMem) +" \n")
		g.write(str(collection.endtime) + " "+ str(collection.afterMem)+ " \n")
		h.write(str(collection.starttime) + " " + str(collection.totalMem) + "\n")
	g.close()
	h.close()
	script.write('"' + "data-mem" + '" w l lw 7 title "used memory", ' \
		+ '"' + "data-totalmem" + '" w l lw 7 title "total memory"')
	script.write("\n \nEOP\n")
	script.write("rm data-*\n")
	script.close()

def makeMemPlotCMS(collections, plotname):
	script = open("data.sh", "w")
	prolog = '''#!/bin/bash

gnuplot << EOP

set terminal jpeg size 1500,1000
set output ''' + '''"''' + plotname+ '''.jpg"
set xtics 0.1 in
set xlabel "time"
set ylabel "memory"
set mxtics 2
set format x "%4.3f"
set grid x y 
set grid mxtics 
plot '''
	script.write(prolog)
	g = open("data-mem", "w")
	h = open("data-totalmem", "w")
	for collection in collections:
		if (collection.type == "collection"):
			g.write(str(collection.starttime) + " " + str(collection.beforeMem) +" \n")
			g.write(str(collection.endtime) + " "+ str(collection.afterMem)+ " \n")
			h.write(str(collection.starttime) + " " + str(collection.totalMem) + "\n")
		else:
			g.write(str(collection.starttime) + " " + str(collection.used) + " \n")
			h.write(str(collection.starttime) + " " + str(collection.totalMem + " \n")) 
	g.close()
	h.close()
	script.write('"' + "data-mem" + '" w l lw 1 title "used memory", ' \
		+ '"' + "data-totalmem" + '" w l lw 1 title "total memory"')
	script.write("\n \nEOP\n")
	script.write("rm data-*\n")
	script.close()	

def makeTimePlot(collections, plotname):
	s = "tmp"
	script = open("data.sh", "w")
	prolog = '''#!/bin/bash

gnuplot << EOP

set terminal jpeg size 900,200
set output ''' + '''"'''+ plotname +'''.jpg"
set xtics 0.5 in
set xlabel "time"
set ylabel "GC type"
set yrange[0:2]
set ytics ("Major" 2, "Minor" 1)
set mxtics 5
set format x "%4.3f"
set grid x y 
set grid mxtics 
plot '''
	script.write(prolog)
	for gccollection in collections:
		g = open(s + str(gccollection.id), "w")
		val = 1 if gccollection.type == "minor" else 2
		g.write(str(gccollection.starttime) + " " + str(val) +" \n")
		g.write(str(gccollection.endtime) + " "+ str(val) + " \n")
		g.close()
		if (gccollection.id != 0):
			script.write(", ")
		script.write('"' + s + str(gccollection.id) + '" w l lw 7 notitle')
	script.write("\n \nEOP\n")
	script.write("rm tmp*\n")
	script.close()

def makeTimePlotCMS(collections, plotname):
	s = "tmp"
	script = open("data.sh", "w")
	prolog = '''#!/bin/bash

gnuplot << EOP

set terminal jpeg size 900,200
set output ''' + '''"'''+ plotname +'''.jpg"
set xtics 0.1 in
set xlabel "time"
set ylabel "GC type"
set yrange[0:2]
set ytics ("GC Collection" 2, "non-collection" 1)
set mxtics 5
set format x "%4.3f"
set grid x y 
set grid mxtics 
plot '''
	script.write(prolog)
	for gccollection in collections:
		g = open(s + str(gccollection.id), "w")
		val = 1 if gccollection.type == "non-collection phase" else 2
		g.write(str(gccollection.starttime) + " " + str(val) +" \n")
		g.write(str(gccollection.endtime) + " "+ str(val) + " \n")
		g.close()
		if (gccollection.id != 0):
			script.write(", ")
		script.write('"' + s + str(gccollection.id) + '" w l lw 7 notitle')
	script.write("\n \nEOP\n")
	script.write("rm tmp*\n")
	script.close()

