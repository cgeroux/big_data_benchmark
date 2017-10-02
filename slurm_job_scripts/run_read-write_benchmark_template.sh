#!/bin/bash
#SBATCH --time=<job-time>#minutes
#SBATCH --account=def-cgeroux
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --mem=128000MB
#SBATCH --job-name=spark_IO_<spark-partitions.name>_<lustre-stripes.name>_<data-size.name>
#SBATCH --output=%x-%j.out
module load spark
source ./paths.sh
TMP_PATH=$SPARK_BM_TMP_PATH/spark_input_<spark-partitions.name>_<lustre-stripes.name>
spark-submit --executor-memory 2G $SPARK_BM_ROOT_PATH/spark/linecount/linecount.py --num-partitions=<spark-partitions.text> $TMP_PATH/<data-size.name> $TMP_PATH/<data-size.name>_tmp_$SLURM_JOB_ID
