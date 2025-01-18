from pymongo import MongoClient
import certifi
# Configuración de la conexión
MONGO_URI = "mongodb+srv://wcgarcia5:wcgarcia5@cluster0.ioe9u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
MONGO_DB_NAME = "seek_db"

client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client[MONGO_DB_NAME]
