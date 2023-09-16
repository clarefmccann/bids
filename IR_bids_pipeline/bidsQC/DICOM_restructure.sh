#!/bin/bash

# Set subject list 

declare -a SUBJLIST=("IRA058")

for SUBJ in "${SUBJLIST[@]}"
do
	cd /u/project/silvers/data/IR/dicom/${SUBJ}/Prisma_fit_MRC35426/20*/
	cp -r Silvers^* /u/project/silvers/data/IR/dicom/restructured/${SUBJ}
        #cd /u/project/silvers/data/SB/dicom/restructured/${SUBJ}_T4
        #find -type f | while read; do mv "$REPLY" "$(dirname $REPLY)/.."; done
	#rm -rf RFMRI* TFMRI* DMRI* AAHS* CAL* SOUND* T1W* MOCO* 
done
