# Import libraries and configuration file
import os
import subprocess
import time
import config_dcm2bids_batch as cfg


# Main function
def main():
    """
    Run the things.
    """
    folders_tocheck = cfg.path_bidsdata, cfg.logdir
    check_dirs(folders_tocheck)
    logfile_fullpaths = cfg.errorlog, cfg.outputlog
    create_logfiles(logfile_fullpaths)
    check_dicomdir(cfg.path_dicoms)
    batch_jobs(cfg.subjectlist, cfg.path_dicoms, cfg.path_config, cfg.path_bidsdata)


def batch_jobs(subject_list, path_dicoms, path_config, path_bidsdata):
    with open(subject_list) as file:
        lines = file.readlines()
    for line in lines:
        entry = line.strip()
        subjectdir = entry.split(",")[0]
        subject = entry.split(",")[1]
        subjectpath = os.path.join(path_dicoms, subjectdir)
        if os.path.isdir(subjectpath):
            time.sleep(10)
            write_to_outputlog(subjectdir + os.linesep)
            if cfg.multiple_sessions:
                wave = entry.split(",")[2]
                if cfg.run_local:
                    batch_cmd = 'dcm2bids -d {subjectpath} -s {wave} -p {subject} -c {path_config} -o {path_bidsdata}  --forceDcm2niix --clobber'.format(
                        subjectpath=subjectpath, wave=wave, subject=subject, path_config=path_config,
                        path_bidsdata=path_bidsdata)
                else:
                    batch_cmd = 'module load singularity; qsub -b y -M $USER@mail -l h_rt=3:00:00,h_data=8G -pe shared 2 -o {logdir}/{subjectdir}_output.txt -j y /u/local/apps/singularity/3.8.5/bin/singularity exec -B {path_dicoms} -B {path_bidsdata} -B {path_conversionfolder} {singularity_image} dcm2bids -d {subjectpath} -s {wave} -p {subject} -c {path_config} -o {path_bidsdata}  --forceDcm2niix --clobber'.format(
                        logdir=cfg.logdir, subjectdir=subjectdir, path_dicoms=cfg.path_dicoms,
                        wave=wave, path_conversionfolder=cfg.path_conversionfolder, path_config=cfg.path_config,
                        subject=subject, path_bidsdata=cfg.path_bidsdata, subjectpath=subjectpath,
                        singularity_image=cfg.singularity_image, account=cfg.group)
            else:
                if cfg.run_local:
                    batch_cmd = 'dcm2bids -d {subjectpath} -p {subject} -c {path_config} -o {path_bidsdata}  --forceDcm2niix --clobber'.format(
                        subjectpath=subjectpath, subject=subject, path_config=path_config,
                        path_bidsdata=path_bidsdata)
                else:
                    batch_cmd = 'module load singularity; qsub -b y -M $USER@mail -l h_rt=1:00:00,h_data=1G -pe shared 2 -o {logdir}/{subjectdir}_output.txt -j y /u/local/apps/singularity/3.8.5/bin/singularity exec -B {path_dicoms} -B {path_bidsdata} -B {path_conversionfolder} {singularity_image} dcm2bids -d {subjectpath} -p {subject} -c {path_config} -o {path_bidsdata}  --forceDcm2niix --clobber'.format(
                        logdir=cfg.logdir, subjectdir=subjectdir, path_dicoms=cfg.path_dicoms,
                        path_conversionfolder=cfg.path_conversionfolder, path_config=cfg.path_config,
                        subject=subject, path_bidsdata=cfg.path_bidsdata, subjectpath=subjectpath,
                        singularity_image=cfg.singularity_image, account=cfg.group)
            subprocess.call([batch_cmd], shell=True)
        else:
            write_to_errorlog(subjectdir + os.linesep)


def check_dicomdir(path_dicoms):
    if not os.path.isdir(path_dicoms):
        write_to_errorlog("Incorrect dicom directory specified")


def touch(path: str):
    """
    Create a new file
    
    @type path:     string
    @param path:    path to - including name of - file to be created
    """
    with open(path, 'a'):
        os.utime(path, None)


def check_dirs(dir_fullpaths: list):
    """
    Check if a directory exists. If not, create it.

    @type dir_fullpaths:        list
    @param dir_fullpaths:       Paths to directorys to check
    """
    for dir_fullpath in dir_fullpaths:
        if not os.path.isdir(dir_fullpath):
            os.mkdir(dir_fullpath)


def create_logfiles(logfile_fullpaths: list):
    """
    Check if a logfile exists. If not, make one.

    @type logfile_fullpaths:         list
    @param logfile_fullpaths:        Paths to logfiles to check
    """
    for logfile_fullpath in logfile_fullpaths:
        if not os.path.isfile(logfile_fullpath):
            touch(logfile_fullpath)


def write_to_outputlog(message):
    """
    Write a log message to the output log. Also print it to the terminal.

    @type message:          string
    @param message:         Message to be printed to the log
    """
    with open(cfg.outputlog, 'a') as logfile:
        logfile.write(message + os.linesep)
    print(message)


def write_to_errorlog(message):
    """
    Write a log message to the error log. Also print it to the terminal.

    @type message:          string
    @param message:         Message to be printed to the log
    """
    with open(cfg.errorlog, 'a') as logfile:
        logfile.write(message + os.linesep)
    print(message)


main()
