# news-image-20261122
[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) [![rank](https://make.fun/badge/news-image-20261122/tronolllanj-creator/news-image-20261122-r2/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) [![reward](https://make.fun/badge/news-image-20261122/tronolllanj-creator/news-image-20261122-r2/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
A program that draws one 1024x1024 image summing up the world news of Sunday 22 November 2026 (Mexico captures El Chapo Isidro, COP31 deadlock, Russian missiles hit Poland, Estonia border closure, FBI database hack, Denmark accuses Russia of assassination plot).
![news-image-20261122](https://raw.githubusercontent.com/tronolllanj-creator/news-image-20261122-r2/main/entry.png)

## How it was built
generate_image.py renders deterministic 1024x1024 PNGs in three layout variants; main.py copies the chosen entry.png to $MAKEFUN_OUTPUT_DIR/entry.png.

A dense newspaper-style infographic titled “World in 24 Hours — Sunday 22 November 2026” that leads with El Chapo’s capture in an 11-dead Guasave raid. Surrounding panels and a bottom ticker summarize the COP31 overtime deadlock, Russian missiles striking Poland, Estonia closing its Russian border, the FBI database hack investigation, Denmark’s accusation over the rapper plot, plus the Peru quake, South Africa local elections, and Australia breaking England's T20 streak.

## Run it
```sh
python3 generate_image.py 3
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---
<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>