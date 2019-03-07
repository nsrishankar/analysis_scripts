#!/usr/bin/env bash
#SBATCH -J runanalysis
#SBATCH -N 1
#SBATCH -n 12
#SBATCH -p short
#SBATCH --mem 30G
#SBATCH --array=101-150%50
#SBATCH --output=slurm_messages/output/analysisout_%A_%a.out
#SBATCH --error=slurm_messages/error/analysisout_%A_%a.err

set -e

# Cleanup functions upon exit
function cleanup(){
	rm -rf $WORKDIR
}

# Directory setup
STARTDIR=$(pwd)
DATAOUTDIR="$STARTDIR/analysis_distributed/"
MYUSER=$(whoami)
LOCALDIR=/local
THISJOB="${SLURM_JOB_NAME}_${SLURM_ARRAY_TASK_ID}"
RAWDATADIR="$STARTDIR/data/*"
WORKDIR=$LOCALDIR/$MYUSER/$THISJOB


rm -rf "$WORKDIR" && mkdir -p "$WORKDIR" && cd "$WORKDIR"
trap cleanup EXIT SIGINT SIGTERM

folder_directory=() # Empty array
for f in $RAWDATADIR  # Append data folder names to the empty array
do
	folder_directory+=($f)
done

echo "Directory: "${folder_directory[$SLURM_ARRAY_TASK_ID]}
cp -a ${folder_directory[$SLURM_ARRAY_TASK_ID]} $WORKDIR
python3 $STARTDIR/analysis_file_test.py
echo "Completed"
cp -a $WORKDIR/*.pkl $DATAOUTDIR
rm -rfv $WORKDIR/${folder_directory[$SLURM_ARRAY_TASK_ID]}

# Copy data files to $DATAOUTDIR
#mkdir -p "$DATAOUTDIR"
#cp -a *.txt $DATAOUTDIR

# Remove working directory
rm -rf "$WORKDIR"
