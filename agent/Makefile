main: agent.o GC_Collection.o GC_stat.o
	g++ -shared -g -fPIC -o libagent.so agent.o GC_Collection.o GC_stat.o -I/usr/lib/jvm/java-7-openjdk-amd64/include
agent.o: agent.cpp GC_Collection.h GC_stat.h
	g++ -c -g agent.cpp -fPIC -I/usr/lib/jvm/java-7-openjdk-amd64/include
GC_Collection.o: GC_Collection.cpp GC_Collection.h
	g++ -c -g GC_Collection.cpp -fPIC -I/usr/lib/jvm/java-7-openjdk-amd64/include
GC_stat.o: GC_stat.cpp GC_stat.h GC_Collection.h
	g++ -c -g GC_stat.cpp -fPIC -I/usr/lib/jvm/java-7-openjdk-amd64/include
clean: 
	rm -f *.o libagent.so