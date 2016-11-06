#Comando a usar para los contratos
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
