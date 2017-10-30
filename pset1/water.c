/* CS50:          https://cs50.harvard.edu/weeks
*  Problem set 1: https://docs.cs50.net/2017/x/psets/1/pset1.html
*  Problem 2:     https://docs.cs50.net/problems/water/water.html
*
* The program asks user the number of minutes she/he took a shower for and
* prints out the number of watter bottles equivalent to the water used.
*/

#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // prompt for integer
    int minutes = get_int("How many minutes it took you to shower?\n");

    // estimate number of water bottles
    int bottles = minutes * 12;

    // print and return
    printf("That is equivalent to %i number of drinking water bottles\n", bottles);
    return 0;
}