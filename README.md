
This repository contains two Python scripts for checking the format of 
prediction files for CAFA2 and CAFA3

For more information on CAFA  see: http://biofunctionprediction.org
Specifically, for the CAFA rules see: http://biofunctionprediction.org/node/8

Running

*New* for any prediction file:
```bash
./cafa_format_checker.py filename
```
This checks any type of prediction file.

For GO based predictions:
```bash
./cafa_go_format_checker.py filename
```

For Human Phenotype Ontology based predictions (HPO)
```bash
./cafa_hpo_format_checker.py filename
```
Where "filename" is the path to the prediction file

Authored by Iddo Friedberg. Distributed under GPLv3 license (attached)

Contact: idoerg@gmail.com

*Important*: If you are participating in CAFA, you should subscribe to the afp-cafa
mailing list: https://mailman.iastate.edu/mailman/listinfo/afpcafa
