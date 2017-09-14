#!/bin/bash
#SBATCH --time=<job-time>#minutes
#SBATCH --account=def-cgeroux
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --mem=128000M
#SBATCH --job-name=create_data_<spark-partitions.name>_<lustre-stripes.name>_<data-size.name>
#SBATCH --output=%x-%j.out
module load spark
SPARK_BM_ROOT_PATH=/home/cgeroux/test_spark/big_data_benchmark
SPARK_BM_TMP_PATH=/scratch/cgeroux/spark_input_<spark-partitions.name>_<lustre-stripes.name>
mkdir -p $SPARK_BM_TMP_PATH
lfs setstripe -c <lustre-stripes.text> $SPARK_BM_TMP_PATH
spark-submit --executor-memory 2G $SPARK_BM_ROOT_PATH/input_files/create_text_spark.py --num-partitions=<spark-partitions.text> --file-size=<data-size.text> -o $SPARK_BM_TMP_PATH/<data-size.name>
