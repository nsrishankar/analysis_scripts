#!/usr/bin/env bash
#SBATCH -J runanalysis
#SBATCH -n 5
#SBATCH -p short
#SBATCH --mem 25G
set -e

# Directory setup
STARTDIR=$(pwd)
DATADIR="$STARTDIR/analysis_out/"
MYUSER=$(whoami)
LOCALDIR=/tmp
THISJOB="analysis_${SLURM_JOB_NAME}"
RAWDATDIR="$STARTDIR/data/*"
WORKDIR=$LOCALDIR/$MYUSER/$THISJOB
#echo $STARTDIR

rm -rf "$WORKDIR" && mkdir -p "$WORKDIR" && cd "$WORKDIR"

for f in $RAWDATDIR
do
    # echo $f
    cp -a $f $WORKDIR    
     # Call to execute program with parameters
    python3 $STARTDIR/convergence_file_test.py
    rm -rf *.dat
done

# Copy data files to $DATADIR
mkdir -p "$DATADIR"
cp -a *.txt $DATADIR

# Remove working directory
rm -rf "$WORKDIR"






















