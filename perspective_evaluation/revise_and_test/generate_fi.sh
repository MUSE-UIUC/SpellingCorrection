#!/bin/bash

number=1
while [ $number -lt 38 ]; do
    cp f1.py "f"$number.py
    number=$((number + 1))
done
