#!/bin/zsh

YEAR=2023
DAY=8

aoc -y $YEAR -d $DAY d -i input.txt --input-only --overwrite
aoc read -y $YEAR -d $DAY
