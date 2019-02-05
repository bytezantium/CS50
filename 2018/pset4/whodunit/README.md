# Questions

## What's `stdint.h`?

`stdint.h` is a header file in the C standard library that includes exact-width integer types
such as `uint8_t`, `uint32_t`, `int32_t`, etc. .

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?
They were introduced inside `stdint.h` in C99, to allow programmers to write more portable code,
by providing a set of typedefs that specify exact-width integer types, together with the
defined minimum and maximum allowable values for each type, using macros.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

`BYTE`:  `1`
`DWORD`: `4`
`LONG`:  `4`
`WORD`:  `2`

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

ASCII: `BM`
Decimal: `66` `77`
Hexadecimal: `0x42` `0x4d`

## What's the difference between `bfSize` and `biSize`?

`bfSize`: the size, in `bytes`, of the bitmap file.
`biSize`: the number of `bytes` required by the BITMAPINFOHEADER structure.

## What does it mean if `biHeight` is negative?

If `biHeight` is `negative`, indicating a `top-down DIB`, biCompression must be either
`BI_RGB` or `BI_BITFIELDS`. `Top-down DIBs` cannot be `compressed`.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

The `biBitCount` specifies the number of `bits-per-pixel`, and thus the `BMP's` color depth.

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

`fopen` might return `NULL`, if it cannot find enough space in `memory` to be allocated for execution.

## Why is the third argument to `fread` always `1` in our code?

Since we are `reading` from all files `pixel` by `pixel` or `RGB triple` by `RGB triple`.
Hence, the unit we are iterating over is a single `pixel` or `RGB triple`.
Hence, the number or quantity of units `fread` is iterating over at one time is 1.

## What value does line 65 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

`int padding = 3`

## What does `fseek` do?

Whenever we are `reading into` a `file` there is the `file position indicator`, basically
like our cursor, that keeps track of where in the `file` we are. So if we ever want
to move that cursor, we use the `fseek`function.

The `fseek` function: `fseek(File *, offset, from);`

The function takes the `file pointer: File *` to seek over, an `offset`, the number of bytes
to move the cursor, and then `from` - a realtive position from which to move the `file position indicator`, or cursor.
The `from` input can have the arguments `SEEK_CUR` (current position in file), `SEEK_SET`(beginning of file),
or `SEEK_END`(end of file).

## What is `SEEK_CUR`?

`SEEK_CUR` is a `parameter` passable into the `fseek` function's `from` argument.
It tells the `file position indicator` to move `offset` number of bytes from its current position in file.

## Whodunit?

It was Professor Plum with the candlestick, in the library.
