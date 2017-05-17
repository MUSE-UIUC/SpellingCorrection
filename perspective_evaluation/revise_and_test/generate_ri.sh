#!/bin/bash

number=1
while [ $number -lt 38 ]; do
    cp r1.py "r"$number.py
    number=$((number + 1))
done
