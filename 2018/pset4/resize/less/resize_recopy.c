// CS50x Problem Set 4: Resize - less comfortable

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // Convert resize_factor to integer
    int resize_factor = atoi(argv[1]);

    // ensure proper usage
    if (argc != 4 || resize_factor < 1 || resize_factor > 100)
    {
        fprintf(stderr, "Usage: resize factor 1-100 infile outfile\n");
        return 1;
    }

    // remember filenames
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

    // store infile's Width and Height
    long infile_Width = bi.biWidth;
    long infile_Height = abs(bi.biHeight);

    // store infile's padding
    int infile_padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // update Height and Width for outfile
    bi.biWidth *= resize_factor;
    bi.biHeight *= resize_factor;

    // update outfile's padding
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // update biSize Image and bfSize for outfile
    bi.biSizeImage = ((sizeof(RGBTRIPLE) * bi.biWidth) + padding) * abs(bi.biHeight);
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);


    // iterate over infile's scanlines
    for (int i = 0; i < infile_Height; i++)
    {

        for (int n = 0; n < resize_factor - 1; n++)
        {
            // iterate over pixels in scanline
            for (int j = 0; j < infile_Width; j++)
            {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                // write RGB triple to outfile and resize horizontally
                for (int m = 0; m < resize_factor; m++)
                {
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }

            // then add outfile's padding
            for (int k = 0; k < padding; k++)
            {
                fputc(0x00, outptr);
            }

            // send infile cursor back
            fseek(inptr, -infile_Width * sizeof(RGBTRIPLE), SEEK_CUR);

        }

        for (int j = 0; j < infile_Width; j++)
        {
            RGBTRIPLE triple;

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

            // write RGB triple to outfile and resize horizontally
            for (int m = 0; m < resize_factor; m++)
            {
                fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
            }
        }
        // padding
        for (int k = 0; k < padding; k++)
        {
            fputc(0x00, outptr);
        }

        // skip over infile's padding, if any
        fseek(inptr, infile_padding, SEEK_CUR);

    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
