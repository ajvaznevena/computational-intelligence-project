#! /bin/bash
# lang=sr 	-> Prevodi dokument na srpski jezik
# -V --toc 	-> Generise sadrzaj
pandoc dokumentacija.md -V lang=sr --filter pandoc-citeproc --bibliography=literatura.bib --metadata link-citations=true -o dokumentacija.pdf --toc
