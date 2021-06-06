To analyze sentiment using these files:
1. Create a VM in Google Cloud Platform
2. Create a virtual env, install dependencies, and run Sentiment-VM.py in the VM. This will read the Reddit RSS Feed from new posts in r/cryptocurrency and save as JSON to your bucket (replace 'reddit-data-bucket-jdxqd-2'). After the JSON is upload to the bucket, it will run entity analysis on it using GCP's NLP API, and save the output to the bucket as a txt file.
3. Create a postgresql database in Cloud SQL called 'reddit_table'. 
4. Run BlobToSQL in the VM which creates a table in the above database, converts the analysis data into tabular form, and saves it to this table. It will then query the SQL table and generate a graph which shows sentiment scores and magnitudes for the day. In essence, this graph shows how positive or negative Redditors are about the cryptocurrency market at the moment. 
5. [Optional] Create a CRON job on the VM to run these files intermittently.

![image](https://user-images.githubusercontent.com/36838938/120940634-1b19b200-c6d3-11eb-9f51-2f702478076a.png)
