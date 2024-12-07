# ############################################################################ #
#                                   IMPORT 
# ############################################################################ #
import utilidades
import query
import base_datos
import metodos_mostrar
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
    print("Empleados:")
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
      

    elif(entrada == "2"): # Baja empleado
      print(borrar_empleado(conexion, parametros_conexion)[1])

    elif(entrada == "3"): # Buscar empleado
      print("\n3 - Buscar empleado.")
      retorno_otros = buscar_empleado(conexion, parametros_conexion)
      # Imprimir siempre el mensaje

      print(retorno_otros[1])

      # Actualizar el valor de la conexion
      conexion = retorno_otros[2]

      if(retorno_otros[0] == 0 and len(retorno_otros) == 4): # Ejecucion 
        empleados_lista=retorno_otros[3]
        # correcta y con resultado
        #pasamos los empleados a texto
        for i in empleados_lista:
          retorno_otros = metodos_mostrar.empleado_a_texto(conexion, parametros_conexion,i)
          empleados += retorno_otros
        print(empleados)

    elif(entrada == "4"): # Modificar empleado
      modificar_empleado(conexion, parametros_conexion)
    

    elif(entrada == "5"): # Mostrar empleados
      print("\n5 - Mostrar empleado.")
      retorno_otros = metodos_mostrar.mostrar_empleado(conexion, parametros_conexion)
      print(retorno_otros[1])

      # Hay empleados que imprimir
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

    "\nIntroduzca el id del departamento.El id ha de ser numerico ",

    "\nIntroduzca el id del empleado.El id ha de ser numerico "
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
  repetir:bool=True#booleano para el bucle para anyadir empleados 

  # Local code
  print("\n1 - Alta empleado.")
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
      retorno_otros = query.query_insert_into("empleado", ["nombre", "correo_electronico", "fecha_contratacion", "salario"], [(f"\"{campos[0]}\"", f"\"{campos[1]}\"", "NOW()", f"\"{campos[2]}\"")])


      # Ejecutar la instruccion
      retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])
      
      # Actualizar el valor de la conexion
      conexion = retorno_otros[2]

      if(retorno_otros[0] == 0): # Insercion correcta
        print("\nEmpleado insertado en la base de datos.")
      
      else: # Insercion erronea
        print(retorno_otros[1]) # Devolver el menasje de error devuelto
          # de la ejecucion de la instruccion
    repetir=utilidades.pedir_confirmacion("\nQuiere anyadir otro empleado?")
    indice=0

# ######################################################################### #
def borrar_empleado(conexion, parametros_conexion):
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
  empleados_lista:list[tuple] = None # Lista para almacenar los empleados leidos
    # de la base de datos.
  empleados:str = "" # Contiene la informacion de los empleados en una cadena 

  # Local code
  print("\n2 - Borrar empleado.")
  # Mandar buscar el empleado
  retorno_otros = buscar_empleado(conexion, parametros_conexion)

  if(retorno_otros == -1): # Error en el buscar. Devolver error
    retorno = (-1, retorno_otros[1], conexion)

  else: # Ejecucion correcta
    # En cualquier caso, imprimir el mensaje de resultado
    print(retorno_otros[1])

    if(len(retorno_otros) != 4): # No hay empleado
      retorno = (0, retorno_otros[1], conexion)
    
    else: # Hay empleado
      empleados_lista=retorno_otros[3]
        # correcta y con resultado
      for i in empleados_lista:#lo pasamos a texto los empleados
          empleados+=f"\nEmpleado: {i[6]}\n"
          retorno_otros = metodos_mostrar.empleado_a_texto(conexion, parametros_conexion,i)
          empleados += retorno_otros
      print(empleados)#lo mostramos

      # Pedir confirmacion
      retorno_otros=utilidades.pedir_campo(peticiones_campos(5)[2],"general_numero")
      if(retorno_otros[0]!=-1):
        confirmado = utilidades.pedir_confirmacion("\n¿Quiere borrar el empleado?")

        if(not confirmado): # El usuario no quiere borrar el empleado
          retorno = (-1, "\nBorrado abortado.", conexion)
        
        else:
          # Crear la query para borrar
          retorno_otros = query.query_delete_from("empleado", [("empleado", "id", "=", f"\"{retorno_otros[2][0]}\"")])

          # Ejecutar la query sobre la base de datos
          retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])
          # Actualizar el valor de la conexion
          conexion = retorno_otros[2]

          if(retorno_otros[0] == 0): # Borrado correcto
            retorno = (0, "\nEmpleado borrado de la base de datos", conexion)
          
          else: # Borrado erroneo
            retorno = (-1, retorno_otros[1], conexion)
  
  return retorno
# ######################################################################### #
def buscar_empleado(conexion, parametros_conexion:tuple):
  """
  Busca un empleado en la base de datos.

  Dado el nombre del empleado, escribe la query y la ejecuta.

  El resultado puede ser obtener los empleados o ninguno.

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
  retorno_otros = utilidades.pedir_campo(peticiones_campos(0)[2], "empleado_nombre")

  if(retorno_otros[0] == -1): # Peticion erronea
      retorno = (-1, retorno_otros[1], conexion) # Construir retorno de ejecucion
  
  else: # Campo valido
    retorno_otros = query.query_select("empleado", [("empleado", "nombre"), ("empleado", "correo_electronico"), ("empleado", "salario"), ("empleado", "fecha_contratacion"), ("departamento", "nombre"), ("empleado", "cargo"),("empleado", "id")],[("left join", "departamento", "empleado", "departamento", "id")], [("empleado", "nombre", "=", f"\"{retorno_otros[2]}\"")])

    # Ejecutar la query
    retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])
    # Actualizar el valor de la conexion
    conexion = retorno_otros[2]

    if(retorno_otros[0] == -1): # Ejecucion erronea
      retorno = (-1, retorno_otros[1], conexion)
    
    else: # Ejecucion correcta
      # Obtener el resultado y comprobar si hay empleados encontrados
      if(len(retorno_otros) != 4): # Si NO hay empleados
        retorno = (0, "\nNo hay empleados con el nombre proporcionado.", conexion)
      
      else: # Hay varios empleados con el nombre proporcionado.
        retorno = (0, "\nUn empleado encontrado", conexion, retorno_otros[3])
    
    return retorno
# ######################################################################### #
def modificar_empleado(conexion, parametros_conexion:tuple):
  """
  Modifica un empleado de la base de datos.

  Busca un empleado por nombre . Si existe, pide confirmacion para modificarlo.
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
  proyecto:str = None # Cadena de caracteres con el empleado a texto.
  confirmado:bool = False # El usuario quiere borrar el empleado.
  empleados_lista:list[tuple] = None # Lista para almacenar los empleados leidos
    # de la base de datos.
  empleados:str = "" # Contiene la informacion de los empleados en una cadena 
  entrada = None # String para seleccionar que campo quieres modificar
  respuesta:str = None # String de la devolucion del metodo pedir campo
  departamentos:tuple=None #tupla con la devolucion del metodo mostrar departamentos
  #Local code
  print("\n4 - Modificar empleado.")
  # Mandar buscar el empleado
  retorno_otros = buscar_empleado(conexion, parametros_conexion)

  if(retorno_otros == -1): # Error en el buscar. Devolver error
    retorno = (-1, retorno_otros[1], conexion)

  else: # Ejecucion correcta
    # En cualquier caso, imprimir el mensaje de resultado
    print(retorno_otros[1])

    if(len(retorno_otros) != 4): # No hay empleado
      retorno = (0, retorno_otros[1], conexion)
    
    else: # Hay empleado
      empleados_lista=retorno_otros[3]
        # correcta y con resultado
      for i in empleados_lista:#lo pasamos a texto los empleados
          empleados+=f"\nEmpleado: {i[6]}\n"
          retorno_otros = metodos_mostrar.empleado_a_texto(conexion, parametros_conexion,i)
          empleados += retorno_otros
      print(empleados)#lo mostramos

      # Pedir confirmacion
      retorno_otros=utilidades.pedir_campo(peticiones_campos(5)[2],"general_numero")
      if(retorno_otros[0]!=-1):
        confirmado = utilidades.pedir_confirmacion("\n¿Quiere modificar el empleado?")

        if(not confirmado): # El usuario no quiere borrar el empleado
          retorno = (-1, "\nBorrado abortado.", conexion)
        
        else:
          # Imprimir menu
          print("\n\n"+"+"*60)
          print("Modficar Empleado:")
          print("1 - Nombre.")
          print("2 - Correo.")
          print("3 - Salario.")
          print("4 - Cargo.")
          print("5 - Departamento.")
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
            respuesta=utilidades.pedir_campo(peticiones_campos(0)[2],"empleado_nombre")
            if(respuesta[0]!=-1):
              #Pedimos confirmación
              modificar = utilidades.pedir_confirmacion("\n Esta seguro de modificar el empleado?")
              if(not confirmado): # El usuario no quiere modificar el empleado
                retorno = (-1, "\nBorrado abortado.", conexion)
              else:
                # Crear la query para borrar
                retorno_otros = query.query_update("empleado", [("empleado", "nombre", f"\"{respuesta[2]}\"")],None,[("empleado","id","=",f"\"{retorno_otros[2]}\"")])

                # Ejecutar la query sobre la base de datos
                retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])
                # Actualizar el valor de la conexion
                conexion = retorno_otros[2]
          elif(entrada == "2"): # correo
            # Pedir correo al usuario
            respuesta=utilidades.pedir_campo(peticiones_campos(1)[2],"empleado_correo")
            if(respuesta[0]!=-1):
              #Pedimos confirmación
              modificar = utilidades.pedir_confirmacion("\n Esta seguro de modificar el empleado?")
              if(not confirmado): # El usuario no quiere modificar el empleado
                retorno = (-1, "\nBorrado abortado.", conexion)
              else:
                # Crear la query para borrar
                retorno_otros = query.query_update("empleado", [("empleado", "correo_electronico", f"\"{respuesta[2]}\"")],None,[("empleado","id","=",f"\"{retorno_otros[2]}\"")])

                # Ejecutar la query sobre la base de datos
                retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])
                # Actualizar el valor de la conexion
                conexion = retorno_otros[2]
          elif(entrada == "3"): # salario
            # Pedir salario al usuario
            respuesta=utilidades.pedir_campo(peticiones_campos(2)[2],"empleado_salario")
            if(respuesta[0]!=-1):
              #Pedimos confirmación
              modificar = utilidades.pedir_confirmacion("\n Esta seguro de modificar el empleado?")
              if(not confirmado): # El usuario no quiere modificar el empleado
                retorno = (-1, "\nBorrado abortado.", conexion)
              else:
                # Crear la query para borrar
                retorno_otros = query.query_update("empleado", [("empleado", "salario", f"\"{respuesta[2]}\"")],None,[("empleado","id","=",f"\"{retorno_otros[2]}\"")])

                # Ejecutar la query sobre la base de datos
                retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])
                # Actualizar el valor de la conexion
                conexion = retorno_otros[2]
          elif(entrada == "4"): # cargo
            # Pedir cargo al usuario
            respuesta=utilidades.pedir_campo(peticiones_campos(3)[2],"empleado_cargo")
            if(respuesta[0]!=-1):
              #Pedimos confirmación
              modificar = utilidades.pedir_confirmacion("\n Esta seguro de modificar el empleado?")
              if(not confirmado): # El usuario no quiere modificar el empleado
                retorno = (-1, "\nBorrado abortado.", conexion)
              else:
                # Crear la query para borrar
                retorno_otros = query.query_update("empleado", [("empleado", "cargo", f"\"{respuesta[2]}\"")],None,[("empleado","id","=",f"\"{retorno_otros[2]}\"")])

                # Ejecutar la query sobre la base de datos
                retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])
                # Actualizar el valor de la conexion
                conexion = retorno_otros[2]
          elif(entrada == "5"): # departamento
            #mostramos los departamentos
            departamentos=metodos_mostrar.mostrar_departamento(conexion, parametros_conexion,True)
            if(departamentos[0] == 0 and len(departamentos)==4):#si lo que devuelve el mostrar departamento coincide con la condicion
              print(departamentos[3])
              # Pedir departamento al usuario
              respuesta=utilidades.pedir_campo(peticiones_campos(4)[2],"general_numero")
              if(respuesta[0]!=-1):
                #Pedimos confirmación
                modificar = utilidades.pedir_confirmacion("\n Esta seguro de modificar el empleado?")
                if(not confirmado): # El usuario no quiere modificar el empleado
                  retorno = (-1, "\nBorrado abortado.", conexion)
                else:
                  # Crear la query para borrar
                  retorno_otros = query.query_update("empleado", [("empleado", "departamento", f"\"{respuesta[2]}\"")],None,[("empleado","id","=",f"\"{retorno_otros[2]}\"")])

                  # Ejecutar la query sobre la base de datos
                  retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])
                  # Actualizar el valor de la conexion
                  conexion = retorno_otros[2]
            else:
              print(departamentos[1])
          if(retorno_otros[0] == 0): # Modificacion correcta
            retorno = (0, "\nEmpleado modificado de la base de datos", conexion)
          
          else: # Borrado erroneo
            retorno = (-1, retorno_otros[1], conexion)
  
  return retorno
