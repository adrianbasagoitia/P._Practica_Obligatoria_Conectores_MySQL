# ############################################################################ #
#                                   IMPORT 
# ############################################################################ #
import os


# ############################################################################ #
#                                   GLOBAL 
# ############################################################################ #


# ################################ Methods ################################ #
def iniciar_programa():
  # Local variables
  conector_presente:bool = False # Contiene si la libreria pymysql esta 
  # presente en el sistema.


  # Local code
  print("\n"*2+"#"*60)
  print("Inicializando programa...")

  # Comprobar instalacion de pymsql
  print("Comprobando instalacion del conector PyMySQL...")
  conector_presente = comprobar_instalacion_pymyqsl()

  if(conector_presente):
    print("\nConector PyMySQL presente en el sistema.")
  
  else:
    print("El conector PyMySQL no esta presente en el sistema.")
    print("Sin un conector a la base de datos, el programa no puede continuar")
    print("con la ejecucion.")
    print("\nPuede instalar el conector a traves de pip con el siguiente comando:")
    print("\t\tpip install PyMySQL")
    print("o puede consultar otras formas de instalacion en la documentacion")
    print("oficial del conector:")
    print("https://pymysql.readthedocs.io/en/latest/")

    print("\n"*2+"Terminando ejecucion del programa."+"\n"+"#"*60, end=" ")


# ######################################################################### #
def comprobar_sistema_operativo():
  """
  Comprueba que sistema operativo esta ejecutando el fichero .py.

  La comprobacion se realiza mediante el atributo name de la libreria os.

  Solo se aceptan sistema operativos Windows (nt), o sistemas operativos
  Linux / UNIX (posix). Esto es una decision de disenyo basada en los sistemas
  operativos a los que los desarrolladores tienen acceso.

  Returns:
      tuple: dos o tres posiciones:
        - codigo de retorno (int): 0 en caso de ejecucion correcta, -1 en
          cualquier otro caso.
        - mensaje de ejecucion (str): Mensaje para el usuario informando del
          retorno de la ejecucion del metodo.
        - separador (str): Caracter separador de rutas del sistema de ficheros.
  """
  # Local variables
  sistema_operativo:str = None # Almacena el nombre del sistema operativo
  # donde se esta ejecutando el fichero .py
  retorno:tuple = None # Tupla conteniendo la informacion necesaria para el 
  # retorno del metodo. 2 o 3 posiciones: Codigo ejecucion (0 - Correcta;
  # -1 incorrecta), mensaje de retorno de ejecucion, el separador del
  # sistema de ficheros: Opcional.


  # Local code
  # Obtener el sistema operativo de la maquina donde se esta ejecutando
  # el fichero python
  sistema_operativo = os.name

  if(sistema_operativo == "nt"): # Si es sistema operativo Windows
    retorno = (0, "\nSistema operativo Windows detectado.", os.sep)
  
  elif(sistema_operativo == "posix"): # Si es sistema operativo Linux / UNIX
    retorno = (0, "\nSistema operativo Linux / UNIX detectado.", os.sep)
  
  else: # Cualquier otro sistema operativo
    retorno = (-1, "\nERROR. El programa no soporta la ejecucion en el sistema "+
    f"operativo {sistema_operativo}.\n Terminando la ejecucion del programa.")
  
  return retorno


# ######################################################################### #
def obtener_directorio_trabajo(separador:str):
  """
  Obtiene el directorio de trabajo del programa.

  Se obtiene a traves de __file__. Tambien se podria obtener a traves de
  sys.argv[0].

  Se obtiene el path, se divide por el caracter separador del sistema de
  ficheros, y se recrea hasta el directorio que contiene el fichero.py

  Returns:
      tuple: Dos posiciones:
        - path del directorio (str): Ruta absoluta del directorio que
          contiene el fichero .py con el caracter separador al final.
        - mensaje de ejecucion (str): Mensaje para el usuario informando del
          retorno de la ejecucion del metodo.
  """
  # Local variables
  path:str = None # Ruta absoluta del fichero .py | Ruta al directorio que
  # contiene el fichero .py
  path_lista:list[str] # Path dividido por separador
  retorno:str # Tupla conteniendo la informacion necesaria para el 
  # retorno del metodo. 2 posiciones: path del directorio de trabajo.
  # Mensaje informativo al usuario de la ejecucion del metodo


  # Local code
  path = __file__ # Obtener el path. En condiciones normales no DEBE lanzar
  # ninguna excepcion

  path_lista = path.split(separador) # Dividir el path

  path = "" # Limpiar el valor de la variable path

  # Recrear el path hasta el directorio que contiene el fichero .py
  # Por motivos practicos, se deja el caracter separador en el ultimo 
  # directorio
  for i in range(0, len(path_lista)-1):
    path += path_lista[i]+separador

  # Crear el retorno del metodo, path y mensaje
  retorno = (0, "\nEl directorio de trabajo queda designado como: "+
          f"\"{path[0:len(path)-1]}\".", path)
  

  return retorno


# ######################################################################### #
def comprobar_instalacion_pymyqsl():
  """
  Comprueba si la libreria PyMySQL esta instalada en el sistema.

  Para comprobar la existencia de la libreria, se intenta realizar un import
  de la misma, gestionandolo con un try / except. En caso de que la libreria
  no este instalada se genera una excepcion y se cambia el valor de una
  variable booleana a False. Si resulta estar instalada, se cambia el valor
  de la variable booleana a True.

  No se puede evitar el lanzamiento de la exception.

  Returns:
      bool: True, Si la libreria lxml esta instalada, False, en cualquier 
      otro caso.
  """
  # Local variables
  instalado:bool = False # Si la libreria PyMySQL esta instalada su valor sera
  # True, en cualquier otro caso, sera False.


  # Local code
  try: # Intentar importar la libreria
    import pymysql
    # Si se llega hasta aqui, la libreria esta instalada
    instalado = True
  
  except ModuleNotFoundError as e: # Si la libreria no esta instalada, se lanza
    # una excepcion, y se cambia el valor a False.
    instalado = False
  
  return instalado


# ############################################################################ #
#                                    MAIN 
# ############################################################################ #
if __name__ == "__main__":
  # Local variables 
  
  # Local code
  iniciar_programa()
  