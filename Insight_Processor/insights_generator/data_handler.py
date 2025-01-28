import boto3
from LLM_handler import LLM_Interfacer
s3_client = boto3.client('s3')

def analyse_scraped_data(s3Bucket : str,directory : str,llm_interfacer : LLM_Interfacer):

    ## Iterate through the sBuckets directory for all the files and generate insights.
    object_keys = get_object_keys(s3Bucket, directory);
    print(object_keys);

    market_data = []

    for key in object_keys:
        sourcewebsite = key.split("/")[-1].split(".")[0]
        print("Collecting data from ", sourcewebsite)
        response = s3_client.get_object(Bucket=s3Bucket, Key=key)
        content = response['Body'].read().decode('utf-8')

        intro = "The following data is sourced from website " + sourcewebsite + " On " + key.split("/")[-2] + " :\n"
        #summary = llm_interfacer.summarise_scraped_data(content, additional_prompt)
        market_data.append(intro + content)

    ## Join all the websites data.
    final_market_data = '\n\n'.join(market_data)

    ## Send the final_summary into LLM Handler to analyse the market data based on the generated summary
    analysis = llm_interfacer.analyse_daily_market_data(final_market_data)
    return analysis

def generateInsights(s3Bucket: str, source_directory : str, target_entities : int, llm_interfacer : LLM_Interfacer):

    try:
        # List objects in the source directory
        response = s3_client.list_objects_v2(Bucket=s3Bucket, Prefix=source_directory)
        if "Contents" not in response:
            raise ValueError(f"No files found in directory: {source_directory}")

        # Sort files by LastModified in descending order
        sorted_files = sorted(response["Contents"], key=lambda obj: obj["LastModified"], reverse=True)

        # Limit to the most recently uploaded files (target_entities)
        selected_files = sorted_files[:target_entities]
        selected_files.reverse()

        market_data = ""
        start_date = ""
        end_date = ""
        for file in selected_files:
            file_key = file["Key"]
            if "/" in file_key[len(source_directory):]: 
                continue

            print("Collected : ",file["Key"])


            file_name = (file_key.split("/")[-1]).split('.')[0]  # Extract file name from the key
            if(start_date == ""):
                start_date = file_name.split("~")[0]
            end_date = file_name.split("~")[-1]

            # Get file content
            file_obj = s3_client.get_object(Bucket=s3Bucket, Key=file_key)
            file_content = file_obj["Body"].read().decode("utf-8")  # Decode file content (assuming UTF-8)

            # Combine file name and content
            market_data += f"{file_name}:\n{file_content}\n\n"
        
        file_name = f"{start_date}~{end_date}.json"

        print("Content :" ,market_data)
        generated_insights = llm_interfacer.generate_insights(market_data)

        return generated_insights,file_name

    except Exception as e:
        print(f"Error generating insights: {e}")
        return "",""


def get_object_keys(s3Bucket: str, directory : str):
    response = s3_client.list_objects_v2(Bucket=s3Bucket, Prefix=directory)
    object_keys = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'] != directory]
    return object_keys
