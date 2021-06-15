# Project_ARC

# Addition to ribosome_visualizer branch

## About

The Grid-Bot is a tool that works in conjunction with the Ribosome Visualizer. It makes grids of all the 16 available visualisations.
It also saves the images individually, to allow for different styles of analisys.

## Getting Started

Instructions to get started with creating image grids of the ribosome visualizer. <br>
To run this script correctly please make sure that you are able to run the scripts in ribosome_visualizer. 

### Prerequisites

Installation requirements

1. Python 3+
2. Ribosome Visualizer (Working)

### How to run

Step 1. Create a virtualenv for python and install packages:

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Step 2. Download and install the chromedriver: https://chromedriver.chromium.org/downloads

Step 3. Change the directory at line 29 to the installation location of the chromdriver.exe

Step 4. Start the Ribosome Visualizer Webapp in another instance of your IDE

Step 5. Start the Bot.py script

Step 6. A window will now pop up, this is the chromedriver. Fullscreen this window.

Step 7. It will now automatically open each case and make a screenshot. It is important to leave the computer running **without doing anything else**.

Step 8. The script will run a few minutes, according to the size of the dataset. It takes about 3 seconds per case, to allow for loading.

Step 9. When the Bot.py script is done, you can start the Cropper.py script. <br>
        **To make sure earlier instances of this script don't contaminate the new ones, all images are deleted. Make sure you save everything you want to keep to another location**

Step 10. The script will now make the different images and generates a grid. <br>
         The scripts can be found at venv//Scripts//Dataset//Grids
         
## Author

* **Bram Löbker** - *Coding work* - [bramlobker](https://github.com/bramlobker)
* **Harm Laurense** - *Coding work* - [yumsi](https://github.com/yumsi)
