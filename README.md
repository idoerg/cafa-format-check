
This repository contains two Python scripts for checking the format of 
prediction files for CAFA4

For more information on CAFA  see: http://biofunctionprediction.org
Specifically, for the CAFA rules see: https://www.biofunctionprediction.org/cafa-targets/CAFA4_rules%20_10_2019_v3.pdf

Running

*New* for any prediction file:
```bash
./cafa4_format_checker.py filename
```

Where "filename" is the path to the prediction file or zipped archive


This checks any type of prediction file.
CAFA4 format checker  will first check that the filename is correctly formatted.
Based on the filename structure, the program will run cafa_binding_site_format_checker, cafa_go_format_checker, 
cafa_do_format_checker, or cafa_hpo_format_checker.


Authored by Iddo Friedberg and Tim Bergquist. Distributed under GPLv3 license (attached)

Contact: idoerg@gmail.com

Contact: trberg@uw.edu

*Important*: If you are participating in CAFA4, you should subscribe to the afp-cafa
mailing list: https://mailman.iastate.edu/mailman/listinfo/afpcafa
