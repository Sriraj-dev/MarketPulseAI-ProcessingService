import datetime
import boto3
from live_market_data_handler import liveMarketHandler
from shared import DYNAMODB_TABLE_NAME

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DYNAMODB_TABLE_NAME)


def save_recommendations_to_dynamoDB(recommendations, feedId : str, type : str, rundate : str):
    
    feed = create_dynamoDB_feed(recommendations, feedId, type, rundate)

    try:
        with table.batch_writer() as batch:
            for entry in feed:
                batch.put_item(Item=entry)
        print( {
            "statusCode": 200,
            "body": f"Recommendations successfully pushed into DynamoDB with FeedID - {feedId}"
        } )
    except Exception as e:
        print(f"Error saving recommendations to DynamoDB: {e}")


def create_dynamoDB_feed(recommendations, feedId : str, type : str, rundate : str):
    feed = []
    for recommendation in recommendations:
        feed.append({
            'feedid': feedId,
            'type': type,
            'name': recommendation.get('name', ""),
            'ticker': recommendation.get('ticker',"N/A"),
            'recommendation': recommendation.get('recommendation',""),
            'reason': recommendation.get('reason',""),
            'source': recommendation.get('source',""),
            'dateofrecommendation' : rundate,
            'suggested_at_price' : liveMarketHandler.get_current_stock_price(recommendation.get('ticker',"")),
            'current_price' : 0,
            'updated_at' : ""
        })
    
    return feed
