#include "EasyBMP/EasyBMP.h"
#include <string.h>

void mosaic(BMP* input, BMP* output, int width, int height) {
  for (int x=0; x<width; ++x) {
    for (int y=0; y<height; ++y) {
      if ((x%2==1)&&(y%2==0)) {
        //Pixel is red part of Bayer Array
        (*output)(x,y)->Red = (*input)(x,y)->Red;
        (*output)(x,y)->Blue = 0;
        (*output)(x,y)->Green = 0;
      }
      else if ((x%2==0)&&(y%2==1)) {
        //Pixel is blue part of Bayer Array
        (*output)(x,y)->Red = 0;
        (*output)(x,y)->Blue = (*input)(x,y)->Blue;
        (*output)(x,y)->Green = 0;
      }
      else {
        //Pixel is green part of Bayer Array
        (*output)(x,y)->Red = 0;
        (*output)(x,y)->Blue = 0;
        (*output)(x,y)->Green = (*input)(x,y)->Green;
      }
    }
  }
  return;
}

int main(int argc, char* argv[]) {
  if (argc != 3) {
    std::cerr <<
    "\nProgram Usage:\n\n" <<
    "   mosiacer <input> <output>\n" <<
    "     <input> - Input filename (.bmp)\n" <<
    "     <output> - Output filename (.bmp)\n\n";
    return 0;
  }
  char* input_file = argv[1];
  char* output_file = argv[2];

  BMP* input_image = new BMP();
  BMP* output_image = new BMP();

  input_image->ReadFromFile(input_file);
  int width = input_image->TellWidth();
  int height = input_image->TellHeight();
  output_image->SetSize(width, height);
  output_image->SetBitDepth(24);

  mosaic(input_image, output_image, width, height);

  output_image->WriteToFile(output_file);
  return 0;
}
