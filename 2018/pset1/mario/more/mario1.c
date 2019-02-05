#include <stdio.h>
#include <cs50.h>

int height, row, space, dash;

int main(void)
{
    do
    {
        height = get_int("Height: ");
    }
    while (height < 0 || height > 23);

    for (row = 0; row < height; row++)
    {
        for (space = (height - row - 1); space > 0; space--)
        {
            printf(" ");
        }
        for (dash = 0; dash < row + 1; dash++)
        {
            printf("#");
        }
        {
            printf("  ");
        }
        for (dash = 0; dash < row + 1; dash++)
        {
            printf("#");
        }

        printf("\n");
    }

}