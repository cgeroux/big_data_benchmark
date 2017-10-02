#!/bin/bash
#SBATCH --time=<job-time>#minutes
##SBATCH --account=def-cgeroux

#SBATCH --account=cc-debug_gpu
#SBATCH --reservation=cc-debug_gpu_6
#SBATCH --gres=gpu:0

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=2000M
#SBATCH --job-name=create_data_<spark-partitions.name>_<lustre-stripes.name>_<data-size.name>
#SBATCH --output=%x-%j.out
module load spark
source ./paths.sh
TMP_PATH=$SPARK_BM_TMP_PATH/spark_input_<spark-partitions.name>_<lustre-stripes.name>
mkdir -p $TMP_PATH
lfs setstripe -c <lustre-stripes.text> $TMP_PATH
spark-submit --executor-memory 2G $SPARK_BM_ROOT_PATH/input_files/create_text_spark.py --num-partitions=<spark-partitions.text> --file-size=<data-size.text> -o $TMP_PATH/<data-size.name>
