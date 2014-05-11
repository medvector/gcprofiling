from sys import argv

def get_diff_time(time1, time2):
    diff_sec = time2[0] - time1[0]
    diff_nsec = time2[1] - time1[1]
    if diff_nsec < 0:
        diff_sec = diff_sec - 1
        diff_nsec += 1000000
    return (diff_sec, diff_nsec)

def parse(f):
    isfirst = 1
    start_time_sec = 0
    start_time_nsec = 0
    for line in f:
        if "total allocated space" in line:
            test = line.split('::')
            time_sec = long(test[0].split(' ')[0])
            time_nsec = long(test[0].split(' ')[2])
            if isfirst:
                start_time_sec = time_sec
                start_time_nsec = time_nsec
                isfirst = 0
                x.append(0)
            else:
                diff_sec, diff_nsec = get_diff_time((start_time_sec, start_time_nsec), (time_sec, time_nsec))
                next_time = float(diff_sec) + float(diff_nsec)/1000000 
                x.append(round(next_time,3))
            mem =  int(test[1].split('=')[1])
            y.append(mem)
        if "total space" in line:
            test = line.split('::')
            time_sec = long(test[0].split(' ')[0])
            time_nsec = long(test[0].split(' ')[2])
            #print time_sec, time_nsec
            if isfirst:
                start_time_sec = time_sec
                start_time_nsec = time_nsec
                isfirst = 0
                x1.append(0)
            else:
                diff_sec = time_sec - start_time_sec
                diff_nsec = time_nsec - start_time_nsec
                if diff_nsec < 0:
                    diff_sec = diff_sec - 1
                    diff_nsec += 1000000
                next_time = float(diff_sec) + float(diff_nsec)/1000000 
            mem =  int(test[1].split('=')[1])
            if mem != -1:
                z.append(mem)
                x1.append(round(next_time,3))
        if "gc invoked" in line:
            test = line.split('::')
            time_sec = long(test[0].split(' ')[0])
            time_nsec = long(test[0].split(' ')[2])
            if isfirst:
                start_time_sec = time_sec
                start_time_nsec = time_nsec
                isfirst = 0
                x1.append(0)
            else:
                diff_sec = time_sec - start_time_sec
                diff_nsec = time_nsec - start_time_nsec
                if diff_nsec < 0:
                    diff_sec = diff_sec - 1
                    diff_nsec += 1000000
                next_time = float(diff_sec) + float(diff_nsec)/1000000 
                gc_pauses_starts.append(next_time)
        if "gc finished" in line:
            test = line.split('::')
            time_sec = long(test[0].split(' ')[0])
            time_nsec = long(test[0].split(' ')[2])
            if isfirst:
                start_time_sec = time_sec
                start_time_nsec = time_nsec
                isfirst = 0
                x1.append(0)
            else:
                diff_sec = time_sec - start_time_sec
                diff_nsec = time_nsec - start_time_nsec
                if diff_nsec < 0:
                    diff_sec = diff_sec - 1
                    diff_nsec += 1000000
                next_time = float(diff_sec) + float(diff_nsec)/1000000 
                gc_pauses_finishes.append(next_time)
        if "sweeped" in line:
            test = line.split('::')
            obj_num = test[1].split()[1]
            vol = test[1].split()[3]
            sweeped.append(int(vol))

                  

def draw_plot():
    import matplotlib.pyplot as pl
    import numpy

    fig = pl.figure(figsize=(20,10))
    pl.rc("font", size=35, weight='bold')
    ax = fig.gca()
    pl.axhline(linewidth=6, color="k")
    pl.axvline(linewidth=6, color="k")
    pl.ylabel('memory, bytes', fontsize=40, weight='bold')
    pl.xlabel('time, sec', fontsize=40, weight='bold')
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontsize(24)
        label.set_bbox(dict(facecolor='white', edgecolor='None', alpha=0.65))

#ax.set_yticks(numpy.arange(0,60000,3000))
#ax.set_xticks(numpy.arange(0,4,0.2))
    help = []
    for i in z:
        help.append(i*0.75)
    pl.grid(linewidth=3)
    p1 = pl.plot(x, y, 'r',linewidth=5.0, label="allocated space")
    p2 = pl.plot(x1, z, 'b',linewidth=5.0, label="total space")
    #p3 = pl.plot(x1, help, 'g',linewidth=5.0, label="0.75 * total space")
    #p1 = pl.plot(x, y, 'k',linewidth=5.0, label="allocated space")
    #p2 = pl.plot(x1, z, 'k--',linewidth=5.0, label="total space")
    #p3 = pl.plot(x1, help, 'k:',linewidth=5.0, label="0.75 * total space")
    legend = ax.legend(loc='lower right', shadow=False)
    pl.savefig(plot_name)

def draw_one_plot():
    pass


def stats():
    duration = []
    for i, el in enumerate(gc_pauses_starts):
        print "start = " + str(el) + "sec"
        print "finish = " + str(gc_pauses_finishes[i]) + "sec\n"
        duration.append(gc_pauses_finishes[i]-el)

    print "max gc pause = " + str(max(duration)) 
    print "avg gc pause = " + str(numpy.mean(duration))
    print "min gc pause = " + str(min(duration))

    print "max alloc size = " + str(max(y))
    print "max total size = " + str(max(z))

    for i in duration:
        print i

    for i in sweeped:
        print i
    print "max sweeped = " + str(max(sweeped))
    print "min sweeped = " + str(min(sweeped))
    print "avg sweeped = " + str(numpy.mean(sweeped))

if __name__ == "__main__":
    log = argv[1]
    plot_name = argv[2]
    sweeped = []

    f = open(log, "r")
    x = []
    x1 = []
    y = []
    z = []

    gc_pauses_starts = []
    gc_pauses_finishes = []
    parse(f)
    draw_plot()
    f.close()