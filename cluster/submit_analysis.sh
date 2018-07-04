#!/usr/bin/env bash

# Stop execution after any error
set -e

# Submit job
sbatch run_analysis.sh
# Sleep for 1 second to avoid overloading the machine
sleep 1