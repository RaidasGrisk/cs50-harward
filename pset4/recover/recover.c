/* CS50:          https://cs50.harvard.edu/weeks
*  Problem set 2: https://docs.cs50.net/2017/x/psets/4/pset4.html
*  Problem 2:     https://docs.cs50.net/problems/resize/less/resize.html
*
* The program recovers deteleted JPEG's from a given storage.
*/

#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2 || fopen(argv[1], "r") == NULL)
    {
        fprintf(stderr, "Usage: ./recover storage\n");
        return 1;
    }

    // init variables
    char image_name[8];
    int image_id = 0;
    unsigned char buffer[512];

    // open storage and destination file
    FILE *file = fopen(argv[1], "r");
    FILE *img = fopen(image_name, "w");

    // loop through storage
    while (fread(&buffer, 512, 1, file) == 1)
    {
        // check if new JPEG is found
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
            {
                // create new image
                fclose(img);
                sprintf(image_name, "%03d.jpg", image_id);
                img = fopen(image_name, "w");
                image_id++;
            }

        // write image
        if (image_id != 0)
        {
            fwrite(&buffer, 512, 1, img);
        }
    }

    // finish
    fclose(file);
    return 0;

}
