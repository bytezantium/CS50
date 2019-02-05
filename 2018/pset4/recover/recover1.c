#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>


int main (int argc, char *argv[])
{
    // correct usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover infile\n");
        return 1;
    }
    // remember filename and open for reading
    char *infile = argv[1];
    FILE *inptr = fopen(infile, "r");
    // check return for NULL
    if (!inptr)
    {
        fprintf(stderr, "Cannot open infile\n");
        return 2;
    }

    // needed storage variables
    unsigned char buffer[512];
    char filename[8];
    int jpgcounter = 0;
    FILE *jpg = NULL;

    while(true)
    {
        fread(buffer, 1, 512, inptr);

        // stop at EOF
        if (feof(inptr))
        {
            break;
        }

        // check for JPEG start
        bool JPEG = (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0);

        // check if beginning of next JPEG (not the first one)
        if (JPEG && jpg != 0)
        {
            fclose(jpg);
            jpgcounter++;
        }

        // opening a new JPEG
        if (JPEG)
        {
            sprintf(filename, "%03i.jpg", jpgcounter);
            jpg = fopen(filename, "w");
            if (!jpg)
            {
                fprintf(stderr, "Could not open %s\n", filename);
                return 3;
            }
        }

        // write into opened jpg
        if (jpg != NULL)
        {
            fwrite(buffer, 512, 1, jpg);
        }

    }
    // close all open files
    fclose(inptr);
    fclose(jpg);

    // successful exit
    return 0;
}