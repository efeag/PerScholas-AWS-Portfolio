import json
import pymysql
import os
import boto3

sns = boto3.client("sns")

MAX_MESSAGE_LENGTH = 500  # maximum number of characters to include in the SNS message

def lambda_handler(event, context):
    print("Event received:", event)

    body = json.loads(event.get("body", "{}"))
    name = body.get("name", "N/A")
    email = body.get("email", "N/A")
    message = body.get("message", "N/A")

    # Truncate the message if it is too long
    truncated_message = message
    if len(message) > MAX_MESSAGE_LENGTH:
        truncated_message = message[:MAX_MESSAGE_LENGTH] + "… [truncated]"

    db_host = os.environ["DB_HOST"]
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    topic_arn = os.environ["SNS_TOPIC_ARN"]

    try:
        # Connect to the database
        conn = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            db=db_name,
            connect_timeout=5
        )

        with conn.cursor() as cur:
            sql = """
                INSERT INTO messages (name, email, message)
                VALUES (%s, %s, %s)
            """
            cur.execute(sql, (name, email, message))
            conn.commit()

        # Human-readable, truncated SNS message
        formatted_message = (
            f"📩 New Contact Form Submission\n"
            f"-------------------------------\n"
            f"Name   : {name}\n"
            f"Email  : {email}\n"
            f"Message:\n{truncated_message}\n"
            f"-------------------------------"
        )

        sns.publish(
            TopicArn=topic_arn,
            Subject="New Contact Form Submission",
            Message=formatted_message
        )

        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"message": "Form submitted successfully"})
        }

    except Exception as e:
        print("Error:", e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
