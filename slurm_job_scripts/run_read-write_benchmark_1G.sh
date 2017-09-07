#!/bin/bash
#SBATCH --time=00:10:00
#SBATCH --account=def-cgeroux
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --mem=128GB
#SBATCH --job-name=spark_IO_1G
#SBATCH --output=%x-%j.out
module load spark
spark-submit --executor-memory 2G ./linecount.py /scratch/cgeroux/spark_input/1G
