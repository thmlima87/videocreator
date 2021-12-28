import pymongo
import yaml

# pegando as credenciais das apis
with open("credentials.yml","r") as c:
    try:
        credentials = yaml.safe_load(c)
    except yaml.YAMLError as exc:
        print(exc)



# Connect to mongodb
def connect():
    client = pymongo.MongoClient(credentials['mongo_connection_string'])
    return client

# Save documents
def saveMany(conn, doc, coll):
    
    try:
        x = conn['trends'][coll].insert_many(doc)
        result = "Registros inseridos com sucesso!"
    except pymongo.errors.BulkWriteError as err:
        result = err.details
    
    return result