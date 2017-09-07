#!/bin/bash
#SBATCH --time=00:15:00
#SBATCH --account=def-cgeroux
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --mem=128GB
#SBATCH --job-name=create_10G_8stripes
#SBATCH --output=%x-%j.out
module load spark
spark-submit --executor-memory 2G ./create_text_spark.py --file-size=10000000000 -o /scratch/cgeroux/spark_input_8stripes/10G
