import requests
import boto3
import random

def obtainIP(serviceName):
    servicediscovery = boto3.client("servicediscovery")
    response = servicediscovery.discover_instances(
        NamespaceName='tracktrace',
        ServiceName= serviceName,
        MaxResults=10,
        HealthStatus='HEALTHY'
    )
    
    instanceArr = response["Instances"]
    instance = instanceArr[random.randint(0,len(instanceArr)-1)]

    #returns ip address
    return instance["Attributes"]['AWS_INSTANCE_IPV4']

# print(obtainIP('scraper_ymlu'))