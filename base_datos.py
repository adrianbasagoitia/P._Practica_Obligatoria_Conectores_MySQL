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


# ######################################################################### #
def query_crear_tabla(nombre_tabla:str, comprobar_existencia:bool, columnas:list[tuple], primary_key:list[str], foreign_key:list[tuple]):
  """
  Genera una query para la creacion de una tabla en la base de datos.

  Args:
      nombre_tabla (str): 
        Nombre de la nueva tabla.
      
      comprobar_existencia (bool): 
        Indica si se debe comprobar la existencia (TRUE), es decir, incorporar
        IF NOT EXISTS, o no incorporar nada.
      
      columnas (list[tuple]): 
        Lista de tuplas conteniendo la informacion de las columnas. Cada tupla 
        DEBE tener seis posiciones.
          - nombre columna (str).
          - tipo de dato (str).
          - Nullable (bool): Indica si la columna puede ser NULL (True) o NOT
            NULL (False)
          - Unique (bool).
          - AUTO_INCREMENT(bool): Si es una columna con un valor autogenerado 
            (True) o no.
          - DEFAULT (str): Si tiene un valor por defecto (Tiene contenido) o no 
            tiene ningun valor por defecto (None).

      
      primary_key (list[str]):
        Lista de cadenas de caracteres con los nombres de las columnas que seran
        la clave primaria de la tabla. 
      
      foreign_key (list[tuple]):
        Lista de tuplas conteniendo la informacion de las claves foraneas. Cada
        tupla DEBE tener cinco posiciones.
          - nombre de la columna de esta tabla (str).
          - nombre de la tabla referenciada (str).
          - nombre del campo de la tabla referenciada (str).
          - ON UPDATE (str). Condicion (CASCADE, SET NULL, NO ACTION) o None.
          - ON DELETE (str). Condicion (CASCADE, SET NULL, NO ACTION) o None.

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
  fk:tuple = None # Almacena una tupla de la lista de foreign_key
  query:str = "CREATE TABLE " # Query a crear

  # Local code
  # ##### IF NOT EXISTS #####
  if(comprobar_existencia):
    query += "IF NOT EXISTS "

  # ##### Nombre de la tabla #####
  query += f"{nombre_tabla.upper()} (\n"

  # ##### Columnas #####
  # Cada columna es una tupla de la lista. La tupla DEBE contener los siguientes
  # campos:
  # Nombre columna | Tipo dato | NULLABLE | UNIQUE | AUTO_INCREMENT | DEFAULT
  for columna in columnas:
    query += f"\t{columna[0].upper()} " # Nombre de la columna
    query += f"{columna[1].upper()} " # Tipo de dato
    
    # Nullable: Si es NULL o NOT NULL
    if(columna[2] == False): # NOT NULL: No es NULLABLE
      query += "NOT NULL "

    else: # NULL: Es NULLABLE
      query += "NULL "
    
    # UNIQUE
    if(columna[3] == True):
      query += "UNIQUE "
    
    # AUTO_INCREMENT
    if(columna[4] == True):
      query += "AUTO_INCREMENT "
    
    # DEFAULT
    if(columna[5] is not None):
      query += f"DEFAULT {columna[5].upper()} "
    
    # Siempre anyadir una coma al final. Despues siempre tiene que venir la 
    # primary key.
    query += ",\n"
  

  # PRIMARY KEY
  # La lista, tiene que contener todos los nombres de las columnas que seran 
  # clave primaria.
  query += "\tPRIMARY KEY(" # Anyadir la cabecera de la clave primaria
  for i in range(0, len(primary_key)): # Anyadir todos los nombres de las 
    # columnas que seran clave primaria
    query += primary_key[i].upper()

    if(i != len(primary_key)-1): # A la ultima no se le pone ,
      query += ", "
  
  query += ")\n" # Cerrar el parentesis y nueva linea. Esta puede ser la ultima
  # linea de la consulta, no se pone coma.

  # FOREIGN KEY
  # Cada foreign key es una tupla de la lista. La tupla DEBE contener los 
  # siguientes campos:
  # Nombre del campo de esta tabla | nombre tabla referenciada | Campo tabla referenciada | ON UPDATE | ON DELETE.
  # Por decision de disenyo ON UPDATE y ON DELETE solo aceptan CASCADE, 
  # SET NULL, NO ACTION
  for i in range(0, len(foreign_key)):
    fk = foreign_key[i] # asignar la tupla a la variable

    query += f"\t,FOREIGN KEY ({fk[0].upper()}) REFERENCES {fk[1].upper()}({fk[2].upper()}) "

    # Si hay un ON UPDATE
    if(fk[3] is not None):
      query += f"ON UPDATE {fk[3].upper()} "

    # Si hay un ON DELETE
    if(fk[4] is not None):
      query += f"ON DELETE {fk[4].upper()} "
    
    # Salto de linea
    query += "\n"
  

  # Al final de todo cerrar el parentesis y poner el punto y coma
  query += ");"

  return (0, "Query para generar tabla escrita.", query)


# ######################################################################### #
def query_eliminar_tabla(nombre_tabla:str):
  """
  Crea una cadena de caracteres con la query necesaria para eliminar una tabla 
  de la base de datos.

  Args:
      nombre_tabla (str): 
        Nombre de la tabla a eliminar en la base de datos.

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
  return (0, "\nQuery para la eliminacion de la base de datos escrita.", f"DROP TABLE {nombre_tabla.upper()};")


# ######################################################################### #
def query_insert_into(nombre_tabla:str, nombre_columnas:list[str], filas:list[tuple]):
  # Local variables
  query = "INSERT INTO " # Query a crear

  # Local code
  # ##### Nombre de la tabla #####
  query += f"{nombre_tabla.upper()} (" # Dejar abierto el parentesis para el 
    # nombre de las columnas

  # ##### Columnas #####
  for i in range(0, len(nombre_columnas)): # Iterar sobre la lista de nombres
    query += nombre_columnas[i].upper() # El nombre de la columna

    if(i != len(nombre_columnas)-1): # Si no es el ultimo nombre, anyadir la 
      # coma y el espacio
      query += ", "
  
  # Por ultimo cerrar el parentesis, anyadir la palabra VALUES y el salto de 
  # linea
  query += ") VALUES \n"

  # ##### Filas #####
  for i in range(0, len(filas)): # Iterar sobre la lista de tuplas, cada tupla 
    # es igual a una fila en la tabla
    
    # Anyadir tabulacion y abrir parentesis
    query += "\t("

    # Recorrer la tupla de la fila y anyadir cada uno de los elementos
    for j in range(0, len(filas[i])): # Por cada elemento en la tupla
      query += filas[i][j].upper()

      if(j != len(filas[i])-1): # Si no es el ultimo elemento
        query += ", "
    
    # Al final de cada fila cerrar el parentesis
    query += ")"

    # Si no es la ultima fila anyadir la coma y un salto de linea
    if(i != len(filas)-1): # Si no es la ultima fila
      query += ",\n"
  
  # Al final de la query anyadir el punto y coma
  query += ";"

  return (0, "Query para generar insert escrita.", query)