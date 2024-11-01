Smart Greenhouse System Setup Guide
Follow these steps to set up and run the Smart Greenhouse System.

Step 1: Install Python Virtual Environment Tool

First, install the python3-venv package to manage dependencies within a virtual
environment:

sudo apt-get install python3-venv

Step 2: Create Project Directory

Make a directory to store your project files:

mkdir ~/my_project
cd ~/my_project

Step 3: Set Up a Python Virtual Environment

Create and activate a virtual environment to manage project dependencies:

Create the virtual environment:

python3 -m venv venv
Activate the virtual environment:

source venv/bin/activate

We should now see (venv) before your command prompt, indicating the environment
is active.

Step 4: Install Required Libraries

Install the libraries needed for the Smart Greenhouse System, such as dht11:
pip install dht11

Step 5: Run the Code

Now, execute the main script to start the Smart Greenhouse System:
python SmartGreenHouseSystem_Group2.py