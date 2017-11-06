/* CS50:          https://cs50.harvard.edu/weeks
*  Problem set 2: https://docs.cs50.net/2017/x/psets/4/pset4.html
*  Problem 2:     https://docs.cs50.net/problems/resize/less/resize.html
*
* The program resize bmp by a given factor.
*/


#include <stdio.h>
#include <stdlib.h>
#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4 || atoi(argv[1]) > 100)
    {
        fprintf(stderr, "Usage: ./resize n infile outfile\n n must be <= 100\n");
        return 1;
    }

    // remember filenames
    int n = atoi(argv[1]);
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // determine padding for infile and outfile
    int padding_old =  (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int padding_new =  (4 - (bi.biWidth * n * sizeof(RGBTRIPLE)) % 4) % 4;

    // create headers for outfile
    BITMAPFILEHEADER bf_new = bf;
    BITMAPINFOHEADER bi_new = bi;

    // set outfile's biWidth, biHeight, biSizeImage, bfSize
    bi_new.biWidth *= n;
    bi_new.biHeight *= n;
    bi_new.biSizeImage = abs(bi_new.biHeight) * (bi_new.biWidth * sizeof(RGBTRIPLE) + padding_new);
    bf_new.bfSize = bi_new.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf_new, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi_new, sizeof(BITMAPINFOHEADER), 1, outptr);

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {

        // iterate over infile's scanline for n times
        for (int m = 0; m < n; m++)
        {

            // go back to the beggining of the scanline
            if (m != 0)
            {
                fseek(inptr, -(bi.biWidth * sizeof(RGBTRIPLE) + padding_old), SEEK_CUR);
            }

            // iterate over pixels in scanline
            for (int j = 0; j < bi.biWidth; j++)
            {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                // write RGB triple to outfile
                for (int k = 1; k <= n; k++)
                {
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }

            // skip over padding, if any (inptr)
            fseek(inptr, padding_old, SEEK_CUR);

            // add padding, if any (outptr)
            for (int k = 0; k < padding_new; k++)
            {
                fputc(0x00, outptr);
            }
        }
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
