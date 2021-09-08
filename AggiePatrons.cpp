#include <iostream>
#include <vector>
#include <stdexcept>
#include <sstream>
#include <fstream>
#include "AggiePatrons.h"

using namespace std;

// default constructor
AggiePatrons::AggiePatrons() : table(nullptr), numDays(0), numPatrons(0), 
                   dayCapacity(0), patronCapacity(0) {}
                   
// copy constructor
AggiePatrons::AggiePatrons(const AggiePatrons& src) : 
                   table(nullptr), numDays(0), numPatrons(0), 
                   dayCapacity(0), patronCapacity(0) {
  this->resizeTable(src.patronCapacity, src.dayCapacity);
  this->numDays = src.numDays;
  this->numPatrons = src.numPatrons;
  for (unsigned int patron=0; patron<numPatrons; ++patron) {
    for (unsigned int day=0; day<numDays; ++day) {
      table[patron][day] = src.table[patron][day];
    }
  }
}
                   
// destructor
AggiePatrons::~AggiePatrons() {
  deleteTable();
}

// copy assignment
AggiePatrons& AggiePatrons::operator=(const AggiePatrons& src) {
  if (this != &src) { // check for self assignment
    this->deleteTable(); // delete old memory
    this->resizeTable(src.patronCapacity, src.dayCapacity); // allocate new memory
    this->numDays = src.numDays;
    this->numPatrons = src.numPatrons;
    // copy
    for (unsigned int patron=0; patron<numPatrons; ++patron) {
      for (unsigned int day=0; day<numDays; ++day) {
        table[patron][day] = src.table[patron][day];
      }
    }    
  }
  return *this;
}


void AggiePatrons::print() {
  if (table == nullptr) {
    cout << "Empty Table" << endl;
  }
  for (unsigned int patron = 0; patron < numPatrons; ++patron) {
    for (unsigned int day = 0; day < numDays; ++day) {
      cout << table[patron][day] << '\t';
    }
    cout << endl;
  }
}

void AggiePatrons::deleteTable() {
  for (unsigned int row = 0; row < patronCapacity; ++row) {
    delete [] table[row];
  }
  delete [] table;
  table = nullptr;
  patronCapacity = 0;
  dayCapacity = 0;
  numPatrons = 0;
  numDays = 0;
}

void AggiePatrons::increasePatrons() {
  unsigned int newPatronCapacity = patronCapacity*2;
  resizeTable(newPatronCapacity, dayCapacity);
}

void AggiePatrons::increaseDays() {
  unsigned int newDayCapacity = dayCapacity*2;
  resizeTable(patronCapacity, newDayCapacity);
}

// new cells are initialized to 0
void AggiePatrons::resizeTable(unsigned int newPatronCapacity, unsigned int newDayCapacity) {
  
  unsigned int theNumPatrons = numPatrons;
  unsigned int theNumDays = numDays;
  // save a copy since deleteTable() function will reset them to 0
  
  if (newPatronCapacity == 0) newPatronCapacity = 1;
  if (newDayCapacity == 0) newDayCapacity = 1;

  
  // allocate new table
  unsigned int** newTable = new unsigned int*[newPatronCapacity];
  for (unsigned int row = 0; row < newPatronCapacity; ++row) {
    newTable[row] = new unsigned int[newDayCapacity] {0};
  }
  
  // copy values
  for (unsigned int row = 0; row < numPatrons; ++row) {
    for (unsigned int col = 0; col < numDays; ++ col) {
      newTable[row][col] = table[row][col];
    }
  }
  
  // delete old table
  deleteTable();
  // everything comes back zeroed out
  
  // update data members
  table = newTable;
  patronCapacity = newPatronCapacity;
  dayCapacity = newDayCapacity;
  numPatrons = theNumPatrons;
  numDays = theNumDays;
  
 }

void AggiePatrons::loadPatronData(std::string filename) {
  //cout << "starting loadPatronData" << endl;
  ifstream ifs(filename);
  if (!ifs.is_open()) {
    throw invalid_argument("Invalid filename: " + filename);
  }
  //cout << "Opened: " << filename << endl;
  string line;
  int patronIndex = 0;
  while (getline(ifs, line)) {
    //cout << "start processing lines" << endl;
    //cout << "line to process: " << line << endl;
    if (line.empty()) {
      //cout << "Empty line" << endl;
      continue;
    }
    addPatron();
    
    istringstream iss(line);

    int events = 0;
    int dayIndex = 0;
    
    while(iss >> events) {
      if (iss.fail()) 
        continue;   
      //cout << "patronIndex: " << patronIndex << endl;
      //cout << "dayIndex: " << dayIndex << endl;
      //cout << "events: " << events << '\n' << endl;
      addDayEvent(patronIndex, dayIndex, events);
      dayIndex++;
    }
    patronIndex++;
  }
}

// add zeros too all patrons for the start day through the last day

// adds days needed to add the new day
void AggiePatrons::addDayEvent(unsigned int patronID, unsigned int dayID,
unsigned int events) {
  if (patronID >= numPatrons)
    throw invalid_argument("invalid patron ID");
  while (dayID >= dayCapacity) {
    increaseDays();
  }
  if (dayID >= numDays) {
    numDays = dayID + 1;
  }
  table[patronID][dayID] = events;
  
}

// adds an additional patron
void AggiePatrons::addPatron() {
  if (numPatrons == patronCapacity) {
    increasePatrons();
  }
  numPatrons++;
}

double AggiePatrons::getAverageAttendanceForDay(unsigned int dayID){
  double sum=0;
  if(dayID<0||dayID>=numDays){
    throw std::invalid_argument("Day out of range");
  }
  for(unsigned int i=0;i<numPatrons;i++){
    sum+=table[i][dayID];
  }
  return sum/numPatrons;
}

unsigned int AggiePatrons::getTotalAttendanceForPatron(unsigned int patronID){
  unsigned int events=0;
  if(patronID<0||patronID>=numPatrons){
    throw std::invalid_argument("Patron does not exist");
  }
  for(unsigned int j=0;j<numDays;j++){
    events+=table[patronID][j];
  }
  return events;
}

std::vector<unsigned int> AggiePatrons::getActivePatrons(){
  vector<unsigned int> patrons;
  int temp;
  for(unsigned int i=0;i<numPatrons;i++){
    temp=0;
    for(unsigned int j=0;j<numDays;j++){
      temp+=table[i][j];
    }
    if(temp>4){
      patrons.push_back(i);
    }
  }
  return patrons;
}
 std::vector<unsigned int> AggiePatrons::getMostActiveDays(){
   vector<unsigned int> days;
   int temp;
   int tempMax=-1;
   for(unsigned int j=0;j<numDays;j++){
     temp=0;
     for(unsigned int i=0;i<numPatrons;i++){
       if(table[i][j]>0){
         temp++;
       }
     }
     if(temp>=tempMax){
       if(temp>tempMax){
         days.clear();
       }
       days.push_back(j);
       tempMax=temp;
     }
   }
   return days;
 }

