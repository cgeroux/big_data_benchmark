#!/bin/bash
#SBATCH --time=03:00:00
#SBATCH --account=def-cgeroux
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --mem=128GB
#SBATCH --job-name=create_500G_8stripes
#SBATCH --output=%x-%j.out
module load spark
spark-submit --executor-memory 2G ./create_text_spark.py --file-size=500000000000 -o /scratch/cgeroux/spark_input_8stripes/500G
