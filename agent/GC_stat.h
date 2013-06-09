#ifndef GC_STAT_H
#define GC_STAT_H
#include <vector>
#include "GC_Collection.h"
#include <iostream>
#include <stdio.h>
#include <sys/time.h>
class GC_stat {
private:
	struct timeval program_start;
	struct timeval program_end;
	int gc_times;
	std::vector <GC_Collection>* myCollections;
public:
	static struct timeval myStart;
	static struct timeval getTimeFromMoment(struct timeval t, struct timeval l);
	static struct timeval add(struct timeval arg1, struct timeval arg2);
	GC_stat(std::vector <GC_Collection>* collections);
	int getTimes();
	void incTimes();
	void printTimeStat();
	void setProgramStart(struct timeval t);
	void setProgramEnd(struct timeval t);
	time_t getProgramStartSec();
	suseconds_t getProgramStartMs();
	time_t getProgramEndSec();
	suseconds_t getProgramEndMs();
	void printMoreTimeStat();
};
#endif