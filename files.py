from flask import Flask, abort, request
import json, time
from comandos import lsArchivos, deleteFiles,darArchivosRecientes, crearArchivo
app = Flask(__name__)

@app.route('/files',methods=['GET'])
def darArchivos():
  list = {}
  list["files"] = lsArchivos()
  return json.dumps(list), 200

@app.route('/files',methods=['DELETE'])
def eliminarArchivos():
	
	for i in lsArchivos():
		deleteFiles(i)
			
	return "Todos los archivos no VIP fueron borrados",200

@app.route('/files/recently_created',methods=['GET'])
def recently():
  list = {}
  list["Archivos creados hace menos de un dia"] = darArchivosRecientes()
  return json.dumps(list),200
  
@app.route('/files',methods=['POST'])
def newArchivo():
  content = request.get_json(silent=True)
  nombreA = content['filename']
  contenido= content['content']
  if crearArchivo(nombreA,contenido):
  	return "Archivo creado",201
  
@app.route('/files/recently_created',methods=['POST'])
def recently3():
 
  return "No implementado",404

@app.route('/files/recently_created',methods=['PUT'])
def recently1():
 
  return "No implementado",404

@app.route('/files/recently_created',methods=['DELETE'])
def recently2():
 
  return "No implementado",404

@app.route('/files',methods=['PUT'])
def recently5():
 
  return "No implementado",404

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=8080,debug='True')
