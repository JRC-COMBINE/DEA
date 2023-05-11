#!/bin/bash

#SBATCH --job-name=DEA_$jobname
#SBATCH --output=$root/logs/${jobname}_%A_%a.out
#SBATCH --error=$root/logs/${jobname}_%A_%a.err
#SBATCH --time=$time
#SBATCH --mem=$mem
#SBATCH --cpus-per-task=$mcpu
#SBATCH --account=$account
#SBATCH --array=$array

cd $root
echo LOADING PYTHON ENVIRONTMENT
$loadpythonenv

echo EXECUTING FUNCTION $func
python -c "import joblib; e = joblib.load('$eroot/$$SLURM_ARRAY_TASK_ID/encounter.pkl'); e.$func(); e.save()"