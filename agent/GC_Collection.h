#ifndef GCCOLLECTION_H
#define GCCOLLECTION_H
#include <sys/time.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <iostream>
class GC_Collection {
private:
	int num;
	struct timeval start_time;
	struct timeval finish_time;
	struct timeval duration;
public:
	GC_Collection(struct timeval st_time, int i);
	void setFinishTime(struct timeval fin_time);
	time_t getStartTimeSec();
	suseconds_t getStartTimeMs();
	time_t getFinishTimeSec();
	suseconds_t getFinishTimeMs();
	time_t getDurationSec();
	suseconds_t getDurationMs();
	struct timeval getDuration();
	int getNum();
};
#endif