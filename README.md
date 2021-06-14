# STRING Network

## About

The STRING Network is a visualization webtool that creates protein-protein interaction networks for both "solid tissue normal" and "primary tumor". The webtool has only been tested on lung cancer data retrieved from the GDC Data Portal.


## Getting Started

Instructions to get started using the STRING Network

### Prerequisites

Installation requirements

1. Dataset downloaded from the GDC Data Portal (https://portal.gdc.cancer.gov/)

### How to run

Step 1. Create a virtualenv for python and install packages:

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Step 2. Place the downloaded .tar.gz dataset in the main directory.

Step 3. Run ``main.py`` to preprocess the dataset to be used by the STRING Network.

```
python main.py
```

Step 4. Run ``Stringdb.html`` to visualize the STRING Network.

## Author

* **Julian Lerrick** - *Initial work* - [JulSL](https://github.com/JulSL)

