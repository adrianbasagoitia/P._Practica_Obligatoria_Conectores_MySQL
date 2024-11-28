# ############################################################################ #
#                                   IMPORT 
# ############################################################################ #


# ############################################################################ #
#                                   GLOBAL 
# ############################################################################ #


# ################################ Methods ################################ #
def crear_conexion(usuario:str, contrasenya:str, puerto:int, es_conexion_inicial:bool = False, nombre_base_datos:str = None):
  """
  Crea una conexion al servidor de la base de datos MySQL.

  En primer lugar, importa el conector a la base de datos (PyMySQL).
  Posteriormente, la ejecucion toma dos caminos en funcion de si es la 
  primera conexion a la base de datos o subsiguientes.

  - Si es la primera conexion, necesita el usuario, la contrasenya y el puerto
    donde esta ejecutando el servidor.
  
  - Si es una conexion subsiguiente, necesita ademas de los parametros 
    usuario, contrasenya y puerto, el nombre de la base de datos a la que se 
    debe realizar la conexion.
  
  Args:
      usuario (str): 
        Cadena de caracteres conteniendo el usuario que se utilizara para 
        conectarse a la base de datos.
      
      contrasenya (str): _description_
        Cadena de caracteres conteniendo la contrasenya que se utilizara para
        conectarse a la base de datos.
      
      puerto (int): 
        Numero del puerto donde esta ejecutando el servidor de la base de datos.

      es_conexion_inicial (bool, optional):
        Indica si es la primera conexion a realizar con el servidor de la base
        de datos (True) o son subsiguientes (False). Opcional. Valor por 
        defecto False.

      nombre_base_datos (str, optional):
        Cadena de caracteres con el nombre de la base de datos a la que 
        realizar la conexion. Solo se debe utilizar este paramtetro con
        conexiones que no sean la primera.

  Returns:
      tuple: dos o tres posiciones:
        - codigo de resultado (int): 
          0 en caso de ejecucion correcta, -1 en cualquier otro caso.
        - mensaje de ejecucion (str): 
          Mensaje para el usuario informando del resultado de la ejecucion 
          del metodo.
        - conexion (Connection):
          Conexion con el servidor de la base de datos. Opcional.
  """ 
  # Import
  import pymysql
  from pymysql import Connection, Error

  # Local variables
  mensaje:str = "" # Mensaje de ejecucion de metodo.
  conn:Connection = None # Conexion a la base de datos
  retorno:tuple = None # Tupla conteniendo la informacion necesaria para el 
  # retorno del metodo. 2 o 3 posiciones: Codigo ejecucion (0 - Correcta;
  # -1 incorrecta), mensaje de resultado de ejecucion, conexion a la base
  # de datos (opcional).


  # Local code
  if(es_conexion_inicial): # Es la primera conexion al servidor de la base de 
    # datos MySQl. Crear unicamente la conexion.
    try:
      conn = pymysql.connect(
        user = f"{usuario}",
        password= f"{contrasenya}",
        port = f"{puerto}"
      )
      # Si se llega hasta aqui, la conexion se ha creado correctamente
      mensaje = "\nConexion establecida con el servidor de la base de datos MySQL."
    
    except pymysql.Error as e:
      mensaje = f"ERROR. Error al realizar la conexion al servidor de la base de datos: {e}"

  else: # No es la conexion inicial, y la base de datos DEBE existir.
    # Esta conexion, lleva implicita la instruccion USE <nombre_base_datos>;
    try:
      conn = pymysql.connect(
        user = f"{usuario}",
        password= f"{contrasenya}",
        port = f"{puerto}",
        database= f"{nombre_base_datos}"
      )
      # Si se llega hasta aqui, la conexion se ha creado correctamente
      mensaje = "\nConexion establecida con el servidor de la base de datos MySQL."
    
    except pymysql.Error as e:
      mensaje = f"ERROR. Error al realizar la conexion al servidor de la base de datos: {e}"
  
  # Generar tupla de retorno de ejecucion
  if("ERROR" in mensaje): # Ejecucion erronea, dos posiciones
    retorno = (-1, mensaje)
  
  else: # Ejecucion vorrecta, tres posiciones
    retorno = (0, mensaje, conn)
  
  return retorno


# ######################################################################### #
def comprobar_conexion(conn):
  """
  Comprueba la apertura de una conexion al servidor de la base de datos.

  Sobre la conexion recibida como parametro, se intenta crear un cursor,
  si la creacion es correcta, la conexion continua abierta, y se cierra el
  cursor. Por el contrario, si el cursor no se crea hay algun problema.

  Args:
      conn (Connection): 
        Conexion de la que se quiere comprobar el estado.
  
  Returns:
      tuple: dos o tres posiciones:
        - codigo de resultado (int): 
          0 en caso de ejecucion correcta, -1 en cualquier otro caso.
        - mensaje de ejecucion (str): 
          Mensaje para el usuario informando del resultado de la ejecucion 
          del metodo.

  """
  # Import
  import pymysql
  from pymysql import Connection, Error
  from pymysql.cursors import Cursor

  # Local variables
  cursor:Cursor = None # Instancia de cursor, para comprobar que la conexion
    # esta abierta
  

  # Local code
  try: # Intentar crear un cursor sobre la conexion para comprobar que sigue 
    # abierta
    cursor = conn.cursor()
    # Si se llega hasta aqui, la conexion continua abierta
    mensaje = "\nLa conexion esta abierta."
    cursor.close() # Cerrar el cursor, para evitar gastar recursos

  except pymysql.Error as e: # La conexion esta cerrada, u otro error.
    mensaje = "\nERROR. La conexion no esta abierta."
  

  if("ERROR" in mensaje): # Ejecucion erronea
    retorno = (-1, mensaje)
  
  else: # Ejecucion vorrecta
    retorno = (0, mensaje)



