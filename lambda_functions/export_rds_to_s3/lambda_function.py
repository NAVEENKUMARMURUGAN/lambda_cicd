import os
import pandas as pd
import boto3
from datetime import datetime
import logging
import psycopg2

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
  try:
    # Extract date from event if provided, else use current date
    if 'date' in event:
      target_date = event['date']
    else:
      target_date = datetime.utcnow().strftime('%Y-%m-%d')

    logger.info('Target Date: %s', target_date)
    
    # Connect to PostgreSQL database using environment variables
    db_name = os.environ.get('DB_NAME')
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    host = os.environ.get('DB_HOST')
    port = os.environ.get('DB_PORT')
    
    conn = psycopg2.connect(
      dbname=db_name,
      user=user,
      password=password,
      host=host,
      port=port
    )
    cursor = conn.cursor()

    # Fetch data from PostgreSQL
    cursor.execute(f"SELECT * FROM public.temp_bank_transactions where transaction_date='{target_date}';")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    # Convert data to pandas DataFrame
    df = pd.DataFrame(data)

    bucket_name = os.environ.get('S3_BUCKET_NAME')
    
    if int(boto3.__version__.split('.')[0]) >= 1 and int(boto3.__version__.split('.')[1]) >= 16:
      df.to_csv(f's3://{bucket_name}/transaction/{target_date}/data.csv', index=False)
    else:
      logger.warning('boto3 version does not support direct S3 upload yet. Using in-memory buffer.')
      csv_buffer = io.StringIO()
      df.to_csv(csv_buffer, index=False)  # Don't include index row in CSV
      s3 = boto3.client('s3')
      key = f'transaction/{target_date}/data.csv'
      s3.put_object(Body=csv_buffer.getvalue().encode('utf-8'), Bucket=bucket_name, Key=key)
    return {
      'statusCode': 200,
      'body': f'Data loaded to S3 successfully for {target_date}!'
    }
  except psycopg2.OperationalError as e:
    logger.error('Database connection error: %s', str(e))
    raise e
  except boto3.exceptions.S3UploadFailedError as e:
    logger.error('S3 upload error: %s', str(e))
    raise e
  except Exception as e:  # Catch other unexpected errors
    logger.error('Unexpected error: %s', str(e))
    raise e