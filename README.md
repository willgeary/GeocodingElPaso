### Setup

Clone this repository:

`git clone https://github.com/willgeary/GeocodingElPaso`

Change into the main directory:

`cd GeocodingElPaso`

### Create virtual environment

Note, this requires the [anaconda](https://www.anaconda.com/download/#macos) distribution of python.

Create a new environment called geocode:

`conda create --name geocode python=3`

Activate the new environment on Windows:

`activate geocode`

Activate the new environment on macOS and Linux:

`source activate geocode`

### Install dependencies

There are three dependencies that you need to install:

`conda install -c conda-forge geopandas`

`pip install requests`

`pip install tqdm`

### Run the script

Now, you are ready to run the script. Note that this may take 5-6 hours for ~30k addresses.

Run the script with:

`python run.py --input=help_recode_addresses.csv`

When the script is complete the results will be saved as `output.csv`
