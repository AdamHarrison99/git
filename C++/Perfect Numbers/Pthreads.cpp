#include <iostream>
#include <chrono>
#include <ctime>
#include <pthread.h>

int num_threads; uint64_t num_factors = 1;
uint64_t num; uint64_t nums[100] = {0}; uint64_t sum = 0;

pthread_mutex_t mutex;

void *report_results(void *args);

struct thread_args {
	uint64_t num_low; uint64_t num_high;
};

int main(){
	auto start_Time = std::chrono::system_clock::now();

  pthread_mutex_init(&mutex, NULL);
  std::cout << "Enter number: ";  std::cin >> num;
  std::cout << "Number of threads: ";  std::cin >> num_threads;

  thread_args args[num_threads];
  uint64_t first = 1; uint64_t last = num; uint64_t start, stop;
  for (int i = 0; i < num_threads; i++) {
    start = ((last - first)/num_threads)*i + first;
    stop = ((last - first)/num_threads)*(i+1) + first;
    args[i].num_low = start;
    args[i].num_high = stop;
  }

  pthread_t tid[num_threads];
  for (int i = 0; i < num_threads; i++) {
    int status = pthread_create(&tid[i], NULL, report_results, &args[i]);
    if (status != 0){
      std::cout << "Unable to create thread " << i << '\n';
    }
  }

  for (int i = 0; i < num_threads; i++) {
		pthread_join(tid[i], NULL);
	}

  std::cout << "Number of factors is: " << num_factors - 1 << '\n';
  for (int i = 1; i < num_factors; i++){
    std::cout << nums[i] << '\n';
  }

  if (sum != num){
    std::cout << '\n' << num << " is not a perfect number" << '\n';
  } else {
    std::cout << '\n' << num << " is a perfect number" << '\n';
  }

  pthread_mutex_destroy(&mutex);

	auto end_Time = std::chrono::system_clock::now();
  std::chrono::duration<double> elapsed_seconds = end_Time - start_Time;
  std::cout << "Elapsed time: " << elapsed_seconds.count() << " Seconds\n";
	return 0;
}

void *report_results(void *s) {
  thread_args *args = static_cast<thread_args*> (s);
  uint64_t num_low = args->num_low; uint64_t num_high = args->num_high;
  while (num_low < num_high){
		pthread_mutex_lock(&mutex);
    if (num % num_low == 0){
      nums[num_factors] = num_low;
      sum += num_low;
      num_factors++;
    }
		pthread_mutex_unlock(&mutex);
    num_low++;
  }
  //std::cout << "Hi, i'm thread # " << pthread_self() << ". ";
  //std::cout << "My num_factors is: " << num_factors << '\n';
  pthread_exit(0);
}
