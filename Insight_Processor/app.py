import json
import datetime
from insights_generator import analyse_scraped_data,generateInsights
from LLM_handler import llm_impl
from aws_handler import store_data_to_s3,save_recommendations_to_dynamoDB
from shared import DAILY_SUMMARY_DATA_DIRECTORY,WEEKLY_SUMMARY_DATA_DIRECTORY,MONTHLY_SUMMARY_DATA_DIRECTORY,YEARLY_SUMMARY_DATA_DIRECTORY
from shared import DATE_FORMAT


def lambda_handler(event, context):

    message_body = event

    if 'Records' in event:
        for record in event['Records']:
            message_body = json.loads(record['body'])

    if message_body['event_type'] == 'daily':
        print("Directory: " + message_body['directory'])
        print("S3 Bucket: " + message_body['s3bucket'])
        print("Run Date: " + message_body['rundate'])

        analysis = analyse_scraped_data(message_body['s3bucket'],message_body['directory'], llm_interfacer=llm_impl)
        file_path = DAILY_SUMMARY_DATA_DIRECTORY + f"{message_body['rundate']}.json"
        store_data_to_s3(file_path, analysis)

    elif message_body['event_type'] == 'custom':
        print(message_body)

        generated_insights,file_name = generateInsights(message_body['s3bucket'], message_body['source_directory'], message_body['target_entities'],llm_interfacer=llm_impl)

        print("File name - " , file_name)
        file_path = message_body['target_directory'] + file_name

        store_data_to_s3(file_path, generated_insights)
        
        runDate : datetime = datetime.datetime.fromisoformat(message_body['rundate'].replace("Z", "+00:00")).date()
        feedId = runDate.strftime(DATE_FORMAT)
        type = 'Weekly'
        if(message_body['target_directory'] == MONTHLY_SUMMARY_DATA_DIRECTORY):
            feedId = feedId[:7]
            type = 'Monthly'
        elif(message_body['target_directory'] == YEARLY_SUMMARY_DATA_DIRECTORY):
            feedId = feedId[:4]
            type = 'Yearly'
        
        print(generated_insights.get('recommendations',[]))
        save_recommendations_to_dynamoDB(generated_insights.get('recommendations',[]), feedId, type, runDate.strftime(DATE_FORMAT))



    else:
        print("Unknown event type: " + message_body['event_type'])

