import logging

import azure.functions as func
import json
import os
from azure.cosmos import CosmosClient


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    ENDPOINT =  os.environ['endpoint']
    PRIMARYKEY = os.environ['key'] 
    DATABASE =  os.environ['database']  
    CONTAINER =  os.environ['container'] 

    source = req.params.get('source')

    client = CosmosClient(ENDPOINT, credential=PRIMARYKEY)
    database = client.get_database_client(DATABASE)
    container = database.get_container_client(CONTAINER)

    if source:
        
        query = 'SELECT * FROM reviews p WHERE p.source = "' + source + '"'

        results = container.query_items(
            query=query
        )
        resList = list(results)

        return func.HttpResponse(resList[0]['comment'])
    
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a source value as either galaxy or mars in the query string or in the request body for a personalized response.",
             status_code=200
        )
