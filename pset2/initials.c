/* CS50:          https://cs50.harvard.edu/weeks
*  Problem set 2: https://docs.cs50.net/2017/x/psets/2/pset2.html
*  Problem 4:     https://docs.cs50.net/problems/initials/more/initials.html
*
* The code asks user to input her/his full name and prints out the name's initials.
*/

#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

int main(void)
{

    // prompt user for full name
    string name = get_string("");

    // print name's initials if previous char was not ' ' or \0 and this char is not ' '
    for (int i = 0; i < strlen(name); i++)
    {
        if (name[i] != ' ' && (name[i - 1] == ' ' || name[i - 1] == '\0'))
        {
            printf("%c", toupper(name[i]));
        }
    }

    // return
    printf("\n");
    return 0;

}
