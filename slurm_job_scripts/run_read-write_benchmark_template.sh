#!/bin/bash
#SBATCH --time=<job-time>#minutes
#SBATCH --account=def-cgeroux
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --mem=128GB
#SBATCH --job-name=spark_IO_<spark-partitions.name>_<lustre-stripes.name>_<data-size.name>
#SBATCH --output=%x-%j.out
module load spark
SPARK_BM_ROOT_PATH=/home/cgeroux/test_spark/big_data_benchmark
SPARK_BM_TMP_PATH=/scratch/cgeroux/spark_input_<spark-partitions.name>_<lustre-stripes.name>
spark-submit --executor-memory 2G $SPARK_BM_ROOT_PATH/spark/linecount/linecount.py --num-partitions=<spark-partitions.text> $SPARK_BM_TMP_PATH/<data-size.name> $SPARK_BM_TMP_PATH/<data-size.name>_tmp_$SLURM_JOB_ID
