/* CS50:          https://cs50.harvard.edu/weeks
*  Problem set 1: https://docs.cs50.net/2017/x/psets/1/pset1.html
*  Problem 4:     https://docs.cs50.net/problems/greedy/greedy.html
*
* The code asks user to specify change requared by a customer and prints minimum number of coins with which said change can be made.
*/

#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{

    // initialize variables
    float change;
    int cents, quarter_c, dime_c, nickel_c, penny_c;
    int quarter = 25, dime = 10, nickel = 5, penny = 1;

    // prompt for integer
    do
    {
        change = get_float("Change owed (example: 1.52 is 1 dollar 52 cents): ");
    }
    while (change < 0);

    // convert input (float) into cents (int)
    cents = round(change * 100);

    // go through each coin and save whats left and coins used
    // should be a loop, but at this time no idea how to create an array
    quarter_c = cents / quarter;
    cents = cents % quarter;

    dime_c = cents / dime;
    cents = cents % dime;

    nickel_c = cents / nickel;
    cents = cents % nickel;

    penny_c = cents / penny;

    // print the results
    printf("Coins used: %i. Number of qarters, dimes, nickels and cents respectively: %i, %i, %i, %i\n",
           quarter_c + dime_c + nickel_c + penny_c, quarter_c, dime_c, nickel_c, penny_c);

    // return a minimum number of coins to give change (for auto-testing)
    printf("%i\n", quarter_c + dime_c + nickel_c + penny_c);
    return 0;

}
