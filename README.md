# Project_ARC

## This github contains the following branches (1 for each visualisation method):

#### 1. DataPreprocessing_ViolinPlots_Excel 
This branch contains the script which processes TCGA datasets and exstracts the relevant data to a .JSON file. This file is usable in the other branches as input data. 
The other scripts are for creating Violin plots and Excel sheets based on the previously made .JSON file. 
#### 2. Ribosome_visualizer
This branch contains a web application which generates an interactive web page, in which gene expression is visualized on a color scale onto ribosome images (.SVG) <br>
*A second script is available on another branch to create a grid of ribosome images of every patient. This script is not implemented into the web tool, but has to be run as a separate instance after running the app.py in the Ribosome_visualizer branch.*
#### 3. String_Network

