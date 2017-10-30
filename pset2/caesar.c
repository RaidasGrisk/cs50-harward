/* CS50:          https://cs50.harvard.edu/weeks
*  Problem set 2: https://docs.cs50.net/2017/x/psets/2/pset2.html
*  Problem 2:     https://docs.cs50.net/problems/caesar/caesar.html
*
* The code asks user to provide text and key. Returns Caesar ciphered text (https://en.wikipedia.org/wiki/Caesar_cipher)
*/

#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[]){

  if (argc == 1 || argc > 2){
    printf("You've entered too few or too many arguments. Please type in a single non-negative int: ");
    return 1;
  }

  else{

    // prompt for string
    string plaintext = get_string("plaintext:  ");

    // initiate other variables
    int str_len = strlen(plaintext);
    int ciphered_char_id;

    // cast key from string to int
    int key = atoi(argv[1]);

    // print ciphertext
    printf("ciphertext: ");

    // loop through each letter and cipher
    for (int c = 0; c < str_len; c++){

      // get ciphered_char_id if lower (97 - 122)
      if (islower(plaintext[c])){
        ciphered_char_id = ((plaintext[c] - 97 + key) % 26) + 97;
      }

      // get ciphered_char_id if upper (65 - 90)
      if (isupper(plaintext[c])){
        ciphered_char_id = ((plaintext[c] - 65 + key) % 26) + 65;
      }

      // get ciphered_char_id if not an alphabet letter (do not cipher)
      if (isalpha(plaintext[c]) == 0){
        ciphered_char_id = plaintext[c];
      }

      // print ciphertext
      printf("%c", ciphered_char_id);
    }

    // return
    printf("\n");
    return 0;

  }

}
