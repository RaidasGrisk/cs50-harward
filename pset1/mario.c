/* CS50:          https://cs50.harvard.edu/weeks
*  Problem set 1: https://docs.cs50.net/2017/x/psets/1/pset1.html
*  Problem 3:     https://docs.cs50.net/problems/mario/more/mario.html
*
* The code asks user to specify pyramid height and then prints out mario-pyramid accordingly.
*/

#include <stdio.h>
#include <cs50.h>

int main(void)
{

    // initialize variables
    int height, spaces, hashes, row;

    // prompt for integer
    do
    {
        height = get_int("Let build a Mario pyramid! Buy how high? Give me a positive int between 0 and 24: ");
    }
    while (height < 0 || height > 23);

    // loop through each row
    for (row = 1; row <= height; row++)
    {

        // print spaces
        for (spaces = height; spaces > row; spaces--)
        {
            printf(" ");
        }

        // print hashes (and one space in the middle)
        for (hashes = 0; hashes <= row * 2; hashes++)
        {
            if (hashes == row)
            {
                printf(" ");
            }
            else
            {
                printf("#");
            }
        }

        // jump to next line
        printf("\n");

    }

    return 0;

}
