#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <cmath>
#include <algorithm>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "process.h"
#include "RR_Scheduler.h"

double total_initial = 0.0; double total_wait = 0.0; double total_turn = 0.0;


process::process(std::string process_name, int arrival_time, int run_time, int cpu_burst){
  name = process_name; arrival_t = arrival_time; run_t = run_time; burst = cpu_burst;
}
process::~process(){}

int process::get_arrival()
{
	return arrival_t;
}

std::string process::get_name()
{
	return name;
}

int process::get_burst()
{
	return burst;
}

void process::dec_burst()
{
  burst--;
}

bool process::get_seen()
{
  return has_seen;
}

void process::seen(int time)
{
  has_seen = true;
	initial_wait = time;
	total_wait = time;
}

int process::get_wait()
{
  return total_wait;
}

void process::set_wait(int wait)
{
  total_wait += wait;
}


RR_Scheduler::RR_Scheduler(std::vector<process> processes, int block, int quantum){
  int current_slice = 0; int clock = 0; int num_completed = 0;
  timeslice = block; q = quantum;
  std::vector <process> queue;
  int index = processes.size();
  bool cswitch = false;
  while(num_completed != processes.size()){
    for(int i = 0; i < index; i++){
      if (processes[i].get_arrival() <= clock){
        queue.push_back(processes[i]);
        index--;
				i--;
      }
    }
    if (queue.size() != 0){
      if (cswitch){
        std::cout << clock << "\t" << queue[0].get_name() << "\t" << queue[0].get_wait() << "\t" << "B" << "\n";
				cswitch = false;
      }
      if (queue[0].get_seen() == false){
        long initial = (clock - queue[0].get_arrival());
        queue[0].seen(initial);
        total_wait += initial;

        std::cout << clock << "\t" << queue[0].get_name() << "\t" << queue[0].get_wait() << "\t" << "Q" << "\n";
      }
      queue[0].dec_burst();
      current_slice++;

      if (queue[0].get_burst() == 0){
        long total_wait_p = ((clock + 1) - queue[0].get_arrival() - queue[0].get_burst());
        std::cout << clock + 1 << "\t" << queue[0].get_name() << "\t" << queue[0].get_wait() << "\t" << "Q" << "\n";
        long turnaround = ((clock + 1) - queue[0].get_arrival());
        total_turn += turnaround;
        total_wait += total_wait_p;
        queue[0].set_wait(total_wait_p);

        queue.erase(queue.begin());
				num_completed++;

        if (queue.size() == 0){
          std::cout << clock << "\t" << queue[0].get_name() << "\t" << queue[0].get_wait() << "\t" << "T" << "\n";
          clock = clock + q;
        }
        else{
          cswitch = true;
        }
        current_slice = 0;
      }
      else if (current_slice == timeslice){
				queue.push_back(queue[0]);
				queue.erase(queue.begin());
				current_slice = 0;
        std::cout << clock << "\t" << "[IDLE]" << "\t" << queue[0].get_wait() << "\t" << "I" << "\n";
        clock = clock + q;
			}
    }
    clock++;
  }
  std::cout << total_wait << "\t" << "[END]\n";
  for(int i = 0; i < processes.size(); i++){
    std::cout << processes[i].get_name() << "\t" << processes[i].get_wait() << "\n";
  }
  processes.erase(processes.begin(), processes.end());
  queue.erase(queue.begin(), queue.end());
}

RR_Scheduler::~RR_Scheduler(){}

bool arrival_sorter(process a, process b)
{
	return a.get_arrival() < b.get_arrival();
}

int main(int argc, char *argv[]){
  if(argc < 3){
    std::cout << "Usage: project5.out <input file> <block duration> <quantum>\n";
    return(1);
  }
  std::string textFileName = argv[1]; int block_duration = atoi(argv[2]); int quantum = atoi(argv[3]);
  std::string textFile = "";
  std::ifstream myReadFile(textFileName);
  if (!myReadFile.is_open()) {
    std::cout << "Could not open " << textFileName << "\n";
    return(1);
  }

  std::string txt_line;
  while (std::getline(myReadFile, txt_line)){
    textFile.append(txt_line); textFile.append("\n");
  }
  myReadFile.close();

  std::vector<process> processes;
  std::string values[3]{}; std::string line; std::string process_name;
  std::istringstream iss (textFile);
  while (std::getline(iss, line)){
    std::istringstream ssline(line);
    getline(ssline, process_name, ' ');
    getline(ssline, values[0], ' ');
    getline(ssline, values[1], ' ');
    getline(ssline, values[2], '\n');

    int arrival_time = stoi(values[0]); int run_time = stoi(values[1]); int cpu_burst = stoi(values[2]);

    process temp(process_name, arrival_time, run_time, cpu_burst);
    processes.push_back(temp); //Not sure if this is the reason only one process is running or not
  }

  sort(processes.begin(), processes.end(), arrival_sorter);

  std::cout << block_duration << " " << quantum << "\n";

  RR_Scheduler(processes, block_duration, quantum); //Fails to use more than one process in the scheduler

  std::cout << total_wait / processes.size() << "\n";

  return(0);
}
