# Recettear Repacker

A set of scripts to unpack and repack Recettear game files

## How it works

Recettear stores most of its data in `bin/dataxxx.bin`.  
These files contain almost all assets, inidividually compressed with LZSS.  
`lnkdatas.bin` (or `lnkdata.bin` for the Japanese version) contains info about  
which assets can be found in which file and their offset.

All the `dataxxx.bin` files combined contain about 1200 files (120MB, 435MB uncompressed).  
For every update that touches one of these files, all of them would need to be recompressed.  
All 120MB would need to be redistributed, even if only a tiny part of it is changed.

For this reason, Recettear has a similar file called `bmpdata.bin`.  
This file contains assets too, and the game will look here first before  
looking in `lnkdatas.bin`. This allows the developers to push small updates  
without having to touch `lnkdatas.bin`. They simply drop the updated version in  
`bmpdata.bin`. Unlike `lnkdatas.bin`, `bmpdata.bin` contains both the data and the metadata.  
`bmpdata.bin` is compressed with LZW.

## Getting started

### Prerequisites

The scripts require Python 3 to be installed.

### Usage

In this section I will show you how to make changes to the game files.  
I recommend dropping the scripts in the games root folder for ease of use, but this is not required.

#### Unpacking `lnkdatas.bin`

First, unpack the `dataxxx.bin` files with the `lnk_unpack.py` script.  
It requires 2 arguments: the path to the game root, and the folder to unpack to.

```bash
python lnk_unpack.py . lnk-unpacked/
```

#### Unpacking `bmpdata.bin`

Next, unpack `bmpdata.bin` with `bmp_unpack.py`.  
It requires 2 arguments: the path to `bmpdata.bin`, and the folder to unpack to.

```bash
python bmp_unpack.py bmpdata.bin bmp-unpacked/
```

#### Repacking `bmpdata.bin`

You can then browse the files and choose which ones you want to change.  
Drop the changed versions in the folder you unpacked `bmpdata.bin` to (`bmp-unpacked` here).

Then, repack `bmpdata.bin`. Please make sure to make a backup of the original first.  
`bmp_pack` requires 2 arguments: the folder to pack and the path to the output file.

```bash
# THIS WILL OVERWRITE bmpdata.bin!
# CREATE A BACKUP!

python bmp_pack.py bmp-unpacked/ bmpdata.bin
```

That's it! Boot up the game and you will see your changes.


#### Identifying files

If you lose track of which file is the original, run the following.  
It will identify the file for you.

```bash
python crc.py FILE
```


## Notes about the game files

All text files are encoded with Shift-JIS, not ASCII. Make sure your editor is configured properly.  
Lastly, here is an overview of the packed game files.

```
dataxxx.bin
├── bmp/                  All images
│   ├── chr/              Character spritesheets
│   ├── en/               Enemy icons
│   ├── item/             Item spritesheets
│   ├── ivent/            Cutscene/event images
│   ├── nami/             Fog textures
│   ├── title/            Boss titles
│   └── umi/              Water textures
├── data/                 Misc game data
│   ├── buysell.txt       ??? Customer dialogue settings
│   ├── chara.txt      
   Adventurer stats
│   ├── config.txt         Font settings
│   ├── enemylist.txt     Dungeon enemy settings
│   ├── enemy.txt         Dungeon enemy stats
│   ├── event.txt         Event flags and conditions
│   ├── gousei.txt        Fusion recipes
│   ├── item.txt          Item list
│   ├── kyaku.txt         Customer settings
│   ├── model.txt         ??? 3D model metadata
│   ├── news.txt          News
│   ├── oder.txt          Orders
│   ├── snews.txt         Dungeon news
│   ├── tuto1.txt         Selling tutorial
│   ├── tuto2.txt         Buying tutorial
│   └── tuto3.txt         Suggestion selling tutorial
├── ef/                   ??? Effect animation data
├── idx/                  ??? Maybe spritesheet or animation info
│   ├── stageidx.txt/     Dungeon data
│   ...
├── iv/                   Event scripts
├── kyaku/                Shop customer data
├── xfile/                 3D model textures
├── xfile2/                Boss 3D model textures
├── fontdata.bin          Bitmap font
└── fontidx.bin           ???
```
