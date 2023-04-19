# Readme -- AI Scaling Attack

## About
This document describes the steps to set up the python environment.

## Note about Mac M1s
Due to compatibility issues, Anaconda and Python 3.6 do not work properly with M1 chips. Thus, this script cannot run on Macs with M1 chips. I reccommend running this on an x86 architecture. This has been tested on a Windows 10 machine.

## System Requirements
- Python 3.6
- Conda / (Virtualenv)

- We've tested everything on different UNIX systems. If you set up a virtual machine,
we recommend using the latest Ubuntu OS.


## Set up environment
In this section, we will describe everything to set up a Python project
with all the necessary requirements/dependencies. If you are already familiar
with creating and using Python projects, this section will not be so interesting.
That said, let's examine the different steps that are necessary:

1. Install *Anaconda*
  - This step will create an own Python environment so that we do not mess up with the
  system.
  - Go to the [Anaconda website](https://www.anaconda.com/distribution/#download-section)
  and download/install the latest Python 3 version. At the time of writing,
  it was the Python 3.7 version and Anaconda 2019.10.
  - If you want to use *virtualenv*, because you are already familiar with that,
  you can also try it. With virtualenv, we had some problems to get the requested
  version from the requirements.txt. But in principle, virtualenv should also work if
  you can get the correct python packages.


2. Setup Anaconda
  - Open a terminal.
  - Create a new environment, we *need Python 3.6*
  - Use: ```conda create --name scaling-attack python=3.6```
    - The name is arbitrary, but makes sense for our project.
  - Activate the environment via ```source activate scaling-attack``` (if this does not
    work, try ```conda activate scaling-attack```)


3. Project Requirements

  - Go to the project directory *scaleatt*. You will find a *requirements.txt* there.
  - Use ```pip install -r requirements.txt``` to install all requirements.
  - If you get the following error: libSM.so.6 is missing.
      - Use opencv-python-headless package instead of opencv-python, without
      libSM6 dependency.
      - Either replace ```opencv-python``` in the requirements.txt by ```opencv-python-headless==4.1.0.25```
      - or if all other packages are already installed, install opencv via ```pip install opencv-python-headless==4.1.0.25```


4. Cython compilation
  - We've implemented some defenses with Cython.
  - Installation
    - Make sure you are in the *scaleatt* directory. Just run ```python setup.py build_ext --inplace```
    - This will compile the defenses, you might get a warning that the numpy version
    is deprecated (which can happen due to cython).
  - Problems
    - If you have problems with the compilation step, each defense has a pure python
    version for each cython code, which you can easily use by setting ```usecythonifavailable=False```
    at the respective code locations where we define a defense object!
    - You will need to remove the cython import in the respective defenses.
  - Another note: Our timing benchmark experiments were done with a pure C++ version
  in the benchmark directory without any python/cython overhead. Their implementation
  is more optimized. So please do not use the python/cython version of our defenses
  to repeat the benchmark experiments.


5. Setup Python project
  - Now we need to start the python project. You can do that with any IDE you want.
  - The following description is based on Pycharm.
    - After installing and opening Pycharm, create a new project
      - with the directory *scaleatt* as *Location*. It will be our content root.
      - and our conda environment *scaling-attack* as python interpreter.
        - Please use *existing interpreter* and activate the *scaling-attack*
        environment that we've created in step 2.


## Troubleshooting
1. Depending on your system, it might be necessary to install the package ```python3-tk```.
2. If you get the error *libSM.so.6 is missing*, see step 3 to solve it.
3. Python paths:
  - If you do not use an IDE or Pycharm, you might need to set the PYTHONPATH
  yourself once, such as: ```export PYTHONPATH=/home/<path_to_extracted_dir>/scaleatt/:$PYTHONPATH```.
  - Alternatively, go to the scaleatt directory in a terminal,
  and start any python script by using the following command: ```PYTHONPATH=/home/<path_to_extracted_dir>/scaleatt python path/to/python-file/file.py```

# Create Image
`create_image.py` is a script based off the Juptyer Notebook found in `tutorial/jupyter_intro.ipynb`.

This script will allow you to create malicious scaling attack images.

## Command Line Arguments
The script uses command line arguments to take in user input.
### -h --help
Lists all arguments and describes each one of them in detail.
### -s --source
The path to the image you would like to use as the normal image.  (**Required Argument**)
### -t --target
The path to the image you would to use that will be mapped onto the source image. (**Required Argument**)
### -l --library
The library you would like to use in order to map the target image onto the source image.

To specify the library you can write the full name of the library or the letter as shown below.

Three library are available:
1. OpenCV (C)
2. Pillow (P)
3. TensorFlow (T)

Please note that the Pillow library is protected against scaling attacks except for using the Nearest algorithm.
Meaning an image will only be generated for Pillow using the Nearest algorithm.

By default the script uses TensorFlow.

### -a --algorithm
The algorithn you would like to use in order to generate the image.


There are 5 different algorithms available:
1. Nearest (N)
2. Bicubic (BC)
3. Bilinear (BL)
4. Lanczos (L)
5. Area (A)

The 5th algorithm Area is protected against scaling attacks thus, an image will not be created.

By default the script uses Nearest.
### -o --output
The name of the output file you would like the malicious image to be saved as. By default, it is saved as `output.png` 
### -c --scaling
The percentage of resolution you would like to use when the target image appears in the output file. The default is 20% (Value must be between 0 and 100). The higher the resolution of the target image the less of the original source image will appear in the output.

When the script has finished, a resulting attack image will be generated with the name `output.png` or a customized name if specified.