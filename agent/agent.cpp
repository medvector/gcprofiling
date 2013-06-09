#include "jvmti.h"
#include <sys/time.h>
#include <string.h>
#include "GC_Collection.h"
#include "GC_stat.h"
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <iostream>
#include <string>
#include <stdarg.h>
#include <map>



bool flag = 0;
struct timeval current_time;
struct timeval start;

std::vector <GC_Collection> collections;
GC_stat myStat(&collections);


void handleError(
    jvmtiEnv *jvmti, jvmtiError errorNumber, const char *message) {

    if (errorNumber == JVMTI_ERROR_NONE) return; // If this is not an error then don't handle it.

    char *errorString = NULL;
    jvmti->GetErrorName(errorNumber, &errorString);
    if (NULL == errorString) errorString = "Unknown";

    if (NULL == message) message = "";

    fprintf(stderr, "ERROR: JVMTI: %d(%s): %s\n", errorNumber, errorString, message);

    exit(3);
}
void JNICALL GarbageCollectionStartCallBack(jvmtiEnv *jvmti) {
    myStat.incTimes();
    gettimeofday(&current_time, NULL);
    collections.push_back(GC_Collection(current_time, myStat.getTimes()));
}

void JNICALL GarbageCollectionFinishCallBack(jvmtiEnv *jvmti) {
    gettimeofday(&current_time, NULL);
    collections.back().setFinishTime(current_time);
}


JNIEXPORT jint JNICALL 
Agent_OnLoad(JavaVM *jvm, char *options, void *reserved) {
    printf("Agent Started\n");
    jvmtiEnv *jvmti;
    jvm->GetEnv((void**)&jvmti, JVMTI_VERSION_1_2);
    jvmtiError error;
    jvmtiCapabilities capabilities;
    (void)memset(&capabilities, 0, sizeof(capabilities));
    capabilities.can_generate_garbage_collection_events = 1;
    capabilities.can_tag_objects = 1;
    capabilities.can_generate_vm_object_alloc_events = 1;
    jvmti->AddCapabilities(&capabilities);
    jvmtiEventCallbacks callbacks;
    (void)memset(&callbacks, 0, sizeof(callbacks));
    callbacks.GarbageCollectionStart = &GarbageCollectionStartCallBack;
    callbacks.GarbageCollectionFinish = &GarbageCollectionFinishCallBack;
    error = jvmti->SetEventCallbacks(&callbacks, (jint)sizeof(callbacks));
    handleError(jvmti, error, "Cannot set jvmti callbacks");
    error = jvmti->SetEventNotificationMode(JVMTI_ENABLE, JVMTI_EVENT_GARBAGE_COLLECTION_START, (jthread)NULL);
    handleError(jvmti, error, "Cannot set event notification");
    error = jvmti->SetEventNotificationMode(JVMTI_ENABLE, JVMTI_EVENT_GARBAGE_COLLECTION_FINISH, (jthread)NULL);
    handleError(jvmti, error, "Cannot set event notification");
    error = jvmti->SetEventNotificationMode(JVMTI_ENABLE, JVMTI_EVENT_VM_OBJECT_ALLOC, (jthread)NULL);
    handleError(jvmti, error, "Cannot set event notification");
    gettimeofday(&start, NULL);
    GC_stat::myStart = start;
    myStat.setProgramStart(start);
    return JNI_OK;
}
JNIEXPORT jint JNICALL 
Agent_OnAttach(JavaVM* vm, char *options, void *reserved) {

    return JNI_OK;
}

JNIEXPORT void JNICALL 
Agent_OnUnload(JavaVM *vm) { 
    gettimeofday(&current_time, NULL);
    myStat.setProgramEnd(current_time);
    myStat.printTimeStat();
    myStat.printMoreTimeStat();
}