#include <iostream>
#include <string>
#include <pthread.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

int num_reads = 3; int num_writes = 3;
int num_readers = 5; int num_writers = 2;
int num_threads = num_readers + num_writers;
int line = 1; int shared;
int w_waiting = 0; int w_working = 0; int r_waiting = 0; int r_working = 0;

pthread_mutex_t mutex;
pthread_cond_t canread, canwrite;

struct thread_args {
	int thread_no;
};

void startread(int thread_no){
	int random_int;

	sleep(rand() % 1 + 1);
  for (int i = 0; i < num_reads; i++){

		pthread_mutex_lock(&mutex);
		if (w_waiting > 0 || w_working == 1){
	    std::cout << "reader " << thread_no << " is sleeping\n";
			r_waiting++;
	    pthread_cond_wait(&canread, &mutex);
			r_waiting--;
	    std::cout << "reader " << thread_no << " is awake\n";
		}

    r_working ++;
		sleep(rand() % 1 + 1);
    random_int = shared;
    r_working --;

    std::cout << line++ << ":" << "reader " << thread_no + 1 << " read " << random_int << " : " << r_working << " reader(s), "
    << r_waiting << " reader(s) waiting, " << w_waiting << " writer(s) waiting\n";
		pthread_mutex_unlock(&mutex);
  }
  pthread_exit(0);
}

void endread(){
	sleep(rand() % 1 + 1);
	pthread_mutex_lock(&mutex);
	if (w_waiting > 0){
		pthread_cond_broadcast(&canwrite);
	}
	else if (r_waiting > 0){
		pthread_cond_broadcast(&canread);
	}
	pthread_mutex_unlock(&mutex);
}

void startwrite(int thread_no){
	//sleep(rand() % 1 + 1);
  int random_int = rand() % 1000 + 1;
	pthread_mutex_lock(&mutex);
		if (r_working > 0 || w_working > 0){
	    std::cout << "writer " << thread_no << " is sleeping\n";
			w_waiting++;
	    pthread_cond_wait(&canwrite, &mutex);
			w_waiting--;
	    std::cout << "writer " << thread_no << " is awake\n";
		}

		w_working++;
		sleep(rand() % 1 + 1);
    shared = random_int;

    std::cout << line++ << ":" << "writer " << thread_no + 1 << " wrote " << random_int << " : " << r_working << " reader(s), "
    << r_waiting << " reader(s) waiting, " << w_waiting << " writer(s) waiting\n";
		pthread_mutex_unlock(&mutex);
}

void endwrite(){
	sleep(rand() % 1 + 1);
	pthread_mutex_lock(&mutex);
	w_working--;

	if (w_waiting > 0){
		pthread_cond_broadcast(&canwrite);
	}
	else if (r_waiting > 0){
		pthread_cond_broadcast(&canread);
	}
	pthread_mutex_unlock(&mutex);
}

void* reader(void* a){
	thread_args *read_args = static_cast<thread_args*> (a);
  int thread_no = read_args->thread_no;
	for (int i = 0; i < num_writes; i++){
		sleep(rand() % 1 + 1);
		startread(thread_no);
		endread();
	}
	pthread_exit(0);
}

void* writer(void* a){
	thread_args *write_args = static_cast<thread_args*> (a);
  int thread_no = write_args->thread_no;
	for (int i = 0; i < num_writes; i++){
		sleep(rand() % 1 + 1);
		startwrite(thread_no);
		endwrite();
	}
	pthread_exit(0);
}

int main(){
  pthread_mutex_init(&mutex, NULL);
  srand(time(NULL));

  pthread_t tid_read[num_threads];
  thread_args read_args[num_threads];
  for (int i=0; i<num_readers; ++i) {
    read_args[i].thread_no = i;
    int status = pthread_create(&tid_read[i], NULL, reader, &read_args[i]);
    if (status != 0) std::cout << "Unable to create thread " << i << '\n';
  }

  pthread_t tid_write[num_threads];
  thread_args write_args[num_threads];
  for (int i=0; i<num_writers; ++i) {
    write_args[i].thread_no = i;
    int status = pthread_create(&tid_write[i], NULL, writer, &write_args[i]);
    if (status != 0) std::cout << "Unable to create thread " << i << '\n';
  }

  for (int i=0; i<num_readers; ++i) {
    pthread_join(tid_read[i], NULL);
  }
  for (int i=0; i<num_writers; i++){
    pthread_join(tid_write[i], NULL);
  }

  pthread_mutex_destroy(&mutex);
	pthread_cond_destroy(&canread);
	pthread_cond_destroy(&canwrite);
//  std::cout << "Press Enter to continue. . .";
//  if (std::cin.get() == '\n'){return 0;}
  return 0;
}
