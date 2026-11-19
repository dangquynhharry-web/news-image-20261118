# The World — 18 November 2026

A program that draws a newspaper front page summing up the world's news
of Wednesday 18 November 2026, and writes it to `/output/entry.png`.

Entry for the make.fun bounty
[news-image-20261118](https://make.fun/bounty/news-image-20261118)
("Sum up 18 November's world news in one image").

## Run

```sh
python3 main.py   # writes /output/entry.png (1024x1024 PNG, ~116 KB)
```

Python 3.13, Pillow. No network, no clock, no randomness: every run
writes byte-identical output. The three DejaVu fonts the page uses are
bundled in `fonts/` (Bitstream Vera license) so the program renders the
same wherever it runs.

## The six stories

1. **Xi and Putin meet in Shenzhen** — talks a day before the first-ever
   three-way summit with Trump; APEC opens with trade and sanctions on
   the agenda.
2. **U.S. strikes Iran site; Iran hits back** — Iran fires drones at U.S.
   bases in Kuwait and Bahrain after U.S. jets hit a missile site on
   Qeshm Island.
3. **Democrats take Senate 56–44** — Peltola wins Alaska, the ninth
   Democratic flip of the midterms.
4. **U.S. loses measles-free status** — after 26 years; 5,412 cases in
   2026, the most since 1991.
5. **Nvidia posts record $115.8B quarter** — revenue doubles in a year;
   first earnings since Huang's exit.
6. **Voyager 1 reaches one light-day** — 16 billion miles from Earth, a
   distance no human-made object has crossed before.

Headlines as reported on 18 November 2026 (AP, Reuters, BBC, PAHO/CDC,
Nvidia, NASA JPL, via the day's news briefs).
