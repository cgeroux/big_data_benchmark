run:
	-hdfs dfs -put english-wordlist.txt /user/ubuntu
	-hdfs dfs -rm -R /user/ubuntu/wordcounts
	spark-submit --master yarn --deploy-mode cluster create_text_spark.py --num-exe=2