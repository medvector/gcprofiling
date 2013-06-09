#include "GC_Collection.h"
#include "GC_stat.h"

GC_Collection::GC_Collection(struct timeval st_time, int i) {
	start_time = GC_stat::getTimeFromMoment(st_time, GC_stat::myStart);
	num = i;
}

void GC_Collection::setFinishTime(struct timeval fin_time) {
		finish_time = GC_stat::getTimeFromMoment(fin_time, GC_stat::myStart);
		duration = GC_stat::getTimeFromMoment(finish_time, start_time);
}

time_t GC_Collection::getStartTimeSec() {
	return start_time.tv_sec;
}

suseconds_t GC_Collection::getStartTimeMs() {
	return start_time.tv_usec;
}

time_t GC_Collection::getFinishTimeSec() {
	return finish_time.tv_sec;
}

suseconds_t GC_Collection::getFinishTimeMs() {
	return finish_time.tv_usec;
} 
time_t GC_Collection::getDurationSec() {
	return duration.tv_sec;
}

suseconds_t GC_Collection::getDurationMs() {
	return duration.tv_usec;
}

int GC_Collection::getNum() {
	return num;
}

struct timeval GC_Collection::getDuration() {
	return duration;
}