#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <cmath>
#include "functions.h"

using std::cout;
using std::cin;
using std::string;
using std::ostringstream;

int main() { 
  cout << "Input filename: ";
  string filename;
  cin >> filename;
  string temp1;
  string temp2;
  
  // TODO(student): add error checking for width, height, targetWidth, and targetHeight
  cout << "Input width and height: ";
  int width = 0;
  int height = 0;
  cin >> temp1 >> temp2;
  try{
    width=std::stoi(temp1,nullptr);
  } catch(std::invalid_argument){
    cout<<"Error: width is a non-integer value";
    return 1;
  }
  try{
    height=std::stoi(temp2,nullptr);
  } catch(std::invalid_argument){
    cout<<"Error: height is a non-integer value";
    return 1;
  }
  cout << "Input target width and height: ";
  int targetWidth = 0;
  int targetHeight = 0;
  cin >> temp1 >> temp2;
  try{
    targetWidth=std::stoi(temp1,nullptr);
  } catch(std::invalid_argument){
    cout<<"Error: target width is a non-integer value";
    return 1;
  }
  try{
    targetHeight=std::stoi(temp2,nullptr);
  } catch(std::invalid_argument){
    cout<<"Error: target height is a non-integer value";
    return 1;
  }
  if(width<=0){
	    cout<<"Error: width must be greater than 0. You entered "<<width;
	    return 1;
  }
  if(height<=0){
	    cout<<"Error: height must be greater than 0. You entered "<<height;
	    return 1;
  }
  if(targetWidth<=0){
	    cout<<"Error: target width must be greater than 0. You entered "<<targetWidth;
	    return 1;
  }
  if(targetHeight<=0){
	    cout<<"Error: target height must be greater than 0. You entered "<<targetHeight;
	    return 1;
  }
  if(width<targetWidth){
    cout<<"Error: target width must be less than width, "<<targetWidth<<" is greater than "<<width;
    return 1;
  }
  if(height<targetHeight){
    cout<<"Error: target height must be less than height, "<<targetHeight<<" is greater than "<<height;
    return 1;
  }
  
  
  // save originalWidth since width will change with carving
  int originalWidth = width; 
  
  Pixel** image1 = createImage(width, height);
  if (image1 != nullptr) { // new returns nullptr if it fails to allocate array
    
    if (loadImage(filename, image1, width, height)) {


      // uncomment for part 2
      
      while ((width - targetWidth > 0) ) {
        if (width - targetWidth > 0) {
          int* verticalSeam = findMinVerticalSeam(image1, width, height);
          removeVerticalSeam(image1, width, height, verticalSeam);
          deleteSeam(verticalSeam);
          width--;
        }

        // this is for the extra credit
        if (height - targetHeight > 0) {
          int* horizontalSeam = findMinHorizontalSeam(image1, width, height);
          removeHorizontalSeam(image1, width, height, horizontalSeam);
          deleteSeam(horizontalSeam);
          height--;
        }
      }
      

      
      
      filename="carved"+std::to_string(width)+'X'+std::to_string(height)+'.'+filename;
      outputImage(filename, image1, width, height);
    }
  }
  
  // call last to remove the memory from the heap
  deleteImage(image1, originalWidth);
}
