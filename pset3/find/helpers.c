/* CS50:          https://cs50.harvard.edu/weeks
*  Problem set 3: https://docs.cs50.net/2017/x/psets/3/pset3.html
*  Problem 1:     https://docs.cs50.net/problems/find/less/find.html
*
*  The code implements:
*  binary_search
*  counting_sort
*  selection_sort
*  bubble_sort
*/


/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */

#include <cs50.h>
#include "helpers.h"

// binary search algorithm
bool binary_search(int value, int values[], int n)
{
    // mark first and last index of the list
    int first = 0;
    int last = n - 1;

    // binary search
    while (first <= last)
    {
        int middle = (last + first) / 2;

        if (values[middle] == value)
        {
            return true;
        }
        else if (values[middle] > value)
        {
            last = middle - 1;
        }
        else if(values[middle] < value)
        {
            first = middle + 1;
        }
    }

    return false;
}

// selection sort algorithmn
void selection_sort(int values[], int n)
{

    // temporary int for swapping
    int temp;

    // loop through each value from the beggining
    for (int i = 0; i < n; i++)
    {

        // compare the value with the rest of values in front
        int i_min = i;
        for (int j = i + 1; j < n; j++)
        {
            if (values[i_min] > values[j])
            {
                i_min = j;
            }
        }

        // swap
        if (i != i_min)
        {
            temp = values[i_min];
            values[i_min] = values[i];
            values[i] = temp;
        }
    }
}

// bubble sort algorithm
void bubble_sort(int values[], int n)
{

    // temporary int for swapping and bool for sorted/not sorted
    int temp;
    bool sorted = false;

    while(sorted != true)
    {
        sorted = true;
        for (int i = 0; i < n-1; i++)
        {
            if (values[i] > values[i+1])
            {
                temp = values[i+1];
                values[i+1] = values[i];
                values[i] = temp;
                sorted = false;
            }
        }
    }
}


/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    if (n < 0)
    {
        return false;
    }
    else
    {
        return binary_search(value, values, n);
    }
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    selection_sort(values, n);
    return;
}


