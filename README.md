
### CAFA4 Format Checker

This repository contains Python scripts for checking the format of 
prediction files for CAFA4

For more information on CAFA  see: http://biofunctionprediction.org
Specifically, for the CAFA rules see: https://www.biofunctionprediction.org/cafa-targets/CAFA4_rules%20_01_2020_v4.pdf

Running

*New* for any prediction file:
```bash
./cafa4_format_checker.py filename
```

Where "filename" is the path to the prediction file or zipped archive


This checks any type of prediction file.
CAFA4 format checker  will first check that the filename is correctly formatted.
Based on the filename structure, the program will run cafa_go_format_checker, 
cafa_do_format_checker, or cafa_hpo_format_checker.


Authored by Iddo Friedberg, Tim Bergquist and Scott Zarecor. Distributed under GPLv3 license (attached)

Contact: idoerg@gmail.com

Contact: trberg@uw.edu

Contact: szarecor@iastate.edu

*Important*: If you are participating in CAFA4, you should subscribe to the afp-cafa
mailing list: https://mailman.iastate.edu/mailman/listinfo/afpcafa
