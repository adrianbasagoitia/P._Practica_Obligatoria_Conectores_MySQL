# ############################################################################ #
#                                   IMPORT 
# ############################################################################ #
import utilidades
import query
import base_datos
import datetime

# ################################ Methods ################################ #
def menu_empleado(conexion, parametros_conexion:tuple):
  """
  Submenu del programa, concerniente a los empleados.

  Imprime por salida estandar (Consola) el menu principal del programa, y pide
  al usuario la introduccion por entrada estandar (Teclado) del indice de la
  opcion que desea realizar. 
    - En caso de ser correcta, se redirige al menu correspondiente. 
    - Por el contrario, si es una opcion erronea se informa al 
  usuario del error.

  Para salir del submenu, y volver al menu principal, se pide al usuario 
  confirmar la accion.
  """
  # Local variables
  entrada:str = None # Caracteres introducidos por el usuario a traves de 
  # entrada estandar (Teclado).
  salir:bool = False # Almacena si el usuario quiere salir del programa (True)
  # o continuar con la ejecucion (False).
  retorno_otros:tuple = None # Tupla que contendra el valor de retorno de 
  # otros metodos.

  # Local code
  while(not salir): # Iterar mientras que el usuario no confirme la salida
    # Limpiar valor
    retorno_otros = None

    # Imprimir menu
    print("\n"*2+"+"*60)
    print("Proyectos:")
    print("1 - Alta empleado.")
    print("2 - Baja empleado.")
    print("3 - Buscar empleado.")
    print("4 - Modificar empleado.")
    print("5 - Mostrar empleado.")
    print("0 - Salir")

    # Pedir opcion a realizar al usuario
    entrada = input("\nIntroduzca el numero de la opcion que desea realizar: ")

    # Filtrar opciones
    if(entrada == "0"): # Salir
      salir = utilidades.pedir_confirmacion("\n¿Quiere salir del programa?")

      if(salir): # Si la salida esta confirmada
        print("\nAdios.")
      else: # Si la salida no se confirma
        print("\nSalida cancelada.")
    

    elif(entrada == "1"): # Alta empleado
      retorno_otros = alta_empleado(conexion, parametros_conexion)
      print(retorno_otros[1])
      

    elif(entrada == "2"): # Baja empleado
      pass#baja_proyecto(conexion, parametros_conexion)
    

    elif(entrada == "3"): # Buscar empleado
      #retorno_otros = buscar_empleado(conexion, parametros_conexion)
      # Imprimir siempre el mensaje
      print(retorno_otros[1])

      # Actualizar el valor de la conexion
      conexion = retorno_otros[2]

      if(retorno_otros[0] == 0 and len(retorno_otros) == 4): # Ejecucion 
        # correcta y con resultado
        #print(proyecto_a_texto(retorno_otros[3]))
        pass

    elif(entrada == "4"): # Modificar empleado
      pass#modificar_empleado(conexion, parametros_conexion)
    

    elif(entrada == "5"): # Mostrar empleados
      print("5 - Mostrar empleado.")
      retorno_otros = mostrar_empleado(conexion, parametros_conexion)
      print(retorno_otros[1])

      # Hay proyectos que imprimir
      if(retorno_otros[0] == 0 and len(retorno_otros) == 4):
        print(retorno_otros[3])

    else: # Opcion erronea
      print(f"\nERROR. La opcion \"{entrada}\" no es una entrada valida.")
  
  return conexion

# ######################################################################### #
def peticiones_campos(indice_peticion:int):
  """
  Devuelve cadenas de caracteres conteniendo mensaje de peticion de campos
  al usuario.

  Dado un indice, comprueba si esta dentro de los limites de la lista de 
  mensajes, y si es asi, lo devuelve. En caso contrario, devuelve un mensaje
  de error.

  Args:
      indice_peticion (int): 
        Indice de la lista conteniendo el mensaje requerido.
  
  Returns:
      tuple: dos o tres posiciones:
        - codigo de retorno (int): 
          0 en caso de ejecucion correcta, -1 en cualquier otro caso.

        - mensaje de ejecucion (str):
          Mensaje para el usuario informando del
          retorno de la ejecucion del metodo.

        - mensaje_peticion (str, optional):
          Mensaje de peticion de un campo al usuario. 
  """  
  # Local variables
  peticiones:list[str] = None # Lista conteniendo cadenas de caracteres para
    # pedir campos al usuario. 

  # Local code
  peticiones = [
    "\nIntroduzca el nombre completo del empleado. No puede haber dos empleados con el mismo nombre e email \n[Letras del alfabeto espanyol, espacios en blanco y los siguientes \ncaracteres \".,;&-\"][Longitud 1 a 120 caracteres]",

    "\nIntroduzca el email del empleado, el dominio ha de ser @MYSQL seguido de .com .No puede haber dos empleados con el mismo nombre e email[Letras del alfabeto espanyol,\nnumeros y los siguientes caracteres \"._\"]\n[Longitud 1 a 80 caracteres]",

    "\nIntroduzca el salario del empleado. El salario por defecto es de 1134€. [Valor minimo: 1134.00, Valor maximo: 999999999.99]",

    "\nIntroduzca el cargo del empleado.\n[Letras del alfabeto espanyol, espacios en blanco y los siguientes \ncaracteres \".,;&-_\"][Longitud 1 a 60 caracteres] ",

    "\nIntroduzca el id del departamento.El id ha de ser numerico "
  ]

  if(indice_peticion >= 0 and indice_peticion < len(peticiones)): # El indice es 
    # correcto
    retorno = (0, "Mensaje de peticion de campo obtenido", peticiones[indice_peticion])

  else: # El indice es incorrecto
    retorno = (-1, "El indice proporcionado no es valido.")
  
  return retorno

# ######################################################################### #
def alta_empleado(conexion, parametros_conexion:tuple):
  """
  Crea un nuevo empleado en la base de datos.

  Pide los campos al usuario, posteriormente escribe la query para insertar
  el nuevo empleado en la base de datos y manda ejecutarla.

  El resultado devuelto por este metodo, es el resultado de ejecutar la query.
  
  No se comprueba la duplicidad de nombres de empleados, eso se comprueba en la
  base de datos.

  Args:
      conexion (Connection): 
        Conexion sobre el servidor de la base de datos.

      parametros_conexion (tuple):
        Tupla con 4 posiciones: usuario, contrasenya, puerto, nombre base datos.

  Returns:
      tuple: dos posiciones:
        - codigo de resultado (int): 
          0 en caso de ejecucion correcta, -1 en cualquier otro caso.
        - mensaje de ejecucion (str): 
          Mensaje para el usuario informando del resultado de la ejecucion 
          del metodo.
  """  
  # Local variables
  nombre_campos:list[str] = ["empleado_nombre", "empleado_correo", "empleado_salario"]
  campos:list[str] = [] # Lista de los campos validos proporcionados por el 
    # usuario.
  continuar:bool = True # Continuar con la ejecucion del bucle
  indice:int = 0 # Indice para iterar en un bucle
  retorno_otros:tuple = None # Tupla conteniendo el retorno de otros metodos
  retorno:tuple # Tupla conteniendo la informacion necesaria para el 
  # retorno del metodo. 3 posiciones: Codigo ejecucion (0 - Correcta;
  # -1 incorrecta), mensaje de resultado de ejecucion, conexion.


  # Local code
  # Pedir los campos
  while(indice < len(nombre_campos) and continuar):
    retorno_otros = utilidades.pedir_campo(peticiones_campos(indice)[2], nombre_campos[indice])


    if(retorno_otros[0] == -1):
      retorno = (-1, retorno_otros[1], conexion) # Construir retorno de ejecucion
      
      # Terminar la ejecucion del bucle
      continuar = False
    
    else: # Ejecucion correcta 
      campos.append(retorno_otros[2]) # anyadir a la lista de campos validos
      indice += 1 # Pedir el siguiente campo
  
  if(continuar): # Todos los campos pedidos son validos y han sido anyadidos
    # Hacer la query
    retorno_otros = query.query_insert_into("empleado", ["nombre", "correo_electronico", "fecha_contratacion", "salario"], [(f"\"{campos[0]}\"", f"\"{campos[1]}\"", "NOW()", f"\"{campos[2]}\"")])


    # Ejecutar la instruccion
    retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])
    
    # Actualizar el valor de la conexion
    conexion = retorno_otros[2]

    if(retorno_otros[0] == 0): # Insercion correcta
      retorno = (0, "\nEmpleado insertado en la base de datos.", conexion)
    
    else: # Insercion erronea
      retorno = (-1, retorno_otros[1], conexion) # Devolver el menasje de error devuelto
        # de la ejecucion de la instruccion
  
  return retorno

# ######################################################################### #
def borrar_empleado(conexion, parametros_conexion):
  """
  Borra un empleado de la base de datos.

  Busca un proyecto por nombre. Si existe, pide confirmacion para borrarlo.
  En caso de obtenerla, intenta borrarlo de la base de datos.

  Args:
      conexion (Connection): Conexion sobre el servidor de la base de datos.
      parametros_conexion (tuple): Tupla con 4 posiciones: usuario, contrasenya, puerto, nombre base datos.
  """  
  # Local variables
  retorno_otros:tuple = None # Retorno de ejecucion de otros metodos
  retorno:tuple = None # Tupla conteniendo la informacion necesaria para el 
  # retorno del metodo. 3 o 4 posiciones: Codigo ejecucion (0 - Correcta;
  # -1 incorrecta), mensaje de resultado de ejecucion, conexion, 
  # proyecto_pedido (opcional).
  proyecto:str = None # Cadena de caracteres con el empleado a texto.
  confirmado:bool = False # El usuario quiere borrar el empleado.

  # Local code
  # Mandar buscar el proyecto
  retorno_otros = buscar_empleado(conexion, parametros_conexion)

  if(retorno_otros == -1): # Error en el buscar. Devolver error
    retorno = (-1, retorno_otros[1], conexion)

  else: # Ejecucion correcta
    # En cualquier caso, imprimir el mensaje de resultado
    print(retorno_otros[1])

    if(len(retorno_otros) != 4): # No hay proyecto
      retorno = (0, retorno_otros[1], conexion)
    
    else: # Hay proyecto
      # Obtener el proyecto formateado
      proyecto_a_texto = proyecto_a_texto(retorno_otros[3])

      # Imprimir el proyecto
      print(proyecto_a_texto)

      # Pedir confirmacion
      confirmado = utilidades.pedir_confirmacion("\n¿Quiere borrar el empleado?")

      if(not confirmado): # El usuario no quiere borrar el proyecto
        retorno = (-1, "\nBorrado abortado.", conexion)
      
      else:
        # Crear la query para borrar
        retorno_otros = query.query_delete_from("empleado", [("empleado", "nombre", "=", f"\"{retorno_otros[3][0]}\""),("empleado", "correo_electronico", "=", f"\"{retorno_otros[3][0]}\"")])

        # Ejecutar la query sobre la base de datos
        retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])
        # Actualizar el valor de la conexion
        conexion = retorno_otros[2]

        if(retorno_otros[0] == 0): # Borrado correcto
          retorno = (0, "\nProyecto borrado de la base de datos", conexion)
        
        else: # Borrado erroneo
          retorno = (-1, retorno_otros[1], conexion)
  
  return retorno
# ######################################################################### #
def buscar_empleado(conexion, parametros_conexion:tuple):
  """
  Busca un proyecto en la base de datos.

  Dado el nombre del proyecto, escribe la query y la ejecuta.

  El resultado puede ser obtener un proyecto o ninguno, dado que el nombre
  del proyecto es unico en la base de datos.

  Args:
      conn (Connection): 
        Conexion sobre el servidor de la base de datos.

      parametros_conexion (tuple):
        Tupla con 4 posiciones: usuario, contrasenya, puerto, nombre base datos.

  Returns:
      tuple: dos o tres posiciones:
        - codigo de resultado (int): 
          0 en caso de ejecucion correcta, -1 en cualquier otro caso.
        - mensaje de ejecucion (str): 
          Mensaje para el usuario informando del resultado de la ejecucion 
          del metodo.
        - proyecto_resultado (tuple):
          Tupla conteniendo el empleado buscado. Contiene el nombre del 
          empleado, su correo, la fecha de contratacion,el departamento al que pertenece el empleado,
          el cargo del empleado y el sueldo del empleado.
  """  
  # Local variables
  retorno_otros:tuple = None # Retorno de ejecucion de otros metodos
  retorno:tuple = None # Tupla conteniendo la informacion necesaria para el 
  # retorno del metodo. 3 o 4 posiciones: Codigo ejecucion (0 - Correcta;
  # -1 incorrecta), mensaje de resultado de ejecucion, conexion, 
  # empleado_pedido (opcional).


  # Local code
  # Pedir el nombre al usuario
  retorno_otros = utilidades.pedir_campo(peticiones_campos(0)[2], "proyecto_nombre")

  if(retorno_otros[0] == -1): # Peticion erronea
      retorno = (-1, retorno_otros[1], conexion) # Construir retorno de ejecucion
  
  else: # Campo valido
    retorno_otros = query.query_select("proyecto", [("proyecto", "nombre"), ("proyecto", "descripcion"), ("proyecto", "fecha_inicio"), ("proyecto", "fecha_fin"), ("departamento", "nombre"), ("empleado", "nombre")], [("left join", "departamento", "departamento", "id"), ("left join", "empleado", "responsable", "id")], [("proyecto", "nombre", "=", f"\"{retorno_otros[2]}\"")])

    # Ejecutar la query
    retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])
    # Actualizar el valor de la conexion
    conexion = retorno_otros[2]

    if(retorno_otros[0] == -1): # Ejecucion erronea
      retorno = (-1, retorno_otros[1], conexion)
    
    else: # Ejecucion correcta
      # Obtener el resultado y comprobar si hay proyectos encontrados
      if(len(retorno_otros) != 4): # Si NO hay proyectos
        retorno = (0, "\nNo hay proyectos con el nombre proporcionado.", conexion)
      
      else: # Hay un proyecto con el nombre proporcionado. NO puede haber mas
        retorno = (0, "\nUn proyecto encontrado", conexion, retorno_otros[3][0])
    
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
        Tupla obtenida de una query SELECT a la base de datos. Consta de 6
        posiciones: Nombre, Correo, Salario, Fecha Contratacion, Departamento
        y Cargo.
  
  Returns:
      str:
        Cadena de caracteres con la informacion del proyecto formateada, lista
        para imprimir.
  """  
  # Local variables
  pro_texto:str = "" # Cadena de texto conteniendo el proyecto

  # Local code
  pro_texto += "\nEmpleado:\n"
  pro_texto += f"\tNombre: {empleado[0]}\n"
  pro_texto += f"\tCorreo: {empleado[1]}\n"
  pro_texto += f"\tSalario: {empleado[2]}\n"
  # Cambiar fechas de dormato americano a europeo
  pro_texto += f"\tFecha de contratación: {empleado[3].strftime("%d-%m-%Y")}\n"
  if(empleado[4] is None or empleado[4] == ""): # El departamento es nulo 
    # vacia.
    pro_texto += f"\tDepartamento: Sin departamento.\n"

  else: # Hay departamento
    queryT = query.query_select("departamento", [("departamento", "nombre")],[("departamento", "id", "=", f"\"{empleado[4]}\"")])
  

  # Ejecutar la query
    departamento = base_datos.ejecutar_instruccion(conexion, parametros_conexion, queryT[2])

     # Actualizar el valor de la conexion
    conexion = departamento[2]
    pro_texto += f"\tDepartamento: {empleado[4]}\n"

  if(empleado[5] is None): # No hay cargo asignado
    pro_texto += f"\tCargo: Sin cargo.\n"
  
  else: # Hay cargo asignado
    pro_texto += f"\tCargo: {empleado[5]}\n"
  
  return pro_texto

# ######################################################################### #
def mostrar_empleado(conexion, parametros_conexion:tuple):
  """
  Crea una cadena de caracteres con la informacion de todos los empleados.

  Realiza una query a la base de datos, y obtiene todos los empleados 
  almacenados. Posteriormente uno a uno va pidiendo que se escriban en una 
  cadena de caracteres incluyendo los empleados que trabajan en los mismos.

  Si no hay ningun proyecto, devuelve un mensaje informativo.

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
  # proyectos en texto (opcional).
  empleados_lista:list[tuple] = None # Lista para almacenar los empleados leidos
    # de la base de datos.
  empleados:str = "" # Contiene la informacion de los empleados en una cadena 
    # de caracteres.
  errores:int = 0 # Numero de empleados cuya lectura ha sido erronea.


  # Local code
  # Obtener la query para seleccionar todos los empleados
  retorno_otros = query.query_select("empleado", [("empleado", "nombre"), ("empleado", "correo_electronico"), ("empleado", "salario"), ("empleado", "fecha_contratacion"), ("empleado", "departamento"), ("empleado", "cargo")],[("left join", "departamento", "empleado", "departamento", "id")])

  # Buscar todos los empleado
  retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])

  # Actualizar el valor de la conexion
  conexion = retorno_otros[2]

  if(retorno_otros[0] != 0): # Ejecucion erronea
    retorno = (-1, retorno_otros[1], conexion)
  
  else: # Se ha podido hacer la query
    if(len(retorno_otros) == 3): # No hay proyectos
      retorno = (0, "\nNo hay empleados que mostrar.", conexion)
    
    else: # Hay empleados que mostrar
      # Guardar los empleado en una variable
      empleados_lista = retorno_otros[3]

      # Recorrer la lista e ir llamando a empleado_a_texto
      for i in empleados_lista:
        retorno_otros = empleado_a_texto(conexion, parametros_conexion,i)

        # Actualizar el valor de la conexion
        conexion = retorno_otros[2]

        if(retorno_otros[0] == 0): # Proyecto a texto creado correctamente
          empleados += retorno_otros[3]
        
        else: # Lectura erronea, almacenar el numero
          errores += 1
      
      # Al acabar el for, si hay algun proyecto erroneo, anyadir al final el 
      # mensaje de error.
      if(errores != 0):
        empleados += f"\nSe ha producio un error en la lectura de {errores} empleado/s."
      
      retorno = (0, "Empleados escritos en texto", conexion, empleados)
  
  return retorno