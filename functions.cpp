#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <cmath>
#include "functions.h"

#define INFO(X) cout << "[INFO] ("<<__FUNCTION__<<":"<<__LINE__<<") " << #X << " = " << X << endl;

using std::cout;
using std::endl;
using std::string;

Pixel** createImage(int width, int height) {
  cout << "Start createImage... " << endl;
  
  // Create a one dimensional array on the heap of pointers to Pixels 
  //    that has width elements (i.e. the number of columns)
  Pixel** image = new Pixel*[width];
  
  bool fail = false;
  
  for (int i=0; i < width; ++i) { // loop through each column
    // assign that column to a one dimensional array on the heap of Pixels
    //  that has height elements (i.e. the number of rows)
    image[i] = new Pixel[height];
    
    if (image[i] == nullptr) { // failed to allocate
      fail = true;
    }
  }
  
  if (fail) { // if any allocation fails, clean up and avoid memory leak
    // deallocate any arrays created in for loop
    for (int i=0; i < width; ++i) {
      delete [] image[i]; // deleting nullptr is not a problem
    }
    delete [] image; // dlete array of pointers
    return nullptr;
  }
  
  // initialize cells
  //cout << "Initializing cells..." << endl;
  for (int row=0; row<height; ++row) {
    for (int col=0; col<width; ++col) {
      //cout << "(" << col << ", " << row << ")" << endl;
      image[col][row] = { 0, 0, 0 };
    }
  }
  cout << "End createImage... " << endl;
  return image;
}

void deleteImage(Pixel** image, int width) {
  cout << "Start deleteImage..." << endl;
  // avoid memory leak by deleting the array
  for (int i=0; i<width; ++i) {
    delete [] image[i]; // delete each individual array placed on the heap
  }
  delete [] image;
  image = nullptr;
}

int* createSeam(int length) {
    // TODO(student): create a seam
    int* seamPointer= new int[length];
    for(int i=0;i<length;i++){
      *(seamPointer+i)=0;
    }
    INFO(length);
  return seamPointer;
}

void deleteSeam(int* seam) {
    // TODO(student): delete a seam
    delete[] seam;
    INFO(seam);
}

bool loadImage(string filename, Pixel** image, int width, int height) {
    // TODO(student): load an image
    string temp;
    int colNum;
    int rowNum;
    int maxColor;
    int tempo;
    
    
    std::ifstream inFS;
    inFS.open(filename);
    if(!inFS.is_open()){
	    cout<<"Error: failed to open input file - "<<filename; 
	    return false;
    }
    inFS >> temp;
    if(temp!="P3" && temp!="p3"){
	    cout<<"Error: type is "<<temp<<" instead of P3";
    	    return false;
    }
    inFS >>temp;
        try{
          colNum=std::stoi(temp,nullptr);
        }catch(std::invalid_argument){
          cout<<"Error: read non-integer value";
          return false;
        }
    if(colNum!=width){
    	cout<<"Error: input width ("<<width<<") does not match value in file ("<<colNum<<")";
	    return false;
    }
    inFS >>temp;
        try{
          rowNum=std::stoi(temp,nullptr);
        }catch(std::invalid_argument){
          cout<<"Error: read non-integer value";
          return false;
        }
    if(rowNum!=height){
	    cout<<"Error: input height ("<<height<<") does not match value in file ("<<rowNum<<")";
    	return false;
    }
    inFS >> maxColor;
    

    for(int row=0;row<height;row++){
	    for(int col=0;col<width;col++){
        /*if(inFS.eof()){
			    cout<<"Error: not enough color values";
			    return false;
		    }*/
	    	inFS >>temp;
        /*try{
          tempo=std::stoi(temp,nullptr);
        }catch(std::invalid_argument){
          cout<<"Error: read non-integer value";
          return false;
        }
		    if(tempo<0 || tempo>maxColor){
			    cout<<"Error: invalid color value "<<tempo;
			  return false;
	    	}*/
        tempo=std::stoi(temp,nullptr);
		    image[col][row].r=tempo;
        /*if(inFS.eof()){
			    cout<<"Error: not enough color values";
			    return false;
		    }*/
	    	inFS >>temp;
        /*try{
          tempo=std::stoi(temp,nullptr);
        }catch(std::invalid_argument){
          cout<<"Error: read non-integer value";
          return false;
        }
		    if(tempo<0 || tempo>maxColor){
			    cout<<"Error: invalid color value "<<tempo;
			  return false;
	    	}*/
        tempo=std::stoi(temp,nullptr);
		    image[col][row].g=tempo;
        /*if(inFS.eof()){
			    cout<<"Error: not enough color values";
			    return false;
		    }*/
	    	inFS >>temp;
        /*try{
          tempo=std::stoi(temp,nullptr);
        }catch(std::invalid_argument){
          cout<<"Error: read non-integer value";
          return false;
        }*/
        tempo=std::stoi(temp,nullptr);
		    /*if(tempo<0 || tempo>maxColor){
			    cout<<"Error: invalid color value "<<tempo;
			  return false;
	    	}*/
		    image[col][row].b=tempo;
	    }
    }
    try{
      inFS>>tempo;
      if(inFS.good()){
      cout<<"Error: too many color values";
      return false;
      }
    } catch(std::invalid_argument){
    }
    INFO(filename);
    INFO(image);
    INFO(width);
    INFO(height);
  return true;
}

bool outputImage(string filename, Pixel** image, int width, int height) {
    // TODO(student): output an image
    std::ofstream ofs;
    ofs.open(filename);
    if (!ofs.is_open()) {
    cout << "Error: failed to open output file " << filename << endl;
    return false;
  }
  // TODO(student): check if output stream opened successfully
  
  // TODO(student): output preamble
  ofs << "P3\n"<<width<<" "<<height<<endl<<255<<endl;
  
  // TODO(student): output pixels
  for(int row=0;row<height;row++){
    for(int col=0;col<width;col++){
      ofs << image[col][row].r<<" ";
      ofs<<image[col][row].g<<" ";
      ofs<<image[col][row].b<<" ";
    }
  }
  ofs.close();
    INFO(filename);
    INFO(image);
    INFO(width);
    INFO(height);
  return true;
}

int energy(Pixel** image, int column, int row, int width, int height) { 
    // TODO(student): compute the energy of a pixel
    int energyx=0;
    int energyy=0;
    int c1=(column==width-1)?0:column+1;
    int c2=(column==0)?width-1:column-1;
    int r1=(row==height-1)?0:row+1;
    int r2=(row==0)?height-1:row-1;
    
      energyx=pow((image[c1][row].r-image[c2][row].r),2);
      energyx+=pow((image[c1][row].g-image[c2][row].g),2);
      energyx+=pow((image[c1][row].b-image[c2][row].b),2);

      energyy=pow((image[column][r1].r-image[column][r2].r),2);
      energyy+=pow((image[column][r1].g-image[column][r2].g),2);
      energyy+=pow((image[column][r1].b-image[column][r2].b),2);
    
    /*INFO(image);
    INFO(column);
    INFO(row);
    INFO(width);
    INFO(height);*/
  return energyx+energyy;
}

int loadVerticalSeam(Pixel** image, int start_col, int width, int height, int* seam) {
    // TODO(student): load a vertical seam
    int col=start_col;
    seam[0]=start_col;
    int left=-1;
    int right=-1;
    int mid=-1;
    int total=energy(image,col,0,width,height);
    for(int row=1;row<height;row++){
      if(col>0){
        left=energy(image,col-1,row,width,height);
      }
      if(col<width-1){
        right=energy(image,col+1,row,width,height);
      }
      mid=energy(image,col,row,width,height);
      if((col>0&&left<mid)&&(col==width-1||left<right)){
        col=col-1;
        total+=left;
      } else if(col<width-1&&right<mid){
        col=col+1;
        total+=right;
      } else{
        total+=mid;
      }
      seam[row]=col;
    }
    /*INFO(image);
    INFO(start_col);
    INFO(width);
    INFO(height);
    INFO(seam);*/
  return total;
}

int loadHorizontalSeam(Pixel** image, int start_row, int width, int height, int* seam) {
    // TODO(student): load a horizontal seam
    int row=start_row;
    seam[0]=start_row;
    int left=-1;
    int right=-1;
    int mid=-1;
    int total=energy(image,0,row,width,height);
    for(int col=1;col<width;col++){
      if(row>0){
        left=energy(image,col,row-1,width,height);
      }
      if(row<height-1){
        right=energy(image,col,row+1,width,height);
      }
      mid=energy(image,col,row,width,height);
      if((row<width-1&&right<mid)&&(row==0||right<left)){
        row=row+1;
        total+=right;
      } else if(row>0&&left<mid){
        row=row-1;
        total+=left;
      } else{
        total+=mid;
      }
      seam[col]=row;
    }
    /*INFO(image);
    INFO(start_row);
    INFO(width);
    INFO(height);
    INFO(seam);*/
  return total;
}

int* findMinVerticalSeam(Pixel** image, int width, int height) {
    // TODO(student): find min vertical seam
    int* seam=createSeam(height);
    int* minSeam=createSeam(height);
    int temp;
    int min=loadVerticalSeam(image,0,width,height,minSeam);
    for(int col=0;col<width;col++){
      temp=loadVerticalSeam(image,col,width,height,seam);
      if(temp<min){
        min=temp;
        loadVerticalSeam(image,col,width,height,minSeam);
      }
    }
    deleteSeam(seam);
    /*INFO(image);
    INFO(width);
    INFO(height);*/
  return minSeam;
}

int* findMinHorizontalSeam(Pixel** image, int width, int height) {
    // TODO(student): find min horizontal seam
    int* seam=createSeam(width);
    int* minSeam=createSeam(width);
    int temp;
    int min=loadHorizontalSeam(image,0,width,height,minSeam);
    for(int row=0;row<height;row++){
      temp=loadHorizontalSeam(image,row,width,height,seam);
      if(temp<min){
        min=temp;
        loadHorizontalSeam(image,row,width,height,minSeam);
      }
    }
    deleteSeam(seam);
    /*INFO(image);
    INFO(width);
    INFO(height);*/
  return minSeam;
}

void removeVerticalSeam(Pixel** image, int width, int height, int* verticalSeam) {
    // TODO(student): remove a vertical seam
    for(int row=0;row<height;row++){
      for(int col=verticalSeam[row];col<width-1;col++){
        image[col][row].r=image[col+1][row].r;
        image[col][row].g=image[col+1][row].g;
        image[col][row].b=image[col+1][row].b;
      }
    }
    /*INFO(image);
    INFO(width);
    INFO(height);
    INFO(verticalSeam);*/
}

void removeHorizontalSeam(Pixel** image, int width, int height, int* horizontalSeam) {
    // TODO(student): remove a horizontal seam
    for(int col=0;col<width;col++){
      for(int row=horizontalSeam[col];row<height-1;row++){
        image[col][row].r=image[col][row+1].r;
        image[col][row].g=image[col][row+1].g;
        image[col][row].b=image[col][row+1].b;
      }
    }
    /*INFO(image);
    INFO(width);
    INFO(height);
    INFO(horizontalSeam);*/
}
