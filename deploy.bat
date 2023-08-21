@echo off
typst compile --font-path ./fonts lcp2pdf.typ Manual.pdf
cd content
7z a -tzip ../kiergergaard-pillars.lcp *.json
pause