#include "GC_stat.h"

struct timeval GC_stat::myStart;
struct timeval GC_stat::getTimeFromMoment(struct timeval t, struct timeval l) {
		struct timeval tmp;
		tmp.tv_sec = t.tv_sec - l.tv_sec;
		tmp.tv_usec = t.tv_usec - l.tv_usec;
		if (tmp.tv_usec < 0) {
			tmp.tv_sec--;
			tmp.tv_usec += 1000000;
		}
		return tmp;
}
struct timeval GC_stat::add(struct timeval arg1, struct timeval arg2) {
	struct timeval tmp;
	tmp.tv_sec = arg1.tv_sec + arg2.tv_sec;
	tmp.tv_usec = arg1.tv_usec + arg2.tv_usec;
	if (tmp.tv_usec >= 1000000) {
		tmp.tv_sec++;
		tmp.tv_usec -= 1000000;
	}
	return tmp;	
}

GC_stat::GC_stat(std::vector <GC_Collection>* collections) {
	gc_times = 0;
	myCollections =  collections;
}

int GC_stat::getTimes() {
	return gc_times;
}

void GC_stat::incTimes() {
	gc_times++;
}

void GC_stat::printTimeStat() {
	freopen("gc.log", "w", stdout);
    for (std::vector<GC_Collection>::iterator it = myCollections->begin();
        it != myCollections->end(); ++it) {
        std:: cout << "garbage colection #" << it->getNum() << std::endl;
        std::cout << "\t start time: " << it -> getStartTimeSec() << " s " <<
        it -> getStartTimeMs() << " ms" << std::endl;
        std::cout << "\t finish time: " << it -> getFinishTimeSec() << " s " <<
        it -> getFinishTimeMs() << " ms" << std::endl;
        std::cout << "\t duration: " << it -> getDurationSec() << " s " <<
        it -> getDurationMs() << " ms" << std::endl;
        std::cout << std::endl;
    } 
}

void GC_stat::setProgramStart(struct timeval t) {
	program_start = GC_stat::getTimeFromMoment(t, GC_stat::myStart);
}
void GC_stat::setProgramEnd(struct timeval t) {
	program_end =  GC_stat::getTimeFromMoment(t, GC_stat::myStart);
}
time_t GC_stat::getProgramStartSec() {
	return program_start.tv_sec;
}
suseconds_t GC_stat::getProgramStartMs() {
	return program_start.tv_usec;
}
suseconds_t GC_stat::getProgramEndMs() {
	return program_end.tv_usec;
}
time_t GC_stat::getProgramEndSec() {
	return program_end.tv_sec;
}
void GC_stat::printMoreTimeStat() {
	std::cout << "Elapsed time: " << GC_stat::getTimeFromMoment(program_end, program_start).tv_sec 
	<< " s " << GC_stat::getTimeFromMoment(program_end, program_start).tv_usec << " ms"<<std::endl;
	struct timeval tmp;
	tmp.tv_sec = 0;
	tmp.tv_usec = 0;
	for (std::vector<GC_Collection>::iterator it = myCollections->begin();
		it != myCollections->end(); ++it) {
		tmp = GC_stat::add(tmp, it -> getDuration());
	}
	std::cout << "GC time: " << tmp.tv_sec << " s " << tmp.tv_usec << " ms"<< std::endl;
}