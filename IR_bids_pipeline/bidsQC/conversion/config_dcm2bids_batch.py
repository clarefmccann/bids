import os
from datetime import datetime

######################## CONFIGURABLE PART BELOW ########################

# Set your Hoffman user group
group = "silvers"
singularity_image = "dcm2bids_2022-09-29.sif" # ignored if running locally; dcm2bids singularity image name
config_file = "study_config.json"

# Set directories
# These variables are used in the main script and must be defined here.
# They need to exist prior to running the script

path_toplevel = os.path.join(os.sep, "u", "project", "silvers", "data", "bids", "IR_bids_pipeline") # folder that contains path_bidsdata and path_conversionfolder
path_dicoms = os.path.join(os.sep, "u", "project", "silvers", "data", "IR", "dicom", "restructured")
path_conversionfolder = os.path.join(path_toplevel, "bidsQC", "conversion")  # Contains subject_list.txt, config file, and dcm2bids_batch.py
path_config = os.path.join(path_conversionfolder, config_file)  # Don't change this one
singularity_image = os.path.join(os.sep, "u", "project", "silvers", "data", "scripts", "containers", singularity_image) # Set equal to "NA" if you are running the script locally

# These variables are also used in the main script and need to be defined here.
# If the directories don't exist, they will be created by the script

path_bidsdata = os.path.join(os.sep, "u", "project", "silvers", "data", "bids", "IR_bids_pipeline", "bids_data") # Where the niftis will be put
logdir = os.path.join(path_bidsdata, "logs_dcm2bids")
outputlog = os.path.join(logdir, "output_dcm2bids" + datetime.now().strftime("%Y%m%d-%H%M") + ".txt")
errorlog = os.path.join(logdir, "errors_dcm2bids" + datetime.now().strftime("%Y%m%d-%H%M") + ".txt")

# Source the subject list (needs to be in your current working directory)
subjectlist = "test_subject_list.txt"

# Run on local machine (run_local = True) or high performance cluster with slurm (run_local = False)
run_local = False

# If subject data are collected across multiple sessions, set to True. If single session, set to False.
# https://bids-specification.readthedocs.io/en/v1.1.2/05-longitudinal-and-multi-site-studies.html
multiple_sessions = False
