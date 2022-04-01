#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>


class DD{
private:
  std::string file_name;

public:

  DD(const std::string input_file){
    file_name = input_file;
    std::cout << "Hello World\n" << file_name << "\n";
  }

  ~DD(){};

  void run(){

  };

};

int main(int argc, char *argv[]){
  if(argc < 2){
    std::cout << "Usage: deadlock_detection.out <input file>\n";
    return(1);
  }
  std::string textFileName = argv[1];
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
  std::istringstream iss (textFile); std::string line;
    std::getline(iss, line);
    std::istringstream ssline(line);
    std::string values[2]{};
    getline(ssline, values[0], ' ');
    getline(ssline, values[1], ' ');
    int columns = stoi(values[0]); int types = stoi(values[1]);
    std::cout << "Number of processes: " << columns << "\nNumber of resource types: " << types << "\n";
    std::vector<std::vector<std::string>> v2;
    for(int i = 0; i < 4; i++){
      std::vector<std::string> v1;
      for (int j = 0; j < columns; i++){
        v1.push_back(getline(ssline, ' '));
        std::cout << v1[j] << ' ';
      }
      v2.push_back(v1);
      std::cout << '\n';
    }
  myReadFile.close();
  return (0);
}
