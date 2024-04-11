#descarga bersion community,  https://www.mongodb.com/try/download
#instalacion : https://www.mongodb.com/docs/manual/tutorial
#modulo de conexion MongoDB : pip install pymongo
#ejecucion sudo mongo --dbpath "path de la base  de datos"
#conexion : mongodb://localhost


from pymongo import MongoClient

#db_client = MongoClient().local  #Is connected to the localhost, if yoy want a different connection you have to especificate 


#romete data base 
db_client =  MongoClient("mongodb+srv://carg127coni:DSXVptiHfOlqWFPg@cluster0.trdtf9d.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").cargi