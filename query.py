# ############################################################################ #
#                                   IMPORT 
# ############################################################################ #


# ############################################################################ #
#                                   GLOBAL 
# ############################################################################ #


# ################################ Methods ################################ #
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
  return (0, "\nQuery para la eliminacion de la base de datos escrita.", f"DROP DATABASE IF EXISTS {nombre_base_datos.upper()};")


# ######################################################################### #
def query_usar_base_datos(nombre_base_datos:str):
  """
  Crea una cadena de caracteres con la query necesaria para usar una base
  de datos en el servidor de la base de datos.

  Args:
      nombre_base_datos (str): 
        Nombre de la base de datos a usar en el servidor de la base de 
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
  return (0, "\nQuery para el uso de la base de datos escrita.", f"USE {nombre_base_datos.upper()};")


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
def query_alter_table_add_fk(nombre_tabla:str, nombre_constraint:str, nombre_columna:str, nombre_tabla_referenciada:str, nombre_columna_referenciada:str, on_delete:str = None, on_update:str = None):
  """
  Crea una query de tipo ALTER TABLE para anyadir una FOREIGN KEY a una tabla
  ya existente.


  Args:
      nombre_tabla (str):
        Nombre de la tabla a la que anyadir la restriccion de clave foranea.
      
      nombre_constraint (str):
        Nombre de la restriccion asociada a la clave foranea.

      
      nombre_columna (str):
        Nombre de la columna que sera la clave foranea.

      
      nombre_tabla_referenciada (str):
        Nombre de la tabla sobre la que se hace la clave foranea.

      
      nombre_columna_referenciada (str):
        Nombre de la columna de la tabla sobre la que se hace la clave foranea.
      
      on_delete (str):
        Restriccion de integridad referencial en el caso de borrado de la fila.
        Si no se requiere en la consulta se debe dejar como None.
        
      on_update (str):
        Restriccion de integridad referencial en el caso de modificacion de la 
        fila. Si no se requiere en la consulta se debe dejar como None.
       
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
  query:str = "ALTER TABLE " # Query a crear


  # Local code
  # ##### Nombre tabla #####
  query += f"{nombre_tabla.upper()} "

  # ##### Nombre constraint #####
  query += f"ADD CONSTRAINT {nombre_constraint.upper()} "

  # ##### Nombre columna #####
  query += f"FOREIGN KEY ({nombre_columna.upper()}) "

  # ##### Tabla referenciada #####
  query += f"REFERENCES {nombre_tabla_referenciada.upper()} ({nombre_columna_referenciada.upper()}) "

  # ##### On Delete #####
  if(on_delete is not None): # Si hay ON DELETE
    query += f"ON DELETE {on_delete.upper()} "
  
  # ##### On Update ##### 
  if(on_update is not None): # Si hay ON UPDATE
    query += f"ON UPDATE {on_delete.upper()} "

  # Eliminar el posible espacio en blanco
  query = query.strip()

  # Al final de la query anyadir el punto y coma
  query += ";"

  return (0, "Query para alterar la tabla escrita.", query)


# ######################################################################### #
def query_insert_into(nombre_tabla:str, nombre_columnas:list[str], filas:list[tuple]):
  """
  Crea una query para insertar datos en una tabla.

  La insercion se realiza por filas completas. No se realiza ninguna validacion,
  se asume que antes de la llamada a este metodo han sido anteriormente 
  validados, y posteriormente seran validados de nuevo en la base de datos.

  Args:
      nombre_tabla (str): 
        Nombre de la tabla donde se insertaran las nuevas filas.

      nombre_columnas (list[str]): 
        Nombre de las columnas de la tabla sobre las que se insertaran datos.

      filas (list[tuple]): 
        Lista de tuplas conteniendo los datos a insertar en cada fila. El 
        tamanyo de cada tupla es indeterminado. Cada llamada sera diferente,
        debe ser del mismo tamanyo de nombre_columnas.

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


# ######################################################################### #
def query_delete_from(nombre_tabla:str, where:list[tuple], join:list[tuple] = None):
  """
  Crea una query para eliminar filas de una tabla.

  Es un metodo interno al programa, el usuario nunca lo tocara o modificara.
  Por lo tanto, no se verifica la validez de los parametros introducidos.
  Se asume que siempre son correctos.

  Args:
      nombre_tabla (str): 
        Nombre de la tabla donde se insertaran las nuevas filas.

      where (list[tuple]):
        Lista de tuplas, cada tupla es una condicion que se debe anyadir al
        where. Cada tupla consta de cuatro posiciones:
          - Nombre de la tabla (str):
            Tabla sobre la que se comprobara la condicion.

          - Nombre del campo (str):
            Nombre del campo sobre el cual aplicar la condicion.
          
          - Condicion (str):
            Condicion a aplicar sobre el campo, solo se acepta <, > o =.
          
          - Valor de la condicion (str):
            Valor a aplicar con la condicion sobre el campo. Si es una
            cadena de caracteres se deben introducir " o '.

      join (list[tuple], optional):
        Lista de tuplas, cada tupla es un join que se debe anyadir a la 
        consulta. Cada tupla, consta de 4 posiciones:
          - Tipo de join (str):
            Tipo  de join a anadir a la consulta.

          - Nombre de la tabla (str):
            Nombre de la tabla sobre la que hacer el join.
          
          - Campo tabla original (str):
            Campo de la tabla original por el cual hacer el join.
          
          - Campo tabla join (str):
            Campo de la tabla anyadida por el cual hacer el join.
        Este es un parametro opcional. Su valor por defectos es None.
        
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
  query = "DELETE " # Query a crear

  # Local code
  ##### Nombre Tabla #####
  query += f"{nombre_tabla.upper()} " # Anyadir el nombre de la tabla de la que 
    # borrar
  query += f"FROM {nombre_tabla.upper()}\n"


  ##### Join #####
  if(join is not None): # Si hay que hacer algun Join
    # Estructura de la tupla de un join
    # Tipo Join (Inner, Left, Right), Nombre Tabla | nombre_campo_tabla |
    # nombre_campo_tabla_join
    for i in range(0, len(join)):
      query += f"\t{join[i][0].upper()} {join[i][1].upper()}\n\t\tON {nombre_tabla.upper()}.{join[i][2].upper()} = {join[i][1].upper()}.{join[i][3].upper()}\n"
      # Por cada join una linea. Tipo de Join nombre_tabla ON 
      # nombre_tabla_original.campo = nombre_tabla.campo
      # Ej INNER JOIN DEPARTAMENTO ON EMPLEADO.DEPARTAMENTO = DEPARTAMENTO.ID
  
  ##### Where #####
  query += "\tWHERE\n" # Anyadir el where

  # Estructura de la tupla de un where
  # nombre_tabla | nombre_campo | condicion (<, >, =) | valor |
  for i in range(0, len(where)): # Recorrer la lista de condiciones del where
    # Anyadir el where
    query += f"\t\t{where[i][0].upper()}.{where[i][1].upper()} {where[i][2].upper()} {where[i][3].upper()}"

    if(i != len(where)-1): # Si no es la ultima clausula, anyadir el AND
      query += " AND\n"
  
  # Al final de la consulta, anyadir el punto y coma
  query += ";"

  return (0, "Query para generar delete from escrita", query)


# ######################################################################### #
def query_update(nombre_tabla:str, set:list[tuple], join:list[tuple] = None, where:list[tuple] = None):
  """
  Crea una query para modificar filas de una tabla.

  Es un metodo interno al programa, el usuario nunca lo tocara o modificara.
  Por lo tanto, no se verifica la validez de los parametros introducidos.
  Se asume que siempre son correctos.

  Args:
      nombre_tabla (str): 
        Nombre de la tabla donde se insertaran las nuevas filas.

      set (list[tuple]):
        Lista de tuplas, cada tupla es un set, que se debe anyadir a la
        consulta. Cada tupla tiene 3 posisicones:
          - Nombre tabla (str):
            Nombre de la tabla de la columna a modificar el valor.
          
          - Nombre campo (str):
            Nombre de la columna a modificar el valor.
          
          - Valor (str):
            Nuevo valor de la columna. Si es una
            cadena de caracteres se deben introducir " o '.

      join (list[tuple], optional):
        Lista de tuplas, cada tupla es un join, que se debe anyadir a la 
        consulta. Cada tupla, consta de 4 posiciones:
          - Tipo de join (str):
            Tipo  de join a anadir a la consulta.

          - Nombre de la tabla (str):
            Nombre de la tabla sobre la que hacer el join.
          
          - Campo tabla original (str):
            Campo de la tabla original por el cual hacer el join.
          
          - Campo tabla join (str):
            Campo de la tabla anyadida por el cual hacer el join.
        Este es un parametro opcional. Su valor por defectos es None.

      where (list[tuple], optional):
        Lista de tuplas, cada tupla es una condicion que se debe anyadir al
        where. Cada tupla consta de cuatro posiciones:
          - Nombre de la tabla (str):
            Tabla sobre la que se comprobara la condicion.

          - Nombre del campo (str):
            Nombre del campo sobre el cual aplicar la condicion.
          
          - Condicion (str):
            Condicion a aplicar sobre el campo, solo se acepta <, > o =.
          
          - Valor de la condicion (str):
            Valor a aplicar con la condicion sobre el campo. Si es una
            cadena de caracteres se deben introducir " o '.
        Este es un parametro opcional. Su valor por defectos es None.
    
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
  query = "UPDATE " # Query a crear


  # Local code
  # ##### Nombre tabla #####
  query += f"{nombre_tabla.upper()}\n"

  # ##### Join #####
  if(join is not None): # Si hay que hacer algun Join
    # Estructura de la tupla de un join
    # Tipo Join (Inner, Left, Right), Nombre Tabla | nombre_campo_tabla |
    # nombre_campo_tabla_join
    for i in range(0, len(join)):
      query += f"\t{join[i][0].upper()} {join[i][1].upper()}\n\t\tON {nombre_tabla.upper()}.{join[i][2].upper()} = {join[i][1].upper()}.{join[i][3].upper()}\n"
      # Por cada join una linea. Tipo de Join nombre_tabla ON 
      # nombre_tabla_original.campo = nombre_tabla.campo
      # Ej INNER JOIN DEPARTAMENTO ON EMPLEADO.DEPARTAMENTO = DEPARTAMENTO.ID
  

  # ##### Set #####
  # Anyadir el set
  query += "\tSET\n"

  # Estructura de la tupla de un set
  # Nombre tabla | nombre campo | valor
  for i in range(0, len(set)): # Incluir todas las condiciones de set
    # Anyadir el set: Ej: SET EMPLEADO.SALARIO = 3500
    query += f"\t\t{set[i][0].upper()}.{set[i][1].upper()} = {set[i][2].upper()}"
    if(i != len(set)-1): # Si no es el ultimo set, anyadir una coma
      query += ","
    
    query += "\n" # Siempre anyadir un salto de linea
  
  ##### Where #####
  query += "\tWHERE\n" # Anyadir el where

  # Estructura de la tupla de un where
  # nombre_tabla | nombre_campo | condicion (<, >, =) | valor |
  for i in range(0, len(where)): # Recorrer la lista de condiciones del where
    # Anyadir el where
    query += f"\t\t{where[i][0].upper()}.{where[i][1].upper()} {where[i][2].upper()} {where[i][3].upper()}"

    if(i != len(where)-1): # Si no es la ultima clausula, anyadir el AND
      query += " AND\n"

    else: # Si el la ultima linea, solo anyadir el salto de linea
        query += "\n"
  
  # Al final de la consulta, anyadir el punto y coma
  query += ";"

  return (0, "Query para generar update escrita", query)


# ######################################################################### #
def query_select(nombre_tabla:str, columnas:list[tuple] = None, join:list[tuple] = None, where:list[tuple] = None, order_by:list[tuple] = None, limit:str = None):
  """
  Crea una query para seleccionar filas de una tabla.

  Es un metodo interno al programa, el usuario nunca lo tocara o modificara.
  Por lo tanto, no se verifica la validez de los parametros introducidos.
  Se asume que siempre son correctos.

  Args:
      nombre_tabla (str): 
        Nombre de la tabla donde se buscaran las filas.

      columnas (list[tuple], optional): 
        Lista de tuplas, cada tupla es una columna de las tablas, que se
        debe anyadir a la consulta, consta de 2 posiciones:
          - Nombre tabla (str):
            Tabla de la que obtener la columna.
          
          - Nombre columna (str):
            Columna a anyadir a la consulta.
        Este es un parametro opcional. Su valor por defecto es None. Si no se
        indica ninguna columna, se seleccionaran todas las posibles, utilizando
        * en la query.

      join (list[tuple], optional):
        Lista de tuplas, cada tupla es un join, que se debe anyadir a la 
        consulta. Cada tupla, consta de 4 posiciones:
          - Tipo de join (str):
            Tipo  de join a anadir a la consulta.

          - Nombre de la tabla (str):
            Nombre de la tabla sobre la que hacer el join.
          
          - Nombre de la tabla del campo situado a la izquierda (str):
            Nombre de la tabla del campo situado a la izquierda

          - Campo tabla situado a la izquierda (str):
            Campo de la tabla de la izquierda por el cual hacer el join.
          
          - Campo tabla join (str):
            Campo de la tabla anyadida por el cual hacer el join.
        Este es un parametro opcional. Su valor por defectos es None.

      where (list[tuple], optional):
        Lista de tuplas, cada tupla es una condicion que se debe anyadir al
        where. Cada tupla consta de cuatro posiciones:
          - Nombre de la tabla (str):
            Tabla sobre la que se comprobara la condicion.

          - Nombre del campo (str):
            Nombre del campo sobre el cual aplicar la condicion.
          
          - Condicion (str):
            Condicion a aplicar sobre el campo, solo se acepta <, > o =.
          
          - Valor de la condicion (str):
            Valor a aplicar con la condicion sobre el campo. Si es una
            cadena de caracteres se deben introducir " o '.
        Este es un parametro opcional. Su valor por defectos es None.

      order_by (list[tuple], optional):
        Lista de tuplas, cada tupla es una columna por la que ordenar el
        resultado de la query. Cada tupla consta de 3 posiciones:
          - Nombre tabla (str):
            Tabla de la que obtener la columna por la que ordenar el resultado.
          
          - Nombre columna (str):
            Columna por la que ordenar el resultado.
          
          - Tipo orden (str):
            Orden Ascencente (ASC) o descendene (DESC).

      limit (str, optional):
        Indica el numero de filas maximo a devolver. Se maneja como una
        cadena de caracteres por simplicidad. Opcional. Valor por defecto
        None.
    
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
  query = "SELECT "


  # Local code
  # ##### Columnas #####
  if(columnas is None): # Si no hay columnas
    query += "*" # Se seleccionan todos los campos
  
  else: # Se han especificado las columnas a incluir
    # Estructurra de la tupla de una columna
    # Nombre tabla | Nombre columna
    for i in range(0, len(columnas)): # Recorrer las tuplas que contienen las 
      # columnas.
      query += f"{columnas[i][0].upper()}.{columnas[i][1].upper()}" # Nombre_campo.
      # Nombre_columna
      
      if(i != len(columnas)-1): # Si no es la ultima columna, separar por una 
        # coma y un espacio en blanco
        query += ", "

      else: # Si es la ultima columna, salto de linea
        query += "\n"
  

  # ##### Nombre tabla #####
  query += f"\tFROM {nombre_tabla.upper()}\n"

  # ##### Join #####
  if(join is not None): # Si hay que hacer algun Join
    # Estructura de la tupla de un join
    # Tipo Join (Inner, Left, Right), Nombre Tabla | nombre_campo_tabla |
    # nombre_campo_tabla_join
    for i in range(0, len(join)):
      query += f"\t\t{join[i][0].upper()} {join[i][1].upper()}\n\t\t\tON {join[i][2].upper()}.{join[i][3].upper()} = {join[i][1].upper()}.{join[i][4].upper()}\n"
      # Por cada join una linea. Tipo de Join nombre_tabla ON 
      # nombre_tabla_original.campo = nombre_tabla.campo
      # Ej INNER JOIN DEPARTAMENTO ON EMPLEADO.DEPARTAMENTO = DEPARTAMENTO.ID 
  

    ##### Where #####
    query += "\tWHERE\n" # Anyadir el where

    # Estructura de la tupla de un where
    # nombre_tabla | nombre_campo | condicion (<, >, =) | valor |
    for i in range(0, len(where)): # Recorrer la lista de condiciones del where
      # Anyadir el where
      query += f"\t\t{where[i][0].upper()}.{where[i][1].upper()} {where[i][2].upper()} {where[i][3].upper()}"

      if(i != len(where)-1): # Si no es la ultima clausula, anyadir el AND
        query += " AND\n"
      
      else: # Si el la ultima linea, solo anyadir el salto de linea
        query += "\n"
    
    # ##### Order By #####
    # Estructura de una tupla de order by
    # Nombre Tabla | Nombre columna | ASCendente o DESCendente
    if(order_by is not None): # Si la query tiene que ordenarse de alguna manera
      # Escribir Order By
      query += "\tORDER BY\n"
      for i in range(0, len(order_by)):
        query += f"\t\t{order_by[i][0].upper()}.{order_by[i][1].upper()} {order_by[i][2].upper()}"

        if(i != len(order_by)-1): # Si no es la ultima columna por la que 
          # ordenar, anyadir una coma
          query += ","

        # Siempre al final de cada linea de order by anyadir un salto de linea
        query += "\n"
    
    # ##### Limit #####
    if(limit is not None):
      query += f"\tLIMIT {limit}"
    
    # Al final de la query, siempre anyadir punto y coma
    query += ";"

  return (0, "Query para generar select escrita", query)