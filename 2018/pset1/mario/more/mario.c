#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // Declaring integer variables
    int height, row, space, dash;

    // Prompt user for height
    do
    {
        height = get_int("Height: ");
    }
    while (height < 0 || height > 23);

    // Print rows
    for (row = 0; row < height; row++)
    {
        // Print spaces for left half pyramid
        for (space = (height - row - 1); space > 0; space--)
        {
            printf(" ");
        }

        // Print dashes for left half pyramid
        for (dash = 0; dash < row + 1; dash++)
        {
            printf("#");
        }

        // Print spaces in middle
        for (int i = 1; i <= 1; i++)
        {
            printf("  ");
        }

        // Print dashes in right half pyramid
        for (dash = 0; dash < row + 1; dash++)
        {
            printf("#");
        }

        printf("\n");
    }

}