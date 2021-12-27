import logging

import azure.functions as func
import json
from azure.cosmos import cosmos_client


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    cosmos_config = {
    "ENDPOINT": "ENDPOINT_FROM_YOUR_COSMOS_ACCOUNT",
    "PRIMARYKEY": "KEY_FROM_YOUR_COSMOS_ACCOUNT",
    "DATABASE": "DATABASE_ID",  
    "CONTAINER": "YOUR_CONTAINER_ID" 
    }

    CONTAINER_LINK = f"dbs/{cosmos_config['DATABASE']}/colls/{cosmos_config['CONTAINER']}"
    FEEDOPTIONS = {}
    FEEDOPTIONS["enableCrossPartitionQuery"] = True

    query = {
        "query": f"SELECT * from c"
    }


    client = cosmos_client.CosmosClient(
        url_connection=cosmos_config["ENDPOINT"], auth={"masterKey": cosmos_config["PRIMARYKEY"]}
    )

    results = client.QueryItems(CONTAINER_LINK, query, FEEDOPTIONS)

    print(list(results))

    
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
