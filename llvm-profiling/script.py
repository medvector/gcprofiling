from sys import argv
import matplotlib.pyplot as pl
import numpy

start_time = (0, 0)
isfirst = 1

def get_diff_time(time1, time2):
    diff_sec = time2[0] - time1[0]
    diff_nsec = time2[1] - time1[1]
    if diff_nsec < 0:
        diff_sec = diff_sec - 1
        diff_nsec += 1000000
    return (diff_sec, diff_nsec)

def getmem(info):
    return int(info.split('=')[1])


def get_sweeped_objects(info):
    obj_num = info.split()[1]
    vol = info.split()[3]
    return (int(obj_num), int(vol))

def round_time(time):
    return round(time, 3)

def parse(file_name, key_line, t, data, transform_time, need_data, getdata):
    global isfirst
    global start_time
    file = open(file_name, "r")
    for line in file:
        if key_line in line:
            time_stamp, info = line.split('::')
            time = (long(time_stamp.split(' ')[0]), long(time_stamp.split(' ')[2]))
            if isfirst:
                start_time = time
                isfirst = 0
                t.append(0)
            else:
                diff_sec, diff_nsec = get_diff_time(start_time, time)
                next_time = float(diff_sec) + float(diff_nsec)/1000000 
                t.append(transform_time(next_time))
            if need_data:
                mem =  getdata(info)
                data.append(mem)
    file.close()

def draw_plot(x, y, color_scheme, labels, location, plotname):
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
    pl.grid(linewidth=3)
    for i, x_ax in enumerate(x):
        p1 = pl.plot(x_ax, y[i], color_scheme[i], linewidth=5.0, label=labels[i])
    legend = ax.legend(loc=location, shadow=False)
    pl.savefig(plotname)

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


def test_drawing():
    sweeped = []

    x = []
    x1 = []
    y = []
    z = []

    gc_pauses_starts = []
    gc_pauses_finishes = []
    parse(log, "total allocated space", x, y, round_time, True, getmem)
    parse(log, "total space", x1, z, round_time, True, getmem)
    parse(log, "gc invoked", gc_pauses_starts, [], (lambda x: x), False, getmem)
    parse(log, "gc invoked", gc_pauses_finishes, [], (lambda x: x), False, getmem)
    parse(log, "sweeped", [], sweeped, (lambda x: x), True, get_sweeped_objects)


    if z[0] == -1:
        del(z[0])
        del(x1[0])
    draw_plot([x, x1], [y, z], ['r', 'b'], ['allocated space', 'total space'], \
        'lower right', 'test3.png')    

if __name__ == "__main__":
    log = argv[1]
    plot_name = argv[2]
    test_drawing()
   