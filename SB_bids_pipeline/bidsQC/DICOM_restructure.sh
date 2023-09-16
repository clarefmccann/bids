#!/bin/bash

# Set subject list 

declare -a SUBJLIST=("SB004")

for SUBJ in "${SUBJLIST[@]}"
do
	cd /u/project/silvers/data/SB/dicom/T4/${SUBJ}/PRISMA_FIT_MRC35343/20*
	cp -r SILVERSGROUP_SBCONT_1 /u/project/silvers/data/SB/dicom/restructured/${SUBJ}_T4
        #cd /u/project/silvers/data/SB/dicom/restructured/${SUBJ}_T4
        #find -type f | while read; do mv "$REPLY" "$(dirname $REPLY)/.."; done
	#rm -rf RFMRI* TFMRI* DMRI* AAHS* CAL* SOUND* T1W* MOCO* 
done
