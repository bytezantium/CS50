// Problem Set 4: Recover

// Implement a program called recover that recovers JPEGs from a forensic image

#include <cs50.h>
#include <stdio.h>
#include <stdint.h>

// declare functions used
bool start_JPEG(unsigned char x[]);

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    char *infile = argv[1]; // remember input filename
    FILE *inptr = fopen(infile, "r"); // open infile
    if (!inptr) // check return for NULL
    {
        fprintf(stderr, "Could not open %s\n", infile);
        return 2;
    }

    // Iniitalize variables
    char filename[8]; // temporary storage names: ###.jpg - named in order in which found, starting at 000.
    int jpgcounter = 0; // image counter
    FILE *jpg = NULL; // file pointer to JPEG outfiles

    // repeat until end of infile
    while (true)
    {
        // read and store infile until EOF
        unsigned char buffer[512]; // temporary storage
        fread(buffer, 1, 512, inptr); // read into infile blockwise
        if (feof(inptr)) // stop reading into infile at EOF
        {
            break;
        }

        if (start_JPEG(buffer) && jpg != NULL) // detect start of a non-first JPEGs
        {
            fclose(jpg);    // close previous, completed JPEG
            jpgcounter++; // update counter for JPEG filenames
        }

        if (start_JPEG(buffer)) // detect beginning of JPEG (also the first JPEG)
        {
            sprintf(filename, "%03i.jpg", jpgcounter); // name JPEG (starts with 000 for first JPEG)
            jpg = fopen(filename, "w"); // open JPEG for writing
            if (!jpg) // check for NULL
            {
                fprintf(stderr, "Could not create %s\n", filename);
                return 3;
            }
        }

        // write to opened JPEG outfiles
        if (jpg != NULL)
        {
            fwrite(buffer, 1, 512, jpg);
        }

    }
    // close opened files
    fclose(jpg); // last opened JPEG file
    fclose(inptr); // opened infile

    return 0;
}

// function to check for start of new JPEG
bool start_JPEG(unsigned char x[])
{
    if (x[0] == 0xff &&
        x[1] == 0xd8 &&
        x[2] == 0xff &&
        (x[3] & 0xf0) == 0xe0)
    {
        return true;
    }
    else
    {
        return false;
    }
}





