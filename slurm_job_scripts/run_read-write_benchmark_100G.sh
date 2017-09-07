#!/bin/bash
#SBATCH --time=01:00:00
#SBATCH --account=def-cgeroux
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --mem=128GB
#SBATCH --job-name=spark_IO_100G
#SBATCH --output=%x-%j.out
module load spark
echo $SBATCH_JOBID
spark-submit --executor-memory 2G ./linecount.py /scratch/cgeroux/spark_input/100G
