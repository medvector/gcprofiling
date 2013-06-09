import java.util.*;
public class Monitor extends Thread{
        public void run() {
         Runtime rt = Runtime.getRuntime();
         System.out.println(
            "Time   Total   Free   Free");
         System.out.println(
            "sec.    Mem.   Mem.   Per.");
         long dt0 = System.currentTimeMillis()/1000;
         while (true) {
            long tm = rt.totalMemory()/1024;
            long fm = rt.freeMemory()/1024;
            long ratio = (100*fm)/tm;
            long dt = System.currentTimeMillis()/1000 - dt0;
            System.out.println(dt 
               + "   " + tm + "   " + fm + "   " + ratio +"%");
            mySleep(wait);
         }
       }
}
