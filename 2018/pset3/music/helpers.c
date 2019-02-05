// Helper functions for music

#include <cs50.h>
#include <math.h>
#include <string.h>

#include "helpers.h"

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    // Extract numerator and denominator and convert from string to int
    int numerator = fraction[0] - '0';
    int denominator = fraction[2] - '0';

    if (denominator != 8)
        do
        {
            numerator *= 2;
            denominator *= 2;
        }
        while (denominator != 8);

    return numerator;
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    int octave = note[strlen(note) - 1] - '0';
    char letter = note[0];
    char accidental = ' ';
    if (strlen(note) == 3)
    {
        accidental = note[1];
    }

    double frequency;

    // Adjust for letter
    if (letter == 'C')
    {
        frequency = 440.0 / pow(2, 9.0 / 12);
    }

    if (letter == 'D')
    {
        frequency = 440.0 / pow(2, 7.0 / 12);
    }

    if (letter == 'E')
    {
        frequency = 440.0 / pow(2, 5.0 / 12);
    }

    if (letter == 'F')
    {
        frequency = 440.0 / pow(2, 4.0 / 12);
    }

    if (letter == 'G')
    {
        frequency = 440.0 / pow(2, 2.0 / 12);
    }

    if (letter == 'A')
    {
        frequency = 440.0;
    }

    if (letter == 'B')
    {
        frequency = 440.0 * pow(2, 2.0 / 12);
    }

    // Adjust for octave
    if (octave > 4)
    {
        frequency *= pow(2.0, (octave - 4));
    }

    else if (octave < 4)
    {
        frequency /= pow(2.0, (4 - octave));
    }

    // Adjust for accidentals
    if (accidental == '#')
    {
        frequency *= pow(2.0, 1.0 / 12.0);
    }

    else if (accidental == 'b')
    {
        frequency /= pow(2.0, 1.0 / 12.0);
    }

    // Return the frequency rounded to nearest integer value
    return round(frequency);
}

// Determines whether a string represents a rest
bool is_rest(string s)
{
    // Checks if there is an end of line and no string
    if (strlen(s) == 0)
    {
        return true;
    }
    else
    {
        return false;
    }

}
