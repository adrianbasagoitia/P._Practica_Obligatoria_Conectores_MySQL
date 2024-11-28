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


# ######################################################################### #
def ejecutar_instruccion(conn, atributos:tuple, query:str):
  """
  Ejecuta una query sobre la base de datos de la conexion.

  Comienza comprobando el estado de la conexion proporcionada como parametro.
  Si la conexion es valida, no realiza ninguna comprobacion adicional.
  Posteriormente, crea un cursor, y ejecuta la query sobre el. Si la query
  devuelve resultado, lo almacena en una variable para su devolucion.

  En otro caso, intenta recrear la conexion utilizando los parametros obtenidos
  desde get_atributos_conexion un numero maximo de tres veces. Si tras todos 
  estos intentos, no se tiene una conexion valida. La ejecucion del metodo es
  erronea.

  Args:
      conn (Connection): 
        Conexion sobre el servidor de la base de datos.

      atributos (tuple):
        Tupla con 4 posiciones: usuario, contrasenya, puerto, nombre base datos.

      query (str): 
        Query a ejecutar. Ej: CREATE DATABASE, SELECT, DELETE, INSERT INTO,...

  Returns:
      tuple: dos o tres posiciones:
        - codigo de resultado (int): 
          0 en caso de ejecucion correcta, -1 en cualquier otro caso.
        - mensaje de ejecucion (str): 
          Mensaje para el usuario informando del resultado de la ejecucion 
          del metodo.
        - contenido devuelto por la query (tuple, optional): 
          Tupla conteniendo las lineas afectadas por la query. Opcional.
  """
  # Import
  import pymysql
  from pymysql import Connection, Error
  from pymysql.cursors import Cursor
  
  # Local variables
  retorno_otros:tuple = None # Tupla que contendra el valor de retorno de 
  # otros metodos.
  num_filas:int = -1 # Numero de filas afectadas por la query.
  contenido_query:tuple = None # Contenido devuelto por la query
  cursor:Cursor = None # Cursor necesario para ejecutar la query.
  indice:int = 3 # Numero de intentos para recrear la conexion al servidor de
    # la base de datos
  creada:bool = False # La conexion ha sido recreada / Esta activa.
  retorno:tuple = None # Tupla conteniendo la informacion necesaria para el 
  # retorno del metodo. 2 o 3 posiciones: Codigo ejecucion (0 - Correcta;
  # -1 incorrecta), mensaje de resultado de ejecucion, contenido devuelto
  # por la query (opcional).


  # Local code
  retorno_otros = comprobar_conexion(conn)

  if(retorno_otros[0] == -1): # La conexion no existe
    # Iterar mientras que existan intentos restantes y la conexion no haya sido
    # creada
    while(indice > 0 and not creada):
      # Intentar crear la conexion
      retorno_otros = crear_conexion(atributos[0], atributos[1], atributos[2], nombre_base_datos = atributos[3])

      if(retorno_otros[0] == -1): # Conexion no creada
        indice -= 1
      
      else: # Conexion creada
        creada = True
        conn = retorno_otros[2] # Asignar la conexion
  
  else: # La conexion esta activa
    creada = True


  if(creada): # Si existe una conexion activa realizar la query
    try:
      # Crear el cursor
      cursor = conn.cursor()

      # Ejecutar la query y obtener el numero de lineas afectadas
      num_filas = cursor.execute(query)

      if(num_filas == 0): # No hay resultado delvuelto de la query
        mensaje = f"\nQuery ejecutada con exito."
      
      else: # Obtener el resultado de la query
        contenido_query = cursor.fetchall()
        mensaje = f"\nQuery ejecutada con exito y contenido almacenado."
      
    except pymysql.Error as e: # Cualquier error en el servidor
      mensaje = f"\nERROR. Error al ejecutar la query {query}: \n{e}"
  
  else: # No se puede establecer una conexion con la base de datos.
    mensaje = "\nERROR. No se puede establecer una conexion con el servidor de la base de datos."
  

  if("ERROR" in mensaje): # Ejecucion erronea
    retorno = (-1, mensaje)
  
  else: # Ejecucion valida.
    if(contenido_query is None): # No hay lineas afectadas
      retorno = (0, mensaje)
    
    else: # Hay lineas afectadas
      retorno = (0, mensaje, contenido_query)
  
  return retorno


# ######################################################################### #
def query_crear_base_datos(nombre_base_datos:str):
  """
  Crea una cadena de caracteres con la query necesaria para crear una base
  de datos en el servidor de la base de datos.

  Args:
      nombre_base_datos (str): 
        Nombre de la base de datos a crear en el servidor de la base de datos.

  Returns:
      tuple: tres posiciones:
        - codigo de resultado (int): 
          0 en caso de ejecucion correcta, -1 en cualquier otro caso.
        - mensaje de ejecucion (str): 
          Mensaje para el usuario informando del resultado de la ejecucion 
          del metodo.
        - query (str): 
          Cadena de caracteres conteniendo la query para ejecutar sobre la 
          conexion al servidor de la base de datos.
  """
  # Local variables

  # Local code
  return (0, "\nQuery para la creacion de la base de datos escrita.", f"CREATE DATABASE {nombre_base_datos.upper()};")


# ######################################################################### #
def query_eliminar_base_datos(nombre_base_datos:str):
  """
  Crea una cadena de caracteres con la query necesaria para eliminar una base
  de datos en el servidor de la base de datos.

  Args:
      nombre_base_datos (str): 
        Nombre de la base de datos a eliminar en el servidor de la base de 
        datos.

  Returns:
      tuple: tres posiciones:
        - codigo de resultado (int): 
          0 en caso de ejecucion correcta, -1 en cualquier otro caso.
        - mensaje de ejecucion (str): 
          Mensaje para el usuario informando del resultado de la ejecucion 
          del metodo.
        - query (str): 
          Cadena de caracteres conteniendo la query para ejecutar sobre la 
          conexion al servidor de la base de datos.
  """
  # Local variables

  # Local code
  return (0, "\nQuery para la eliminacion de la base de datos escrita.", f"DROP DATABASE {nombre_base_datos.upper()};")