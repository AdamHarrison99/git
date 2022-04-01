#ifndef process_H
#define process_H

class process {
private:
std::string name;
int arrival_t;
int run_t;
int burst;
bool has_seen;
int initial_wait = 0;
int total_wait = 0;
public:

  process(const std::string process_name, int arival_time, int run_time, int cpu_burst);

  ~process();

  int get_arrival();

  std::string get_name();

  int get_burst();

  int get_run();

  void seen(int time);

  bool get_seen();

  bool arrival_sorter(process a, process b);

  int get_wait();

  void dec_burst();

  void set_wait(int wait);

};
#endif
