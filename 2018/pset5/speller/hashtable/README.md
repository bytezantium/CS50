# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?

According to Merriam-Webster's Medical Dictionary,
pneumonoultramicroscopicsilicovolcanoconiosis is a
pneumoconiosis caused by inhalation of very fine
silicate or quartz dust.

## According to its man page, what does `getrusage` do?

int getrusage(int who, struct rusage *usage);

getrusage() returns resource usage measures for WHO, which can be one of the following:
    RUSAGE_SELF
        Return  resource  usage  statistics for the calling process, which is the sum of resources used by
        all threads in the process.
    RUSAGE_CHILDREN
        Return resource usage statistics for all children of the calling process that have terminated  and
        been  waited  for.  These statistics will include the resources used by grandchildren, and further
        removed descendants, if all of the intervening descendants waited on their terminated children.
    RUSAGE_THREAD (since Linux 2.6.26)
        Return resource usage statistics for the calling thread.

The resource usages are returned in the structure pointed to by USAGE, which has the following form:
           struct rusage {
               struct timeval ru_utime; /* user CPU time used */
               struct timeval ru_stime; /* system CPU time used */
               long   ru_maxrss;        /* maximum resident set size */
               long   ru_ixrss;         /* integral shared memory size */
               long   ru_idrss;         /* integral unshared data size */
               long   ru_isrss;         /* integral unshared stack size */
               long   ru_minflt;        /* page reclaims (soft page faults) */
               long   ru_majflt;        /* page faults (hard page faults) */
               long   ru_nswap;         /* swaps */
               long   ru_inblock;       /* block input operations */
               long   ru_oublock;       /* block output operations */
               long   ru_msgsnd;        /* IPC messages sent */
               long   ru_msgrcv;        /* IPC messages received */
               long   ru_nsignals;      /* signals received */
               long   ru_nvcsw;         /* voluntary context switches */
               long   ru_nivcsw;        /* involuntary context switches */
           };

## Per that same man page, how many members are in a variable of type `struct rusage`?

16

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?

If we passed them by value, hence only as copies on a stack frame, `struct rusage before` and/or `struct rusage after` might be
`popped off` the `call stack` prior to our comparison calculation `calculate ()` between `before` and `after`.
This would run the high risk of preventing any meaningful comparison calculations in terms of `benchmarking` the `rusage` efficiency of our `functions`
because the inputs to `calculate()` could likely be `garbage values` left from other programs that have used that variables' stack frame in the meantime.

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.

Main opens the inputted text file for reading - if not NULL. Before main enters the for loop it initializes the int variables index and words to 0. Main also
declares a char word[LENGTH + 1]. In this array main will store the words of the text, as long as they do not exceed the LENGTH and the + 1 for NUL.
Main then enters the for loop by virtue of which it accesses the characters in the opened file one by one via fgetc(). It does so until it reaches 'EOF'.
If the character fulfills the conditions it is structured into word[] at the current index.
In order for each contiguous characters to be added into a word, they must fulfill `Condition 1`:

`Condition 1`: `isalpha()` must return `true` `OR` the character is an `apostrophe`, only if the `index > 0`, hence if it is not at the beginning of a new word.

As long as `condition 1` is met, each contiguous `character` read from the text file is added to a `word[]` at the current `index`. After a `character` is `inserted` into `word[]`,
the `index` is `incremented` by 1. How does `main` know when an array of characters has completed a word? Well, if the `character` does not fulfill `condition 1`
anymore, we must have reached a space between two words, for example a `space bar` or a `comma` in the `text`. If this is the case `main` marks the word structure
as complete by checking via `else if (index > 0)` if a `word` is currently being inserted into, and then main terminates the current word by putting the `NUL` character
(`\0`) to mark the cohesive end of a `string` of characters i.e. our `word`. The`words` counter is incremented. The spelling is checked. The `time_check` benchmark is calculated.
If misspelled the word is `printed`, and the `misspellingss` counter is incremented.
Finally, The `index` is then set to `0` so `main` can prepare for the next word to be written.

`Condition 1.1`: `if (index > LENGTH)` Ignore alphabetical strings too long to be words
There is a caveat to the fulfillment of `condition 1`. The word size cannot exceed the size of the array - i.e. the predefined constant `LENGTH` and + 1 for `NUL`.
If it does so, the `while ((c = fgetc(file)) != EOF && isalpha(c));` loop moves the `file position indicator` forward int the read into text file until we either
reach `EOF` or a beginning of a new word signified by `isalpha(c)`not returning true any more, as previously explained. The `word[]`array that we have begun inserting
into is not terminated with a `\0` (`NUL`) characters, lest we want to mark the end of a legal word. Instead, the space allocated memory for the oversize word
array is left untouched in memory as `garbage value`.
The `index` is then set to `0` again, so we can prepare for the insertion of new legal characters into a new word, or if `EOF` we `break` out of the `for loop`.

What if a character does not fulfill condition 1?
`Condition 2`: `else if (isdigit(c))`
This part of the `for loop` ignores words with numbers. Similar to what happens if `condition 1.1` is met, if a `character` is not `alphabetical`,
the code inside this condition moves the `file position indicator` until the illegal `string` of `alphanumerical` `characters` has ended or 'EOF' is reached.
Once the former condition is met the `index` is set to `0` to prepare for a new word. If `EOF` is met, we `break` out of the `for loop`.

## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?
We use `fgetc`over `fscanf`, in order to insert into a limited size `array`, without risking going outside the allocated size of our word arrays. Thus
avoiding touching memory that we have not allocated to our variable, we derisk `segmentation faults` in our program.
We also use `fgetc`to be able to differentiate between `alphabetical` and `alphanumerical` words. This presmuably allows us to make our
`spell check function` later more time efficient, by already `sorting` out `non-alphabetical words`, that would fail the test anyway.

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?
To tell the `compiler` that, if `values` are passed in as `constant` `parameters` to a `function`, these `constant variables`
are in `read-only` mode and will keep their `values` until the `function` `exits`.
This can increase the efficiency of code and reduce its `runtime`.


