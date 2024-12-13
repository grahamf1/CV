import os
from azure.cosmosdb.table import TableService, Entity

the_connection_string = os.environ.get('AZURE_COSMOS_CONNECTION_STRING')
print(f"Connection string: {the_connection_string}")
if not the_connection_string:
    raise ValueError("AZURE_COSMOS_CONNECTION_STRING environment variable is not set")

try:
    table_service = TableService(endpoint_suffix="table.cosmos.azure.com", connection_string=the_connection_string)
    print("TableService created successfully.")
except Exception as e:
    print(f"Error creating TableService: {str(e)}")
    
table_name = 'comments'
table_service.create_table(table_name)

def add_comment(name, email, comment):
    entity = Entity()
    entity.PartitionKey = 'comments'
    entity.RowKey = f"{name}_{email}"
    entity.name = name
    entity.email = email
    entity.comment = comment
    table_service.insert_entity(table_name, entity)

def get_all_comments():
    comments = table_service.query_entities(table_name, filter="PartitionKey eq 'comments'")
    return [{'name': entity.name, 'email': entity.email, 'comment': entity.comment} for entity in comments]