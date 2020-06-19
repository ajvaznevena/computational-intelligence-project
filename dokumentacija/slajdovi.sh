#! /bin/bash
pandoc -V theme:metropolis -V classoption=dvipsnames -V lang=en prezentacija.md -t beamer -o prezentacija.pdf --columns=50

