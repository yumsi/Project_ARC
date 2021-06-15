# STRING Network

## About

The STRING Network is a visualization webtool that creates protein-protein interaction networks for both "solid tissue normal" and "primary tumor". The webtool has only been tested on lung cancer data retrieved from the GDC Data Portal.


## Getting Started

Instructions to get started using the STRING Network

### Prerequisites

Installation requirements

1. Python 3+
2. Dataset containing count data + samplesheet downloaded from the GDC Data Portal (https://portal.gdc.cancer.gov/). The samplesheet should contain 1 tumor and 1 normal entry from every case.


### How to run

Step 1. Create a virtualenv for python and install packages:

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Step 2. Place the downloaded .tar.gz dataset in the 'main' directory. Place the downloaded samplesheet in the 'data' folder. Place your gene names in the 'gene selection' folder.
```

├── Main folder
│ ├── Data
│ │ ├── Cases
│ │ └── Gene selection <--- Add your gene name list here as "eiwitten.txt"
│ │ └── output
│ │  <--- Add your sample sheet here.
│   <--- Add your downloaded TCGA dataset here.
```

Step 3. Run ``main.py`` to preprocess the dataset to be used by the STRING Network.

```
python main.py
```

Step 4. Run ``Stringdb.html`` to visualize the STRING Network.

## Author

* **Julian Lerrick** - *Initial work* - [JulSL](https://github.com/JulSL)

