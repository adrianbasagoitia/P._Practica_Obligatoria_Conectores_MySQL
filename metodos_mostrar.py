# ############################################################################ #
#                                   IMPORT 
# ############################################################################ #
import query
import base_datos
# ######################################################################### #
def departamento_a_texto(conexion, parametros_conexion:tuple,departamento:tuple):
  """
  Escribe los datos de un departamento a una cadena de caracteres.

  Dada una tupla obtenida de una query a la base de datos, escribe en una
  cadena de caracteres la informacion del proyecto formateada y legible para
  el usuario.

  En caso de que alguno de los campos tenga valor vacio o NULL, se cambia a un
  valor "amigable" para el usuario como: "Sin cargo" o "Sin departamento."

  Args:
      conn (Connection): 
        Conexion sobre el servidor de la base de datos.

      parametros_conexion (tuple):
        Tupla con 4 posiciones: usuario, contrasenya, puerto, nombre base datos.
      empleado (tuple):
        Tupla obtenida de una query SELECT a la base de datos. Consta de 4
        posiciones: Nombre, Descripcion, Responsable e id.
  
  Returns:
      str:
        Cadena de caracteres con la informacion del departamento formateada, lista
        para imprimir.
  """  
  # Local variables
  pro_texto:str = "" # Cadena de texto conteniendo el departamento
  queryT:tuple = None # Query para obtener los proyectos
    # tabla empleado_proyecto
  # Local code
  #Anyadimos a la cadena los campos
  pro_texto += f"\tNombre: {departamento[0]}\n"
  pro_texto += f"\tCorreo: {departamento[1]}\n"
  if(departamento[2] is None or departamento[2] == ""): # El responsable es nulo 
    # vacia.
    pro_texto += f"\tResponsable: Sin Responsable.\n"

  else: # Hay responsable
      pro_texto += f"\tResponsable: {departamento[2]}\n"
  pro_texto+= "\n"
  return pro_texto

# ######################################################################### #
def mostrar_departamento(conexion, parametros_conexion:tuple,id:bool=False):
  """
  Crea una cadena de caracteres con la informacion de todos los departamentos.

  Realiza una query a la base de datos, y obtiene todos los departamentos 
  almacenados. Posteriormente uno a uno va pidiendo que se escriban en una 
  cadena de caracteres incluyendo los empleados que trabajan en los mismos.

  Si no hay ningun departamento, devuelve un mensaje informativo.

  Args:
      conexion (Connection): 
        Conexion sobre el servidor de la base de datos.

      parametros_conexion (tuple):
        Tupla con 4 posiciones: usuario, contrasenya, puerto, nombre base datos.
    
        id (bool):booleano para indicar si se quiere mostrar o no el id del departamento

  Returns:
      tuple: tres o cuatro posiciones:
        - codigo de resultado (int): 
          0 en caso de ejecucion correcta, -1 en cualquier otro caso.
        - mensaje de ejecucion (str): 
          Mensaje para el usuario informando del resultado de la ejecucion 
          del metodo.
        - conexion (Connection):
          Conexion actual a la base de datos.
        - proyectos (str, optional):
          Cadena de caracteres, conteniendo la informacion de todos los 
          proyectos y los empleados que trabajan en ellos. Es opcional.
  """  
  # Local variables
  retorno_otros:tuple = None # Retorno de ejecucion de otros metodos
  retorno:tuple = None # Tupla conteniendo la informacion necesaria para el 
  # retorno del metodo. 3 o 4 posiciones: Codigo ejecucion (0 - Correcta;
  # -1 incorrecta), mensaje de resultado de ejecucion, conexion, 
  # empleado en texto (opcional).
  departamentos_lista:list[tuple] = None # Lista para almacenar los departamentos leidos
    # de la base de datos.
  departamentos:str = "" # Contiene la informacion de los departamentos en una cadena 
    # de caracteres.
  errores:int = 0 # Numero de departamentos cuya lectura ha sido erronea.


  # Local code
  # Obtener la query para seleccionar todos los departamentos
  retorno_otros = query.query_select("departamento", [("departamento", "nombre"), ("departamento", "descripcion"), ("empleado", "nombre"),("departamento", "id")],[("left join", "empleado", "departamento", "responsable", "id")])

  # Buscar todos los empleado
  retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])

  # Actualizar el valor de la conexion
  conexion = retorno_otros[2]

  if(retorno_otros[0] != 0): # Ejecucion erronea
    retorno = (-1, retorno_otros[1], conexion)
  
  else: # Se ha podido hacer la query
    if(len(retorno_otros) == 3): # No hay departamentos
      retorno = (0, "\nNo hay departamentos que mostrar.", conexion)
    
    else: # Hay departamentos que mostrar
      # Guardar los departamentos en una variable
      departamentos_lista = retorno_otros[3]

      # Recorrer la lista e ir llamando a departamentos_lista
      for i in departamentos_lista:
        if(id==True):#si se quiere mostrar el id
          departamentos+=f"\nDepartamento: {i[3]}"
        else:
          departamentos+=f"\nDepartamento: "
        retorno_otros = departamento_a_texto(conexion, parametros_conexion,i)
        departamentos += retorno_otros
      
      # Al acabar el for, si hay algun departamento erroneo, anyadir al final el 
      # mensaje de error.
      if(errores != 0):
        departamentos += f"\nSe ha producio un error en la lectura de {errores} departamento/s."
      
      retorno = (0, "Departamentos escritos en texto", conexion, departamentos)
  
  return retorno
# ######################################################################### #
def empleado_a_texto(conexion, parametros_conexion:tuple,empleado:tuple):
  """
  Escribe los datos de un empleado a una cadena de caracteres.

  Dada una tupla obtenida de una query a la base de datos, escribe en una
  cadena de caracteres la informacion del proyecto formateada y legible para
  el usuario.

  En caso de que alguno de los campos tenga valor vacio o NULL, se cambia a un
  valor "amigable" para el usuario como: "Sin cargo" o "Sin departamento."

  Args:
      conn (Connection): 
        Conexion sobre el servidor de la base de datos.

      parametros_conexion (tuple):
        Tupla con 4 posiciones: usuario, contrasenya, puerto, nombre base datos.
      empleado (tuple):
        Tupla obtenida de una query SELECT a la base de datos. Consta de 7
        posiciones: Nombre, Correo, Salario, Fecha Contratacion, Departamento
        , Cargo e id.
  
  Returns:
      str:
        Cadena de caracteres con la informacion del empleado formateada, lista
        para imprimir.
  """  
  # Local variables
  pro_texto:str = "" # Cadena de texto conteniendo el empleado
  queryT:tuple = None # Query para obtener los proyectos
  proyectos:tuple = None # Retorno de la consulta a la base de datos sobre la 
    # tabla empleado_proyecto
  # Local code
  #Anyadimos a la cadena los campos
  pro_texto += f"\tNombre: {empleado[0]}\n"
  pro_texto += f"\tCorreo: {empleado[1]}\n"
  pro_texto += f"\tSalario: {empleado[2]}\n"
  # Cambiar fechas de dormato americano a europeo
  pro_texto += f"\tFecha de contratación: {empleado[3].strftime("%d-%m-%Y")}\n"
  if(empleado[4] is None or empleado[4] == ""): # El departamento es nulo 
    # vacia.
    pro_texto += f"\tDepartamento: Sin departamento.\n"

  else: # Hay departamento
    pro_texto += f"\tDepartamento: {empleado[4]}\n"

  if(empleado[5] is None): # No hay cargo asignado
    pro_texto += f"\tCargo: Sin cargo.\n"
  
  else: # Hay cargo asignado
    pro_texto += f"\tCargo: {empleado[5]}\n"
  #hazemos la consulta para sacar los proyectos en los que trabaja el empleado
  # Crear la query
  queryT = query.query_select("empleado", [("proyecto", "nombre")], [("left join", "empleado_proyecto", "empleado", "id", "id_empleado"), ("left join", "proyecto", "empleado_proyecto", "id_proyecto", "id")], [("empleado", "id", "=", f"{empleado[6]}")])
  # Ejecutar la query
  proyectos = base_datos.ejecutar_instruccion(conexion, parametros_conexion, queryT[2])
  # Actualizar el valor de la conexion
  conexion = proyectos[2]
  if(proyectos[0] != 0): # Error al ejecutar
    pro_texto+="\nError al leer los proyectos de la base de datos."
  
  else: # Se han leido correctamente
    # Si no hay empleados
    if(proyectos[3] == ((None,),)):
      pro_texto+= "\n \tNo esta trabajando en ningun proyecto .\n"
    
    else: # Si hay proyectos
      pro_texto+="\n \tProyectos: \n"
      for proyecto in proyectos[3]:
        pro_texto += f"\t Nombre: {proyecto}\n"

      pro_texto+= "\n"
  return pro_texto

# ######################################################################### #
def mostrar_empleado(conexion, parametros_conexion:tuple):
  """
  Crea una cadena de caracteres con la informacion de todos los empleados.

  Realiza una query a la base de datos, y obtiene todos los empleados 
  almacenados. Posteriormente uno a uno va pidiendo que se escriban en una 
  cadena de caracteres incluyendo los empleados que trabajan en los mismos.

  Si no hay ningun empleado, devuelve un mensaje informativo.

  Args:
      conexion (Connection): 
        Conexion sobre el servidor de la base de datos.

      parametros_conexion (tuple):
        Tupla con 4 posiciones: usuario, contrasenya, puerto, nombre base datos.

  Returns:
      tuple: tres o cuatro posiciones:
        - codigo de resultado (int): 
          0 en caso de ejecucion correcta, -1 en cualquier otro caso.
        - mensaje de ejecucion (str): 
          Mensaje para el usuario informando del resultado de la ejecucion 
          del metodo.
        - conexion (Connection):
          Conexion actual a la base de datos.
        - proyectos (str, optional):
          Cadena de caracteres, conteniendo la informacion de todos los 
          proyectos y los empleados que trabajan en ellos. Es opcional.
  """  
  # Local variables
  retorno_otros:tuple = None # Retorno de ejecucion de otros metodos
  retorno:tuple = None # Tupla conteniendo la informacion necesaria para el 
  # retorno del metodo. 3 o 4 posiciones: Codigo ejecucion (0 - Correcta;
  # -1 incorrecta), mensaje de resultado de ejecucion, conexion, 
  # empleado en texto (opcional).
  empleados_lista:list[tuple] = None # Lista para almacenar los empleados leidos
    # de la base de datos.
  empleados:str = "" # Contiene la informacion de los empleados en una cadena 
    # de caracteres.
  errores:int = 0 # Numero de empleados cuya lectura ha sido erronea.


  # Local code
  # Obtener la query para seleccionar todos los empleados
  retorno_otros = query.query_select("empleado", [("empleado", "nombre"), ("empleado", "correo_electronico"), ("empleado", "salario"), ("empleado", "fecha_contratacion"), ("departamento", "nombre"), ("empleado", "cargo"),("empleado", "id")],[("left join", "departamento", "empleado", "departamento", "id")])

  # Buscar todos los empleado
  retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])

  # Actualizar el valor de la conexion
  conexion = retorno_otros[2]

  if(retorno_otros[0] != 0): # Ejecucion erronea
    retorno = (-1, retorno_otros[1], conexion)
  
  else: # Se ha podido hacer la query
    if(len(retorno_otros) == 3): # No hay empleados
      retorno = (0, "\nNo hay empleados que mostrar.", conexion)
    
    else: # Hay empleados que mostrar
      # Guardar los empleado en una variable
      empleados_lista = retorno_otros[3]

      # Recorrer la lista e ir llamando a empleado_a_texto
      for i in empleados_lista:
        empleados+=f"\nEmpleado: \n"
        retorno_otros = empleado_a_texto(conexion, parametros_conexion,i)
        empleados += retorno_otros
      
      # Al acabar el for, si hay algun empleado erroneo, anyadir al final el 
      # mensaje de error.
      if(errores != 0):
        empleados += f"\nSe ha producio un error en la lectura de {errores} empleado/s."
      
      retorno = (0, "Empleados escritos en texto", conexion, empleados)
  
  return retorno
