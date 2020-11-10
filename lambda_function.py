#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3
import json
from datetime import date

def lambda_handler(event, context):
    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        photo = record['s3']['object']['key']
        try:
           response = detect_text(photo, bucket)
           print (response)
           return response
        
        except Exception as e:
           print(e)
           print ("Error processing object {} from bucket {}. " .format(photo, bucket))
           raise e

def detect_text(photo, bucket):

    client=boto3.client('rekognition')
    sns = boto3.client('sns')
    today = date.today()
    d2 = today.strftime("%B %d, %Y")
    a = []
    response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
                        
    textDetections=response['TextDetections']
    print ('Detected text\n----------')
    for text in textDetections:
            print ('Detected text:' + text['DetectedText'])
            print ('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
            print ('Id: {}'.format(text['Id']))
            if 'ParentId' in text:
                print ('Parent Id: {}'.format(text['ParentId']))
            print ('Type:' + text['Type'])
            print()
            if not 'ParentId' in text:
              a.append(text['DetectedText'])
            
    msg = '\n'.join(a)
            
##publish text as message to SNS if not empty            
    if len(a) != 0:
       print ('length of a - we are here')
       sns.publish(TopicArn='arn:aws:sns:eu-west-1:123456789012:myMotivations', 
              Subject= "Motivation for Today " + d2, 
              Message=msg)
    

    return len(textDetections)
    


if __name__ == "__main__":
    main()
