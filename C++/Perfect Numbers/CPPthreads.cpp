#include <iostream>
#include <chrono>
#include <ctime>
#include <thread>
#include <mutex>
#include <vector>

int num_threads;
uint64_t num_factors = 1; uint64_t nums[100] = {0}; uint64_t sum = 0; uint64_t num_low, num_high, num;

std::mutex mtx;

void report_results(uint64_t num_low, uint64_t num_high);

int main(){
  auto start_Time = std::chrono::system_clock::now();

  std::cout << "Enter number: ";  std::cin >> num;
  std::cout << "Number of threads: ";  std::cin >> num_threads;

  std::vector<std::thread> threads;
  uint64_t first = 1; uint64_t last = num; uint64_t start, stop;
  for (int i = 0; i < num_threads; i++) {
    start = ((last - first)/num_threads)*i + first;
    stop = ((last - first)/num_threads)*(i+1) + first;
    num_low = start;
    num_high = stop;
    threads.push_back(std::thread {report_results, num_low, num_high});
  }

  for (std::thread &t: threads) { t.join(); }

  std::cout << "Number of factors is: " << num_factors - 1 << '\n';
  for (int i = 1; i < num_factors; i++){
    std::cout << nums[i] << '\n';
  }

  if (sum != num){
    std::cout << '\n' << num << " is not a perfect number" << '\n';
  } else {
    std::cout << '\n' << num << " is a perfect number" << '\n';
  }

  auto end_Time = std::chrono::system_clock::now();
  std::chrono::duration<double> elapsed_seconds = end_Time - start_Time;
  std::cout << "Elapsed time: " << elapsed_seconds.count() << " Seconds\n";
	return 0;
}

void report_results(uint64_t num_low, uint64_t num_high) {
  while (num_low < num_high){
    mtx.lock();
    if (num % num_low == 0){
      nums[num_factors] = num_low;
      sum += num_low;
      num_factors++;
    }
    mtx.unlock();
    num_low++;
  }
}
