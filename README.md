# Preprocessing, violin plots and excel sheets

## About

These scripts work together to normalize and save ribosomal count data from TCGA. After this, violin plots and excel sheets of the data are created.


## Getting Started

Instructions to get started with normalizing TCGA count data and creating violin plots/excel sheets

### Prerequisites

Installation requirements

1. Python 3.8+
2. Packages from 'requirements.txt'. Can be installed using with the following command using the Python commandline.
```
pip install -r requirements.txt
```
3. Dataset containing count data + samplesheet downloaded from the GDC Data Portal (https://portal.gdc.cancer.gov/). The samplesheet should contain 1 tumor and 1 normal entry from every case.

### How to run

1. Make a directory like seen in 'Sample_sheet' in the folder 'Data'. This has the following structure:
.  
├── Data  
│   ├── < Sample name >  
│   │    ├── Input  
│   │    └── Ouput  
│   │    └── cases_extracted  

2. Place the downloaded .tar.gz and sample sheet in the 'Input' directory. Make sure nothing else is in this folder, and the 'cases_extracted' folder is also empty.

3. Make sure the 'all_rp_genes.csv' file is in the 'Data' folder.

3. Run 'analysis.py' to preprocess the dataset and generate violin plots + excel sheets. These will be saved in the 'output' directory.

## Author

* **Lars Maas**
