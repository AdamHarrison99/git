#include <iostream>

int main(){
  std::cout << "Enter number: ";
  uint64_t num; uint64_t sum; uint64_t num_factors = 0;
  uint64_t nums[100];
  bool perfect = false;
  std::cin >> num;

  int i = 1;
  while (i < num){
    nums[i] = num % i;
    if (num % i == 0){
      sum += i;
    }

    i++;
  }
  num_factors = i;

  std::cout << "Number of factors: " << num_factors << '\n';
  for (int j = 1; i < num_factors; j++){
    std::cout << nums[j] << ", ";
  }
  if (sum != num){
    std::cout << '\n' << num << " is not a perfect number" << '\n';
  } else {
    std::cout << '\n' << num << " is a perfect number" << '\n';
  }

}
