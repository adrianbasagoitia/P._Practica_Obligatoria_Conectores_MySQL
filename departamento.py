# ############################################################################ #
#                                   IMPORT 
# ############################################################################ #
import utilidades
import query
import base_datos
import metodos_mostrar
import datetime

# ################################ Methods ################################ #
def menu_departamento(conexion, parametros_conexion:tuple):
  """
  Submenu del programa, concerniente a los departamentos.

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
  empleados_lista:list[tuple] = None # Lista para almacenar los empleados leidos
    # de la base de datos.
  empleados:str = "" # Contiene la informacion de los empleados en una cadena 
    # de caracteres.
  # Local code
  while(not salir): # Iterar mientras que el usuario no confirme la salida
    # Limpiar valor
    retorno_otros = None

    # Imprimir menu
    print("\n"*2+"+"*60)
    print("Departamento:")
    print("1 - Alta departamento.")
    print("2 - Baja departamento.")
    print("3 - Buscar departamento.")
    print("4 - Modificar departamento.")
    print("5 - Mostrar departamento.")
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
    

    elif(entrada == "1"): # Alta departamento
      retorno_otros = alta_departamento(conexion, parametros_conexion)
      

    elif(entrada == "2"): # Baja departamento
      print(borrar_departamento(conexion, parametros_conexion)[1])

    elif(entrada == "3"): # Buscar departamento
      print("\n3 - Buscar departamento.")
      retorno_otros = buscar_departamento(conexion, parametros_conexion)
      # Imprimir siempre el mensaje

      print(retorno_otros[1])

      # Actualizar el valor de la conexion
      conexion = retorno_otros[2]

      if(retorno_otros[0] == 0 and len(retorno_otros) == 4): # Ejecucion 
        empleados_lista=retorno_otros[3]
        # correcta y con resultado
        for i in empleados_lista:
          retorno_otros = metodos_mostrar.departamento_a_texto(conexion, parametros_conexion,i)
          empleados += retorno_otros
        print(empleados)

    elif(entrada == "4"): # Modificar departamento
      modificar_departamento(conexion, parametros_conexion)
    

    elif(entrada == "5"): # Mostrar departamentos
      print("5 - Mostrar departamento.")
      retorno_otros = metodos_mostrar.mostrar_departamento(conexion, parametros_conexion)
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
    "\nIntroduzca el nombre completo del departamento. No puede haber dos departamento con el mismo nombre\n[Letras del alfabeto espanyol, \nnumeros, espacios en blanco y los siguientes \ncaracteres \".,;&-\"][Longitud 1 a 60 caracteres]",

    "\nIntroduzca la descripcion del departamento[Letras del alfabeto espanyol,\nnumeros y los siguientes caracteres \"._\"]\n[Longitud 1 a 255 caracteres]",

    "\nIntroduzca el id del empleado.El id ha de ser numerico "
  ]

  if(indice_peticion >= 0 and indice_peticion < len(peticiones)): # El indice es 
    # correcto
    retorno = (0, "Mensaje de peticion de campo obtenido", peticiones[indice_peticion])

  else: # El indice es incorrecto
    retorno = (-1, "El indice proporcionado no es valido.")
  
  return retorno

# ######################################################################### #
def alta_departamento(conexion, parametros_conexion:tuple):
  """
  Crea un nuevo departamento en la base de datos.

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
  nombre_campos:list[str] = ["departamento_nombre", "departamento_descripcion"]
  campos:list[str] = [] # Lista de los campos validos proporcionados por el 
    # usuario.
  continuar:bool = True # Continuar con la ejecucion del bucle
  indice:int = 0 # Indice para iterar en un bucle
  retorno_otros:tuple = None # Tupla conteniendo el retorno de otros metodos
  retorno:tuple # Tupla conteniendo la informacion necesaria para el 
  # retorno del metodo. 3 posiciones: Codigo ejecucion (0 - Correcta;
  # -1 incorrecta), mensaje de resultado de ejecucion, conexion.
  repetir:bool=True#booleano para el bucle para anyadir empleados 

  # Local code
  # Pedir los campos
  while(repetir):
    campos:list[str] = []
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
      retorno_otros = query.query_insert_into("departamento", ["nombre", "descripcion"], [(f"\"{campos[0]}\"", f"\"{campos[1]}\"")])


      # Ejecutar la instruccion
      retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])
      
      # Actualizar el valor de la conexion
      conexion = retorno_otros[2]

      if(retorno_otros[0] == 0): # Insercion correcta
        print("\nDepartamento insertado en la base de datos.")
      
      else: # Insercion erronea
        print(retorno_otros[1]) # Devolver el menasje de error devuelto
          # de la ejecucion de la instruccion
    repetir=utilidades.pedir_confirmacion("\nQuiere anyadir otro departamento?")
    indice=0
    continuar = True

# ######################################################################### #
def borrar_departamento(conexion, parametros_conexion):
  """
  Borra un empleado de la base de datos.

  Busca un empleado por nombre . Si existe, pide confirmacion para borrarlo.
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
  departamentos_lista:list[tuple] = None # Lista para almacenar los empleados leidos
    # de la base de datos.
  departamento:str = "" # Contiene la informacion de los empleados en una cadena 
  borrar:str=""#nombre del departamento a borrar

  # Local code
  print("\n2 - Borrar departamento.")
  # Mandar buscar el empleado
  retorno_otros = buscar_departamento(conexion, parametros_conexion)

  if(retorno_otros == -1): # Error en el buscar. Devolver error
    retorno = (-1, retorno_otros[1], conexion)

  else: # Ejecucion correcta
    # En cualquier caso, imprimir el mensaje de resultado
    print(retorno_otros[1])

    if(len(retorno_otros) != 4): # No hay departamento
      retorno = (0, retorno_otros[1], conexion)
    
    else: # Hay departamento
      departamentos_lista=retorno_otros[3]
        # correcta y con resultado
      for i in departamentos_lista:#lo pasamos a texto los departamentos
          borrar=i[0] #guardamos el valor del nombre del departamento a borrar
          departamento += metodos_mostrar.departamento_a_texto(conexion, parametros_conexion,i)
      print(departamento)#lo mostramos
      #Pedimos confirmacion
      confirmado = utilidades.pedir_confirmacion("\n¿Quiere borrar el departamento?")

      if(not confirmado): # El usuario no quiere borrar el departamento
          retorno = (-1, "\nBorrado abortado.", conexion)
        
      else:
          # Crear la query para borrar
          retorno_otros = query.query_delete_from("departamento", [("departamento", "nombre", "=", f"\"{borrar}\"")])

          # Ejecutar la query sobre la base de datos
          retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])
          # Actualizar el valor de la conexion
          conexion = retorno_otros[2]

          if(retorno_otros[0] == 0): # Borrado correcto
            retorno = (0, "\nDepartamento borrado de la base de datos", conexion)
          
          else: # Borrado erroneo
            retorno = (-1, retorno_otros[1], conexion)
  
  return retorno
# ######################################################################### #
def buscar_departamento(conexion, parametros_conexion:tuple):
  """
  Busca un departamento en la base de datos.

  Dado el nombre del departamento, escribe la query y la ejecuta.

  El resultado puede ser obtener el departamento o ninguno.Ya que el nombre del departamento es unico

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
          Tupla conteniendo el departamento buscado. Contiene el nombre del 
          departamento, su descripcion, su responsable y el id.
  """  
  # Local variables
  retorno_otros:tuple = None # Retorno de ejecucion de otros metodos
  retorno:tuple = None # Tupla conteniendo la informacion necesaria para el 
  # retorno del metodo. 3 o 4 posiciones: Codigo ejecucion (0 - Correcta;
  # -1 incorrecta), mensaje de resultado de ejecucion, conexion, 
  # empleado_pedido (opcional).


  # Local code
  # Pedir el nombre al usuario
  retorno_otros = utilidades.pedir_campo(peticiones_campos(0)[2], "departamento_nombre")

  if(retorno_otros[0] == -1): # Peticion erronea
      retorno = (-1, retorno_otros[1], conexion) # Construir retorno de ejecucion
  
  else: # Campo valido
    retorno_otros = query.query_select("departamento", [("departamento", "nombre"), ("departamento", "descripcion"), ("empleado", "nombre"),("departamento", "id")],[("left join", "empleado", "departamento", "responsable", "id")], [("departamento", "nombre", "=", f"\"{retorno_otros[2]}\"")])

    # Ejecutar la query
    retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])
    # Actualizar el valor de la conexion
    conexion = retorno_otros[2]

    if(retorno_otros[0] == -1): # Ejecucion erronea
      retorno = (-1, retorno_otros[1], conexion)
    
    else: # Ejecucion correcta
      # Obtener el resultado y comprobar si hay empleados encontrados
      if(len(retorno_otros) != 4): # Si NO hay empleados
        retorno = (0, "\nNo hay departamentos con el nombre proporcionado.", conexion)
      
      else: # Hay varios empleados con el nombre proporcionado.
        retorno = (0, "\nUn departamento encontrado", conexion, retorno_otros[3])
    
  return retorno
# ######################################################################### #
def modificar_departamento(conexion, parametros_conexion:tuple):
  """
  Modifica un departamendo de la base de datos.

  Busca un departamento por nombre . Si existe, pide confirmacion para modificarlo.
  En caso de obtenerla, intenta modificar de la base de datos el campo seleccionado.

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
  confirmado:bool = False # El usuario quiere borrar el empleado.
  empleados_lista:list[tuple] = None # Lista para almacenar los empleados leidos
    # de la base de datos.
  departamentos_lista:list[tuple] = None # Lista para almacenar los departamentos leidos
    # de la base de datos.
  departamento:str = "" # Contiene la informacion de los departamentos en una cadena 
  entrada = None # String para seleccionar que campo quieres modificar
  respuesta:str = None # String de la devolucion del metodo pedir campo
  empleados:tuple=None #tupla con la devolucion del metodo mostrar empleados
  em_txt:str=""# String con los empleados del departamento en texto
  queryT:tuple = None # Query para obtener los empleados del departamento
  #Local code
  print("\n4 - Modificar departamento.")
  # Mandar buscar el empleado
  retorno_otros = buscar_departamento(conexion, parametros_conexion)

  if(retorno_otros == -1): # Error en el buscar. Devolver error
    retorno = (-1, retorno_otros[1], conexion)

  else: # Ejecucion correcta
    # En cualquier caso, imprimir el mensaje de resultado
    print(retorno_otros[1])

    if(len(retorno_otros) != 4): # No hay departamento
      retorno = (0, retorno_otros[1], conexion)
    
    else: # Hay departamento
      departamentos_lista=retorno_otros[3]
        # correcta y con resultado
      for i in departamentos_lista:#lo pasamos a texto los departamentos
          departamento += metodos_mostrar.departamento_a_texto(conexion, parametros_conexion,i)
      print(departamento)#lo mostramos
      #Pedimos confirmacion
      confirmado = utilidades.pedir_confirmacion("\n¿Quiere modificar el departamento?")

      if(not confirmado): # El usuario no quiere modificar el departamento
          retorno = (-1, "\nModificar abortado.", conexion)
        
      else:
          # Imprimir menu
          print("\n\n"+"+"*60)
          print("Modficar Empleado:")
          print("1 - Nombre.")
          print("2 - Descripcion.")
          print("3 - Responsable.")
          print("0 - Salir")
          # Pedir opcion a realizar al usuario
          entrada = input("\nIntroduzca el numero de la opcion que desea realizar: ")
          # Filtrar opciones
          if(entrada == "0"): # Salir
                salir = utilidades.pedir_confirmacion("¿Quiere salir del menu disco?")

                if(salir):
                  print("\nAdios.")
                else:
                  print("\nSalida cancelada.")
              
          elif(entrada == "1"): # nombre
            # Pedir nombre al usuario
            respuesta=utilidades.pedir_campo(peticiones_campos(0)[2],"departamento_nombre")
            if(respuesta[0]!=-1):
              #Pedimos confirmación
              confirmado = utilidades.pedir_confirmacion("\n Esta seguro de modificar el departamento?")
              if(not confirmado): # El usuario no quiere modificar el departamento
                retorno = (-1, "\nBorrado abortado.", conexion)
              else:
                # Crear la query para borrar
                retorno_otros = query.query_update("departamento", [("departamento", "nombre", f"\"{respuesta[2]}\"")],None,[("departamento","nombre","=",f"\"{retorno_otros[3][0][0]}\"")])

                # Ejecutar la query sobre la base de datos
                retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])
                # Actualizar el valor de la conexion
                conexion = retorno_otros[2]

                if(retorno_otros[0] == -1) :
                  print(retorno_otros[1])
          elif(entrada == "2"): # descripcion
            # Pedir descripcion al usuario
            respuesta=utilidades.pedir_campo(peticiones_campos(1)[2],"departamento_descripcion")
            if(respuesta[0]!=-1):
              #Pedimos confirmación
              confirmado = utilidades.pedir_confirmacion("\n Esta seguro de modificar el departamento?")
              if(not confirmado): # El usuario no quiere modificar el departamento
                retorno = (-1, "\nBorrado abortado.", conexion)
              else:
                # Crear la query para borrar
                retorno_otros = query.query_update("departamento", [("departamento", "descripcion", f"\"{respuesta[2]}\"")],None,[("departamento","nombre","=",f"\"{retorno_otros[3][0][0]}\"")])

                # Ejecutar la query sobre la base de datos
                retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])
                # Actualizar el valor de la conexion
                conexion = retorno_otros[2]
          elif(entrada == "3"): # responsable
            # Pedir responsable al usuario
            subconsulta = query.query_select("departamento", [("departamento", "id")], None, [("departamento", "nombre", "=", f"\"{retorno_otros[3][0][0]}\"")])
            # Eliminar el punto y coma
            subconsulta = subconsulta[2][0:-1]

            # Obtener la query para seleccionar todos los empleados
            queryT = query.query_select("empleado", [("empleado", "nombre"), ("empleado", "correo_electronico"), ("empleado", "salario"), ("empleado", "fecha_contratacion"), ("departamento", "nombre"), ("empleado", "cargo"),("empleado", "id")],[("inner join", "departamento", "empleado", "departamento", "id")],[("departamento", "nombre", "=", f"\"{retorno_otros[3][0][0]}\""), ("empleado", "id", "NOT IN", f"({subconsulta})")])
            # Ejecutar la query sobre la base de datos
            empleados=base_datos.ejecutar_instruccion(conexion, parametros_conexion, queryT[2])
            if(empleados[0]==0 and len(empleados)==4):
              empleados_lista=empleados[3]
              for i in empleados_lista:
                em_txt+=metodos_mostrar.empleado_a_texto(conexion, parametros_conexion,i)+"\n"
              print(em_txt)
              respuesta=utilidades.pedir_campo(peticiones_campos(2)[2],"general_numero")
              if(respuesta[0]!=-1):
                #Pedimos confirmación
                confirmado = utilidades.pedir_confirmacion("\n Esta seguro de modificar el departamento?")
                if(not confirmado): # El usuario no quiere modificar el departamento
                  retorno = (-1, "\nBorrado abortado.", conexion)
                else:
                  # Crear la query para borrar
                  retorno_otros = query.query_update("departamento", [("departamento", "responsable", f"\"{respuesta[2]}\"")],None,[("departamento","nombre","=",f"\"{retorno_otros[3][0][0]}\"")])

                  # Ejecutar la query sobre la base de datos
                  retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])
                  # Actualizar el valor de la conexion
                  conexion = retorno_otros[2]

                  if(retorno_otros[0] != 0):
                    print(retorno_otros[1])
            else:
              print(empleados[1])
          if(retorno_otros[0] == 0): # Modificacion correcta
            retorno = (0, "\nDepartamento modificado de la base de datos", conexion)
          
          else: # Borrado erroneo
            retorno = (-1, retorno_otros[1], conexion)
  
  return retorno
