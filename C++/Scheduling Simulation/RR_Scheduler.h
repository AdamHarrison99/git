#ifndef RR_Scheduler_H
#define RR_Scheduler_H
#include <time.h>

class RR_Scheduler{
private:
  int timeslice;
  int q;
  int num_completed = 0;
public:

  RR_Scheduler(const std::vector<process> processes, int block, int quantum);

  ~RR_Scheduler();

};
#endif
