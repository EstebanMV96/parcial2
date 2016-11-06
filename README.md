#PARCIAL 2
##Esteban Moya- Cod:13207005

### 1) A continuación se mostrara los scripts necesarios para que nuestro servidor de integracion continua pueda ejecutar las pruebas.

####test_files.py
```python
import pytest
import files
import json

@pytest.fixture
def client(request):
	client=files.app.test_client()
	return client

def darArchivos(client):
	return client.get('/files',follow_redirects=True)


def eliminarArchivos(client):
	return client.delete('/files',follow_redirects=True)

def recently(client):
	return client.get('/files/recently_created',follow_redirects=True)


def crearArchivo(client):
	arch='prueba.txt'
	response = client.post('/files',data=json.dumps(dict(filename=arch,content='Hola mundo')),content_type='application/json')
	return response


def test_darArchivos(client):
	result=darArchivos(client)
	esta="comandos.py" in result.data
	esta1="files.py" in result.data
	assert esta, "comandos.py deberia de aparecer en los archivos listados"
	assert esta1, "files.py deberia de aparecer en los archivos listados"
	assert result.status=="200 OK", "El codigo de respuesta indica un error"
	
	
	
	
def test_eliminarArchivos(client):
	result=eliminarArchivos(client)
	assert "Todos los archivos no VIP fueron borrados" in result.data 
	assert result.status=="200 OK", "El codigo de respuesta indica un error"


def test_recently(client):
	result=recently(client)
	assert result.status=="200 OK", "El codigo de respuesta no fue el esperado"

def test_crearArchivo(client):
	result=crearArchivo(client)
	assert result.status=="201 CREATED", "Ocurrio un error al crear el archivo"
```

####files.py

```python
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

```

####comandos.py

```python
from subprocess import Popen, PIPE

def lsArchivos():
	#HOLA PROFE LOS ARCHIVOS LOS ESTABA CREANDO EN "/home/filesystem_user/Parciales/parcial1"
	archivos = Popen(["ls","/home/filesystem_user/Parciales/parcial1"], stdout=PIPE, stderr=PIPE).communicate()[0].split('\n')
	return filter(None,archivos)

def deleteFiles(nomArchivo):
	vip=["comandos.py","comandos.pyc","files.py"]
	if nomArchivo not in vip:
		kill=Popen(["rm","-f","/home/filesystem_user/Parciales/parcial1/"+nomArchivo], stdout=PIPE, stderr=PIPE)
		kill.wait()
		return True



def darArchivosRecientes():
	archivos = Popen(["find","-mtime","-1"], stdout=PIPE, stderr=PIPE)
	archivos1 = Popen(["grep","./"],stdin=archivos.stdout, stdout=PIPE, stderr=PIPE).communicate()[0].split('\n')
	return filter(None,archivos1)	
    	

def crearArchivo(nombre,contenido):
	nuevoArchivo= Popen(["touch","/home/filesystem_user/Parciales/parcial1/"+nombre], stdout=PIPE, stderr=PIPE)
	nuevoArchivo.wait()
	file=open("/home/filesystem_user/Parciales/parcial1/"+nombre,"w")
	file.write(contenido)
	file.close()
	if nombre in lsArchivos():
		return True

```







