# ############################################################################ #
#                                   IMPORT 
# ############################################################################ #
from io import TextIOWrapper

# ############################################################################ #
#                                   GLOBAL 
# ############################################################################ #


# ################################ Methods ################################ #
def leer_fichero(directorio_trabajo:str, nombre_fichero:str):
  """
  Lee el contenido del fichero nombre_fichero ubicado en directorio_trabajo.

  Intenta abrir el fichero en modo lectura y realizar la lectura completa
  del fichero utilizando la instruccion .readlines().

  Args:
      directorio_trabajo (str): 
        Directorio donde debe estar contenido el fichero. Debe contener al 
        final el caracter separador del sistema de ficheros.

      nombre_fichero (str): 
        Nombre del fichero que se quiere leer.

  Returns:
      tuple: tuple: dos o tres posiciones:
      - codigo de resultado (int): 
        0 en caso de ejecucion correcta, -1 en cualquier otro caso.
      - mensaje de ejecucion (str): 
        Mensaje para el usuario informando del resultado de la ejecucion del
        metodo.
      - contenido del fichero (str, optional): 
        Contenido del fichero almacenado en una lista de cadenas de caracteres.
  """
  # Local variables
  mensaje:str = None # Mensaje para el usuario informando del resultado 
  # de la ejecucion del metodo.
  fichero:TextIOWrapper = None # Almacena el descriptor de fichero, 
  # cuando el fichero .xml se abre.
  contenido:list[str] = None # Contenido leido del fichero
  retorno:tuple = None # Tupla conteniendo la informacion necesaria para el 
  # retorno del metodo. 2 o 3 posiciones: Codigo ejecucion (0 - Correcta;
  # -1 incorrecta), mensaje de resultado de ejecucion, contenido del fichero.
  
  
  # Local code
  try:
    # Abrir el fichero modo lectura
    with open(directorio_trabajo+nombre_fichero, "r") as fichero:

      # Leer todo el contenido del fichero
      contenido = fichero.readlines()

      # Si llega aqui, el fichero ha sido leido.
      # Generar mensaje para el usuario
      mensaje = f"\nFichero {nombre_fichero} leido correctamente."
  
  except FileNotFoundError as e: # El fichero no existe.
    mensaje = "\nERROR. El fichero no existe."

  except IOError as e: # Error de entrada / salida.
    mensaje = "\nERROR. Error de entrada / salida."
  
  except PermissionError as e: # Error de permisos
    mensaje = f"""\nERROR. El usuario no tiene permiso para leer el fichero 
    \"{nombre_fichero}\"."""
  
  except OSError as e: # Error en el sistema operativo: Permisos u otra causa.
    mensaje = "\nERROR. Error en el sistema operativo."

  except Exception as e: # Error general
    mensaje = f"\nERROR. Error Indeterminado.\n {e}."


  if("ERROR." in mensaje): # Si ha habido algun error
    retorno = (-1, mensaje)
  
  else: # Lectura correcta del fichero
    retorno = (0, mensaje, contenido)

  return retorno


# ######################################################################### #
def escribir_fichero(directorio_trabajo:str, nombre_fichero:str):
  """
  Escribe el contenido por defecto del fichero nombre_fichero ubicado en 
  directorio_trabajo.

  Intenta abrir el fichero en modo escritura y realizar la escritua de los
  parametros por defecto de la conexion al servidor de la base de datos.

  Args:
    directorio_trabajo (str): 
      Directorio donde debe estar contenido el fichero. Debe contener al 
      final el caracter separador del sistema de ficheros.

    nombre_fichero (str): 
      Nombre del fichero que se quiere crear.

  Returns:
    tuple: tuple: dos posiciones:
    - codigo de resultado (int): 
      0 en caso de ejecucion correcta, -1 en cualquier otro caso.
    - mensaje de ejecucion (str): 
      Mensaje para el usuario informando del resultado de la ejecucion del
      metodo.
  """
  # Local variables
  mensaje:str = None # Mensaje para el usuario informando del resultado 
  # de la ejecucion del metodo.
  fichero:TextIOWrapper = None # Almacena el descriptor de fichero, 
  # cuando el fichero .xml se abre.
  retorno:tuple = None # Tupla conteniendo la informacion necesaria para el 
  # retorno del metodo. 2 posiciones: Codigo ejecucion (0 - Correcta;
  # -1 incorrecta), mensaje de resultado de ejecucion.
  usuario:str = "root" # Usuario para la conexion al servidor de la base de 
    # datos.
  contrasenya:str = "my-secret-pw" # Contrasenya para la conexion al servidor 
    # de la base de de datos.
  puerto:int = 3308 # Puerto para la conexion al servidor de la base de de 
    # datos.
  
  # Local code
  try:
    # Abrir el fichero modo lectura
    with open(directorio_trabajo+nombre_fichero, "w") as fichero:
      # Escribir el contenido en el fichero
      fichero.write("# Fichero de configuracion.\n")
      fichero.write("# Este fichero contiene los parametros para realizar una conexion al servidor\n")
      fichero.write("# de la base de datos.\n")
      fichero.write("# SOLO puede haber una linea sin comentar.\n")
      fichero.write("# Las lineas de comentario comienzan por \"# \"\n")
      fichero.write("# El formato de la linea valida es usuario;contrasenya;puerto\n")
      fichero.write(f"{usuario};{contrasenya};{puerto}")


      # Si llega aqui, el fichero ha sido escrito.
      # Generar mensaje para el usuario
      mensaje = f"\nFichero {nombre_fichero} ha sido escrito correctamente."
  
  except FileNotFoundError as e: # El fichero no existe.
    mensaje = "\nERROR. El fichero no existe."

  except IOError as e: # Error de entrada / salida.
    mensaje = "\nERROR. Error de entrada / salida."
  
  except PermissionError as e: # Error de permisos
    mensaje = f"""\nERROR. El usuario no tiene permiso para leer el fichero 
    \"{nombre_fichero}\"."""
  
  except OSError as e: # Error en el sistema operativo: Permisos u otra causa.
    mensaje = "\nERROR. Error en el sistema operativo."

  except Exception as e: # Error general
    mensaje = f"\nERROR. Error Indeterminado.\n {e}."


  if("ERROR." in mensaje): # Si ha habido algun error
    retorno = (-1, mensaje)
  
  else: # Escritura correcta en el fichero
    retorno = (0, mensaje, (usuario, contrasenya, puerto))

  return retorno