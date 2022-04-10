#################################
 Fill empty drive space in Xenix
#################################

:title: Fill empty drive space in Xenix
:tags:
:layout: post
:date: 2022-04-10 19:00:00 +0200
:comments: true
:category: blog
:description:
:lang: en

A couple of months ago, `@blitzclone <https://twitter.com/blitzclone>`_ and I
installed Xenix on one of my vintage machines. He documented the process in
`a somewhat amusing thread on Twitter <https://twitter.com/blitzclone/status/1481698790583279619>`_.
While installing and using Xenix is quite a hassle if you are used to modern Unix systems,
I find it impressive what SCO and Microsoft were able to achieve with the very primitive
hardware back in the day (remember, on those systems,
RAM is still measured in Kilobytes, and there is not even a proper MMU).

Still, Xenix never had a chance to succeed in the market: "Serious" mainframes ran more versatile Unix distributions,
usually specific to their vendor, whereas PCs back then often did not meet the high requirements.
Many of them were still sold without a hard drive, which is a vital thing to have for Unix System V
and thereby also for Xenix. As we know today, Microsoft decided to focus on DOS development instead,
and introduced graphical shells for that OS called Windows (you may have heard of that product).

Nevertheless, Xenix was, for a short period of time, the cheapest and hence most installed Unix around.
Then BSD was open-sourced, and Linux came into being, and Xenix soon faded out of the public eye.
The operating system remained fairly common in its niche of point of sales solutions and on-site controller networks
for some time. Until a couple of years ago, the last thing to be heard of Xenix was the occasional failing system,
tucked away somewhere and subsequently forgotten, leaving their administrators hectically searching for replacement
parts or new solutions. Among those surprised companies was our trustily disorganized
`German Railway <https://www.heise.de/newsticker/meldung/Wenn-Computer-Oldies-nicht-mehr-wollen-Update-135968.html>`_.
These days, though, I guess all productive Xenix system have either been virtualized or decommissioned.

In this article, however, I would like to leave history aside and
focus on my getting to know Xenix and talk about the experience of programming on an old Unix.
If you would like to know more about Xenix itself, have a look at
the `Computer History Wiki's <https://gunkies.org/wiki/Xenix>`_ page on the subject,
which details the various versions of Xenix and quirks thereof.

I will also not go into further
details here explaining how exactly we got Xenix to work,
as that would probably warrant at least one
separate article. You may want to have a look at "Fun with virtualization", where you can find a whole
`article series <https://virtuallyfun.com/wordpress/category/xenix/>`_ about installing and configuring Xenix.

Motivation
----------

After I was done with the installation, I created a backup of the hard drive in the computer,
largely because I was afraid that I would break the system and then have to start the whole procedure again from scratch.
First, I connected a Raspberry Pi to the machine, using a null modem cable and a USB-to-serial adapter
on the minicomputer.
I went on to fork ELKS, a Linux kernel derivative designed to support vintage computers from the original IBM PC onwards.
You can find my fork and the changes I made on `GitHub <https://github.com/Logout22/elks/commits/xenix>`_.
Then, I used a Gotek virtual floppy drive with a custom-built image of my version of ELKS,
and some scripts on the Raspberry Pi, to create a hard disk image file via SLIRP and FTP.
I have put the scripts in my ELKS repository as well, in case you are wondering how exactly that worked.

When I analyzed the hard-drive dump using the ``strings`` command on Linux, in the hopes of finding the hello world program
that Julian and I had written, I could still see some plain-text fragments of the previous owner's data, e.g. letters
that he must have written on the previously installed DOS system.
I wanted to clean them up, out of fairness, but also because I thought that should be a simple exercise to get to know
software development on old Unix. Also, as far as I could tell, Xenix has dd, but no /dev/zero device,
so I would have to write the filler program myself, in plain old K&R C.

To better explain the problems that I faced despite the simple task, we will go over the source code piece by piece.
The complete source code can be found on `Codeberg <https://codeberg.org/Logout/fill-space>`_.

In the sections that follow, I will assume that you have some basic knowledge of the modern C language (i.e. ANSI C and beyond).

The program
-----------

To start off, I needed to store the data (i.e. zeroes) that I wanted to write to disk somewhere.
I assumed that old compilers would not reserve very high amounts of stack space (especially on a 286 with its weird segmentation logic),
so I declared my zero buffer globally:

.. code-block:: c

    char zero_buffer[BLOCK_SIZE];

By the way, all constants, like BLOCK_SIZE here, need to be macros declared using #define. That may seem strange
to you if you are used to modern C++ development for instance, but in C, const values cannot be used for array bounds
and other statically defined values because they are not, by definition, available at compile time.

While that may take some time to get used to and look a bit ugly, it is still more or less readable code.
What really killed me is the function declaration syntax of ancient C:

.. code-block:: c

    void main(argc,argv)
      int argc;
      char** argv;
    {

Why did Kernighan and Ritchie (RIP) have to do it like that? I do not get that. From what I read, it was simply
their convention, and the so-called C++-style declaration which is common nowadays was only introduced with the later ANSI C.
But as far as I can see, none of the languages that inspired C, neither ALGOL nor BCPL for example,
have such a weird syntax to declare their function headers. Did they simply like it better that way?
Was it a limitation of the contemporary compilers? If you know more about this, please send me a message!

Something that I already knew, on the other hand, but which also annoys me, is that
all variables must be declared at the beginning of the function, or you will simply get a syntax error.
So here they come, fanfares!

.. code-block:: c

    FILE* filler = NULL;
    unsigned long blocks_written, blocks_per_iteration;
    unsigned long chunk_count, remaining_blocks;
    int i, j;
    char confirm;

As a matter of fact, no one knows at this point what all of these will be for, and no one cares.
If anything, this convention is an invitation to leave half of the variables uninitialized,
to give them all single-letter names that are easy to remember further down, and to reuse them wherever you can.
This suddenly gives you a hint why so many programming anti-patterns came into existence originally.
I understand that compilers back then were fairly limited, but I cannot imagine that it would have been impossible
to add a separate pass that searches for all declarations and reserves the required heap space.
Here, again, one can look at other contemporary languages, like Pascal or BCPL, that did not declare everything upfront.

Next, we do some input value checks. Returning from main() is not well-defined before C99 as far as I know, so
I opted to use the exit() function to return control flow, which thankfully worked:

.. code-block:: c

    if (argc < 2) {
        printf("Please supply a block count target.\n");
        exit(1);
    }

memset() and atol() also existed, which was a plus!

.. code-block:: c

    memset(zero_buffer, 0, BLOCK_SIZE);
    remaining_blocks = atol(argv[1]);

Next, we are looking at the progress indicator. Such a mechanism is useful to detect hangs in general,
but in this particular case, the system is also shared
through the Raspberry Pi gateway that I mentioned earlier.
Logging in from a different user still gives you the same serial port, so
producing some output regularly tells the new user that the serial terminal is still busy.

My first approach was to use ANSI characters for a sort of interactive progress bar,
and organize the work in threads:
One for progress monitoring and one for writing.
This idea did not come to fruition because there was no reliable way to wait for a certain time on this system:
There was no sleep() defined in the standard library, and when
I tried select() without sockets, the system call did not wait as I had expected.

As that approach did not work out, I decided
to split the data to be written into larger chunks, and display a short line indicating progress whenever
one of those blocks was completed.

If you think about it, it also does not really make sense to use threads on a single-core machine.
Still, it would have been a neat demonstration of Xenix' scheduling capabilities.
Maybe I will get around to it in a future project.

While composing the progress line, I realized that printf did not expect more than one parameter to substitute,
and only printed garbage for the second one. I am pretty sure that this is a toolchain bug,
but I would not rule out that early versions of C simply did not iterate further. Hence, e.g. the debug output
in the end looks like this:

.. code-block:: c

    printf("Wrote %u blocks, ", blocks_written);
    printf("%u remaining\n", remaining_blocks);

When trying to compute the necessary data ratios, I discovered the worst issue of all:
Division on the required numeric range was broken! I suppose it has to do with 16-bit arithmetic somehow,
but ultimately I have no idea why; please enlighten me if you do! In the end, I just let the computer count
how often one integer fit into the other, like a schoolchild.
Thinking about how slow division could be on old machines like the 286, though,
my method is probably more efficient than one might think. ;)

.. code-block:: c

    for (i = 0; i < remaining_blocks; ) {
        ++chunk_count;
        i += CHUNK_SIZE;
    }

The scanf() function was garbage as well, but to be honest, I never really got the hang of that one anyway.
Here, though, not even the extremely basic examples from my old C book for DOS worked.
In the end, I resorted to plain UNIX read() to get user input:

.. code-block:: c

    printf("OK?\n");
    read(0, &confirm, 1);
    if (confirm != 'y') {
        exit(1);
    }

I would have loved to get the input from the same line, i.e. drop the ``\n`` from the printf() above,
but I did not find a way to flush the output buffer; no flush function to be seen anywhere in the docs!

At that point, I had run into so many obstacles already that I decided not to care if my confirmation looked pretty.
It was only there, after all, because I had noticed the division bug I mentioned earlier just floating by
when an earlier version of this program was already running.
I consequently decided to add a confirmation as a sanity check, in case anything else went haywire.

Now, we have arrived at the main loop, which is at the heart of the program:

.. code-block:: c

    blocks_written = 0;
    blocks_per_iteration = CHUNK_SIZE;

    filler = fopen(FILENAME, "w");
    for (i = 0; i < chunk_count; ++i) {
        if (remaining_blocks < CHUNK_SIZE) {
            blocks_per_iteration = remaining_blocks;
        }
        for (j = 0; j < blocks_per_iteration; ++j) {
            fwrite(zero_buffer, BLOCK_SIZE, 1, filler);
        }
        blocks_written += blocks_per_iteration;
        remaining_blocks -= blocks_per_iteration;
        printf("Wrote %u blocks, ", blocks_written);
        printf("%u remaining\n", remaining_blocks);
    }

As you can see, we are using a very basic algorithm.
You may have noticed that error handling on the fopen / fwrite / fclose / unlink system calls is missing.
I would leave that as an exercise for the enthusiastic reader.
Adding error handling should be easy if you look at
the respective function reference pages in the `UNIX System V manual`_. ;)

The ``if`` statement which caps ``blocks_per_iteration`` is necessary for the last chunk,
where there are fewer blocks remaining than one chunk size.
Luckily, my hand-crafted integer division seems to round up ``chunk_count`` in that case,
so no correction required there.

I was not sure how long each of these operations would take, so I added more debug output:

.. code-block:: c

    printf("Done, closing file.\n");
    fclose(filler);
    printf("Deleting file...\n");
    unlink(FILENAME);


Finally, we are done:

.. code-block:: c

    printf("Done, your hard drive should be clean now. :)\n");

Did it work?
------------

When I finally tried the program, it ran into a "no free space" error a lot earlier than ``df``
had previously indicated.
Apparently, the hint from the `Xenix System Administrator's guide`_ that Xenix needs at least 15 % (!)
of free space is a hard requirement in practice.
In the end, I had to kill the program using the Ctrl+\\ hot key.

Ironically, the data was still there when I ran 'strings' on a subsequently created hard drive image,
but again, I could not find my source code.
I have no idea how Xenix organizes its data storage, but it must be very efficient!
Well, except for all the available space that is unusable, but you know, something's always gotta give. :D

I ended up swallowing the ultimate bitter pill:
Using the ELKS floppy, I overwrote all data on the hard drive using classic dd, and subsequently reinstalled Xenix.
On a positive note, the installation was a lot easier the second time, and I got far more software to work than before.
And, naturally, I created a (clean) full disk backup immediately after I was done.

What comes next?
----------------

As that was no success at all, I should look towards other endeavours regarding Linux' grandpa.
A simple history function for the shell would be great, maybe even something like a complete command line processor.
Good, usable shells, like the Korn shell, are limited to Xenix 386, unfortunately, likely due to memory requirements.
The supplied C shell supports some rudimentary history in the form of reusable variables, but that is not really what I want.

Some very basic history in the modern sense, with support for the cursor keys, should not be too hard to do, right?
On the other hand, that is what I said about this project as well, so let's see ;)

Helpful resources
-----------------

These resources helped me a lot to write anything usable for Xenix.
I hope that they will be useful for you, too, should you want to try your luck on this ancient UNIX:

- `Xenix System Administrator's guide`_
- The original `UNIX System V manual`_

Beware: Both documents trigger a warning in current browsers because they are served via insecure HTTP! From what I can see, they should be safe to open, though.

- `Ancient C compilers repo`_, especially the C files from the first UNIX source code, for getting to know the quirky early C syntax
  and reading some example code on how to use the early versions of the UNIX system calls

.. _Xenix System Administrator's guide: http://www.nj7p.org/Manuals/PDFs/Intel/174389-001.pdf
.. _UNIX System V manual: http://bitsavers.trailing-edge.com/pdf/att/3b1/999-801-312IS_ATT_UNIX_PC_System_V_Users_Manual_Volume_1.pdf
.. _Ancient C compilers repo: https://github.com/mrquincle/ancient-c-compilers
