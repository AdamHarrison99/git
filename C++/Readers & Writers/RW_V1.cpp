#include <iostream>
#include <pthread.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

int num_reads = 3; int num_writes = 3;
int num_readers = 3; int num_writers = 2;
int num_threads = num_readers + num_writers;
int reading = 0; int line = 1; int shared;

pthread_mutex_t mutex;

void *readers(void *args); void *writers(void *args);

struct thread_args {
	int thread_no;
};

int main(){
  pthread_mutex_init(&mutex, NULL);
  srand(time(NULL));

  thread_args args[num_threads];
  pthread_t tid[num_threads];
  for (uint32_t i=0; i<num_readers; ++i) {
    args[i].thread_no = i;
    int status = pthread_create(&tid[i], NULL, readers, &args[i]);
    if (status != 0) std::cout << "Unable to create thread " << i << '\n';
  }

  for (uint32_t i=0; i<num_writers; ++i) {
    args[i].thread_no = i;
    int status = pthread_create(&tid[i], NULL, writers, &args[i]);
    if (status != 0) std::cout << "Unable to create thread " << i << '\n';
  }

  for (uint32_t i=0; i<num_threads; ++i) {
    pthread_join(tid[i], NULL);
  }

  pthread_mutex_destroy(&mutex);
  return 0;
}

void *readers(void *a){
	thread_args *args = static_cast<thread_args*> (a);
  int thread_no = args->thread_no; int crit_readers = 0; int random_int;
  for (int i = 0; i < num_reads; i++){
    sleep(rand() % 10 + 1);

    pthread_mutex_lock(&mutex);
    crit_readers = reading;
    reading ++;
    random_int = shared;
    reading --;
    std::cout << line++ << ":" << "reader " << thread_no + 1 << " read " << random_int << " " << crit_readers << " reader(s)" << '\n';
    pthread_mutex_unlock(&mutex);
  }
  pthread_exit(0);
}

void *writers(void *a){
  thread_args *args = static_cast<thread_args*> (a);
  int thread_no = args->thread_no; int random_int; int crit_readers = 0;
  for (int i = 0; i < num_writes; i++){
    sleep(rand() % 10 + 1);

    random_int = rand() % 1000 + 1;
    pthread_mutex_lock(&mutex);
    crit_readers = reading;
    shared = random_int;
    std::cout << line++ << ":" << "writer " << thread_no + 1 << " wrote " << random_int << " " << crit_readers << " reader(s)" << '\n';
    pthread_mutex_unlock(&mutex);
  }
  pthread_exit(0);
}
