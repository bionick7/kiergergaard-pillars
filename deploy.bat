@echo off
7z a -tzip kiergergaard-pillars.lcp *.json
typst compile --font-path ./fonts main.typ outp.pdf