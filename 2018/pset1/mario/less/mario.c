#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //Initialize variables h for height and r for rows

    int h;
    int r;

    // Prompt user for height between 0 and 23

    do
    {
        h = get_int("Height: ");
    }
    while (h < 0 || h > 23);


    // Print number of rows r to match height

    for (r = 0; r < h; r++)
    {
        // Print number of spaces in each row
        for (int s = (h - r - 1); s > 0; s--)
        {
            printf(" ");
        }

        // Print number of dashes per row
        for (int d = 1; d <= (r + 2); d++)
        {
            printf("#");
        }

        printf("\n");
    }
}