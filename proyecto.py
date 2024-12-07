# ############################################################################ #
#                                   IMPORT 
# ############################################################################ #
import utilidades
import query
import base_datos
import datetime

# ############################################################################ #
#                                   GLOBAL 
# ############################################################################ #


# ################################ Methods ################################ #
def menu_proyecto(conexion, parametros_conexion:tuple):
  """
  Submenu del programa, concerniente a los proyectos.

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
    print("1 - Alta proyecto.")
    print("2 - Baja proyecto..")
    print("3 - Buscar proyecto.")
    print("4 - Modificar proyecto.")
    print("5 - Mostrar proyectos.")
    print("0 - Salir")

    # Pedir opcion a realizar al usuario
    entrada = input("\nIntroduzca el numero de la opcion que desea realizar: ")

    # Filtrar opciones
    if(entrada == "0"): # Salir
      salir = utilidades.pedir_confirmacion("\n¿Quiere salir del submenu proyecto y volver al menu principal?")

      if(salir): # Si la salida esta confirmada
        print("\nAdios.")
      else: # Si la salida no se confirma
        print("\nSalida cancelada.")
    

    elif(entrada == "1"): # Alta proyecto
      print("\n"*2+"+"*60)
      print("1 - Alta proyecto.")
      retorno_otros = alta_proyecto(conexion, parametros_conexion)

      # Imprimir siempre el mensaje
      print(retorno_otros[1])

      # Actualizar el valor de la conexion
      conexion = retorno_otros[2]
      

    elif(entrada == "2"): # Baja proyecto
      print("\n"*2+"+"*60)
      print("2 - Baja proyecto.")
      retorno_otros = baja_proyecto(conexion, parametros_conexion)

      # Imprimir siempre el mensaje
      print(retorno_otros[1])

      # Actualizar el valor de la conexion
      conexion = retorno_otros[2]


    elif(entrada == "3"): # Buscar proyecto
      print("\n"*2+"+"*60)
      print("3 - Buscar proyecto.")
      retorno_otros = buscar_proyecto(conexion, parametros_conexion)

      # Imprimir siempre el mensaje
      print(retorno_otros[1])

      # Actualizar el valor de la conexion
      conexion = retorno_otros[2]

      if(retorno_otros[0] == 0 and len(retorno_otros) == 4): # Ejecucion 
        # correcta y con resultado
        retorno_otros = proyecto_a_texto(conexion, parametros_conexion, retorno_otros[3])

        # Actualizar el valor de la conexion
        conexion = retorno_otros[2]

        # Imprimir siempre el mensaje
        print(retorno_otros[1])

        if(retorno_otros[0] == 0):
          print(retorno_otros[3])


    elif(entrada == "4"): # Modificar proyecto
      print("\n"*2+"+"*60)
      print("4 - Modificar proyecto.")
      retorno_otros = modificar_proyecto(conexion, parametros_conexion)

      # Imprimir siempre el mensaje
      print(retorno_otros[1])

      # Actualizar el valor de la conexion
      conexion = retorno_otros[2]


    elif(entrada == "5"): # Mostrar proyectos
      print("\n"*2+"+"*60)
      print("5 - Mostrar proyectos.")
      retorno_otros = mostrar_proyecto(conexion, parametros_conexion)
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
    "\nIntroduzca el nombre del proyecto. No puede haber duplicados \n[Letras del alfabeto espanyol, espacios en blanco y los siguientes \ncaracteres \".,;&-\"][Longitud 1 a 60 caracteres]",

    "\nIntroduzca la descripcion del proyecto [Letras del alfabeto espanyol,\nespacios en blanco y los siguientes caracteres \".,;&-\"]\n[Longitud 0 a 255 caracteres]",

    "\nIntroduzca la fecha de finalizacion del proyecto dd-mm-aaaa",

    "\nIntroduzca el identificador del departamento responsable del proyecto",

    "\nIntroduzca el identificador del empleado responsable del proyecto"
  ]

  if(indice_peticion >= 0 and indice_peticion < len(peticiones)): # El indice es 
    # correcto
    retorno = (0, "Mensaje de peticion de campo obtenido", peticiones[indice_peticion])

  else: # El indice es incorrecto
    retorno = (-1, "El indice proporcionado no es valido.")
  
  return retorno


# ######################################################################### #
def alta_proyecto(conexion, parametros_conexion:tuple):
  """
  Crea un nuevo proyecto en la base de datos.

  Pide los campos al usuario, posteriormente escribe la query para insertar
  el nuevo proyecto en la base de datos y manda ejecutarla.

  El resultado devuelto por este metodo, es el resultado de ejecutar la query.
  
  No se comprueba la duplicidad de nombres de proyecto, eso se comprueba en la
  base de datos.

  Args:
      conn (Connection): 
        Conexion sobre el servidor de la base de datos.

      parametros_conexion (tuple):
        Tupla con 4 posiciones: usuario, contrasenya, puerto, nombre base datos.

  Returns:
      tuple: tres posiciones:
        - codigo de resultado (int): 
          0 en caso de ejecucion correcta, -1 en cualquier otro caso.
        - mensaje de ejecucion (str): 
          Mensaje para el usuario informando del resultado de la ejecucion 
          del metodo.
        - conexion (Connection):
          Conexion actual a la base de datos.
  """  
  # Local variables
  nombre_campos:list[str] = ["proyecto_nombre", "proyecto_descripcion", "general_fecha"]
  campos:list[str] = [] # Lista de los campos validos proporcionados por el 
    # usuario.
  continuar:bool = True # Continuar con la ejecucion del bucle
  indice:int = 0 # Indice para iterar en un bucle
  retorno_otros:tuple = None # Tupla conteniendo el retorno de otros metodos
  retorno:tuple # Tupla conteniendo la informacion necesaria para el 
  # retorno del metodo. 3 posiciones: Codigo ejecucion (0 - Correcta;
  # -1 incorrecta), mensaje de resultado de ejecucion, conexion.
  departamentos:dict[int, str] # Diccionario con los departamentos dentro.
  mensaje:str # Cadena de caracteres para pedir un campo.
  dep_usu:int # Departamento introducido por el usuario
  empleados:dict[int, str] # Diccionario con los empleados de un departamento 
    # dentro
  emp_usu:str # Empleado introducido por el usuario.


  # Local code
  # ##### Pedir los campos #####
  while(indice < len(nombre_campos) and continuar):
    retorno_otros = utilidades.pedir_campo(peticiones_campos(indice)[2], nombre_campos[indice])

    if(retorno_otros[0] == -1): # Si la ejecucion es erronea
      retorno = (-1, retorno_otros[1], conexion) # Construir retorno de ejecucion
      
      # Terminar la ejecucion del bucle
      continuar = False
    
    else: # Ejecucion correcta 
      campos.append(retorno_otros[2]) # anyadir a la lista de campos validos
      indice += 1 # Pedir el siguiente campo
  
  if(continuar): # Comprobar que la fecha de fin sea igual o mayor a la actual
    if(datetime.datetime.strptime(campos[2], "%Y-%m-%d").date() < datetime.datetime.now().date()):
      continuar = False

      retorno = (-1, "\nFecha invalida. La fecha debe ser igual o mayor a la actual.", conexion)


  if(continuar): # Todos los campos pedidos son validos y han sido anyadidos
    # ##### Pedir departamento #####
    retorno_otros = departamentos_a_diccionario(conexion, parametros_conexion)

    # Actualizar el valor de la conexion
    conexion = retorno_otros[2]

    if(retorno_otros[3] == {}): # No hay departamentos
      retorno = (-1, "No hay departamentos. Sin un departamento un proyecto no puede ser creado.", conexion)
    
    else: # Hay departamentos
      # Asignar departamentos a variable
      departamentos = retorno_otros[3]

      mensaje = "\nDepartamentos:\n"
      for k in departamentos.keys(): # Almacenar los departamentos en una 
        # cadena de caracteres
        mensaje += f"\t{k} - {departamentos[k]}\n"
      
      mensaje += "\nIntroduzca el ID del departamento al que quiere asignar el proyecto"
      retorno_otros = utilidades.pedir_campo(mensaje, "general_numero")

      if(retorno_otros[0] == -1): # Peticion erronea
        retorno = (-1, retorno_otros[1])
      
      else: # Peticion correcta
        dep_usu = int(retorno_otros[2]) # Casteo sin consecuencias, es un numero valido
        if(dep_usu not in departamentos.keys()): # Departamento incorrecto
          retorno = (-1, "\nDepartamento erroneo. Cancelando operacion", conexion)
        
        else: # Departamento correcto
          print(f"\nDepartamento {departamentos[dep_usu]} asignado.")

          # ##### Pedir el empleado responsable. #####
          retorno_otros = empleados_departamento_a_diccionario(conexion, parametros_conexion, dep_usu)

          # Actualizar el valor de la conexion
          conexion = retorno_otros[2]

          if(retorno_otros[3] == {}): # No hay empleados en el departamento
            retorno = (-1, "\nNo hay empleados. Sin un responsable un proyecto no puede ser creado.", conexion)
          
          else: # Hay empleados en el departamento
            # Asignar empleados a variable
            empleados = retorno_otros[3]

            mensaje = "\nEmpleados:\n"
            for e in empleados.keys(): # Almacenar los empleados en una 
              # cadena de caracteres
              mensaje += f"{e} - {empleados[e]}\n"
            mensaje += "\nIntroduzca el ID del empleado que quiere asignar como responsable del proyecto"
            retorno_otros = utilidades.pedir_campo(mensaje, "general_numero")

            if(retorno_otros[0] == -1): # Peticion erronea
              retorno = (-1, retorno_otros[1])

            else: # Peticion correcta
              emp_usu = int(retorno_otros[2]) # Casteo sin consecuencias, es un numero valido
              if(emp_usu not in empleados.keys()): # Empleado incorrecto
                retorno = (-1, "\nEmpleado erroneo. Cancelando operacion", conexion)
              
              else: # Empleado correcto
                print(f"\nEmpleado {departamentos[dep_usu]} designado como responsable.")

                # Hacer la query
                retorno_otros = query.query_insert_into("proyecto", ["nombre", "descripcion", "fecha_inicio", "fecha_fin", "departamento", "responsable"], [(f"\"{campos[0]}\"", f"\"{campos[1]}\"", "NOW()", f"\"{campos[2]}\"", f"{dep_usu}", f"{emp_usu}")])

                # Ejecutar la instruccion
                retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])
                
                # Actualizar el valor de la conexion
                conexion = retorno_otros[2]

                if(retorno_otros[0] == 0): # Insercion correcta
                  retorno = (0, "\nProyecto insertado en la base de datos.", conexion)
                
                else: # Insercion erronea
                  retorno = (-1, retorno_otros[1], conexion) # Devolver el menasje de error devuelto
                    # de la ejecucion de la instruccion
  
  return retorno


# ######################################################################### #
def baja_proyecto(conexion, parametros_conexion):
  """
  Borra un proyecto de la base de datos.

  Busca un proyecto por nombre. Si existe, pide confirmacion para borrarlo.
  En caso de obtenerla, intenta borrarlo de la base de datos.

  Args:
      conn (Connection): 
        Conexion sobre el servidor de la base de datos.

      parametros_conexion (tuple):
        Tupla con 4 posiciones: usuario, contrasenya, puerto, nombre base datos.

  Returns:
      tuple: tres posiciones:
        - codigo de resultado (int): 
          0 en caso de ejecucion correcta, -1 en cualquier otro caso.
        - mensaje de ejecucion (str): 
          Mensaje para el usuario informando del resultado de la ejecucion 
          del metodo.
        - conexion (Connection):
          Conexion actual a la base de datos.
  """  
  # Local variables
  retorno_otros:tuple = None # Retorno de ejecucion de otros metodos
  retorno:tuple = None # Tupla conteniendo la informacion necesaria para el 
  # retorno del metodo. 3 o 4 posiciones: Codigo ejecucion (0 - Correcta;
  # -1 incorrecta), mensaje de resultado de ejecucion, conexion, 
  # proyecto_pedido (opcional).
  proyecto:str = None # Cadena de caracteres con el proyecto a texto.
  confirmado:bool = False # El usuario quiere borrar el proyecto.

  # Local code
  # Mandar buscar el proyecto
  retorno_otros = buscar_proyecto(conexion, parametros_conexion)

  if(retorno_otros == -1): # Error en el buscar. Devolver error
    retorno = (-1, retorno_otros[1], conexion)

  else: # Ejecucion correcta
    # En cualquier caso, imprimir el mensaje de resultado
    print(retorno_otros[1])

    if(len(retorno_otros) != 4): # No hay proyecto
      retorno = (0, retorno_otros[1], conexion)
    
    else: # Hay proyecto
      # Obtener el proyecto formateado
      proyecto_a_textoT = proyecto_a_texto(conexion, parametros_conexion, retorno_otros[3])

      # Actualizar el valor de la conexion
      conexion = proyecto_a_textoT[2]

      if(proyecto_a_textoT[0] != 0): # Proyecto a texto erroneo
        retorno = (-1, proyecto_a_textoT[1], conexion)
      
      else: # Ejecucion correcta
        # Imprimir el proyecto
        print(proyecto_a_textoT[3])

        # Pedir confirmacion
        confirmado = utilidades.pedir_confirmacion("\n¿Quiere borrar el proyecto?")

        if(not confirmado): # El usuario no quiere borrar el proyecto
          retorno = (-1, "\nBorrado abortado.", conexion)
        
        else:
          # Crear la query para borrar
          retorno_otros = query.query_delete_from("proyecto", [("proyecto", "nombre", "=", f"\"{retorno_otros[3][0]}\"")])

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
def buscar_proyecto(conexion, parametros_conexion:tuple):
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
      tuple: tres o cuatro posiciones:
        - codigo de resultado (int): 
          0 en caso de ejecucion correcta, -1 en cualquier otro caso.
        - mensaje de ejecucion (str): 
          Mensaje para el usuario informando del resultado de la ejecucion 
          del metodo.
        - conexion (Connection):
          Conexion actual a la base de datos.
        - proyecto_resultado (tuple, optional):
          Tupla conteniendo el proyecto buscado. Contiene el nombre del 
          proyecto, su descripcion, la fecha de inicio, la fecha de fin,
          el nombre del departamento responsable y el empleado responsable
          del proyecto.
  """  
  # Local variables
  retorno_otros:tuple = None # Retorno de ejecucion de otros metodos
  retorno:tuple = None # Tupla conteniendo la informacion necesaria para el 
  # retorno del metodo. 3 o 4 posiciones: Codigo ejecucion (0 - Correcta;
  # -1 incorrecta), mensaje de resultado de ejecucion, conexion, 
  # proyecto_pedido (opcional).


  # Local code
  # Pedir el nombre al usuario
  retorno_otros = utilidades.pedir_campo(peticiones_campos(0)[2], "proyecto_nombre")

  if(retorno_otros[0] == -1): # Peticion erronea
      retorno = (-1, retorno_otros[1], conexion) # Construir retorno de ejecucion
  
  else: # Campo valido
    retorno_otros = query.query_select("proyecto", [("proyecto", "nombre"), ("proyecto", "descripcion"), ("proyecto", "fecha_inicio"), ("proyecto", "fecha_fin"), ("departamento", "id"), ("departamento", "nombre"), ("empleado", "id"), ("empleado", "nombre")], [("left join", "departamento", "proyecto", "departamento", "id"), ("left join", "empleado", "proyecto", "responsable", "id")], [("proyecto", "nombre", "=", f"\"{retorno_otros[2]}\"")])

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
def modificar_proyecto(conexion, parametros_conexion:tuple):
  # Local variables
  proyecto:tuple # Tupla conteniendo el proyecto obtenido de la base de datos.
  intentos:int = 3 # Intentos para imprimir el proyecto a texto
  valido:bool = False # Si el proyecto a sido pasado a una cadena de 
    # caracteres. Si el usuario ha seleccionado una opcion correcta
  pro_texto:str # Cadena de caracteres conteniendo la informacion del proyecto 
    # en texto
  opcion:str # Opcion introducida por el usuario
  nuevo_campo:str # Nuevo campo para modificar el anterior
  empleados:dict[int, str] # Diccionario con los empleados del sistema que 
    # pertenecen a un departamento en concreto ID: Nombre.
  mensaje:str # Cadena de caracteres con un mensaje para imprimir al usuario

  # Local code
  # Buscar un proyecto
  retorno_otros = buscar_proyecto(conexion, parametros_conexion)

  # Actualizar el valor de la conexion
  conexion = retorno_otros[2]

  if(retorno_otros[0] == -1): # Ejecucion erronea
    retorno = (-1, retorno_otros[1], conexion)
  
  else: # Ejecucion correcta
    if(len(retorno_otros) == 3): # No hay proyecto
      retorno = (0, retorno_otros[1], conexion)
  
    else: # Hay un proyecto
      # Imprimir mensaje de retorno
      print(retorno_otros[1])

      # Guardar proyecto en variable
      proyecto = retorno_otros[3]
      
      # Imprimir el proyecto en texto
      while(intentos > 0 and not valido):
        retorno_otros = proyecto_a_texto(conexion, parametros_conexion, proyecto)

        # Actualizar el valor de la conexion
        conexion = retorno_otros[2]

        if(retorno_otros[0] == -1): # Ejecucion erronea
          intentos -= 1 # Reducir un intento
        
        else: # Ejecucion correcta
          valido = True
          pro_texto = retorno_otros[3]
      
      if(intentos == 0 and not valido):
        retorno = (-1, "\nNo se ha podido obtener la informacion del proyecto. Cancelando modificacion.", conexion)
      
      else: # Se ha podido obtener el proyecto a texto
        # Resetear el numero de intentos a 5
        intentos = 5
        valido = False
        while(intentos > 0 and not valido):
        # Imprimir el proyecto a texto
          print(pro_texto)

          print("Menu modificar")
          print("1 - Nombre.")
          print("2 - Descripcion.")
          print("3 - Fecha Fin.")
          print("4 - Responsable.")
          print("5 - Anyadir empleados.")
          print("6 - Eliminar empleados.")
          print("0 - Salir.")

          opcion = input(f"\nIntroduzca el numero de la opcion que desea realizar; [{intentos} restantes]: ")

          if(opcion == "0"): # Salir
            valido = True # Opcion valida
            retorno = (0, "\nOperacion cancelada", conexion)
          
          # ##### CAMBIAR NOMBRE #####
          elif(opcion == "1"): # Cambiar Nombre
            valido = True # Opcion valida
            retorno_otros = utilidades.pedir_campo(peticiones_campos(0)[2], "proyecto_nombre")

            if(retorno_otros[0] != 0): # La peticion es erronea
              retorno = (-1, retorno_otros[1], conexion)
            
            else: # La peticion es correcta
              # Asignar el valor a una variable
              nuevo_campo = retorno_otros[2]

              # Pedir confirmacion para la operacion
              retorno_otros = utilidades.pedir_confirmacion(f"¿Quiere cambiar el nombre del proyecto de {proyecto[0]} a {nuevo_campo}?")

              if(retorno_otros is not True): # Operacion no confirmada
                retorno = (-1, "\nOperacion no confirmada por el usuario.", conexion)
              
              else: # Operacion confirmada. Hacer el cambio
                # Crear la query
                retorno_otros = query.query_update("proyecto", [("proyecto", "nombre", f"\"{nuevo_campo}\"")], None, [("proyecto", "nombre", "=", f"\"{proyecto[0]}\"")])

                # Ejecutar la query
                retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])

                # Actualziar el valor de la conexion
                conexion = retorno_otros[2]

                if(retorno_otros[0] != 0): # Ejecucion erronea
                  retorno = (-1, retorno_otros[1], conexion)
                
                else:
                  retorno = (0, f"\nNombre del proyecto cambiado de {proyecto[0]} a {nuevo_campo}.", conexion)
          
          
          # ##### CAMBIAR DESCRIPCION #####
          elif(opcion == "2"):
            valido = True
            retorno_otros = utilidades.pedir_campo(peticiones_campos(1)[2], "proyecto_descripcion")

            if(retorno_otros[0] != 0): # La peticion es erronea
              retorno = (-1, retorno_otros[1], conexion)
            
            else: # La peticion es correcta
              # Asignar el valor a una variable
              nuevo_campo = retorno_otros[2]

              # Pedir confirmacion para la operacion
              retorno_otros = utilidades.pedir_confirmacion(f"\n¿Quiere cambiar la descripcion del proyecto de \"{proyecto[1]}\" a \"{nuevo_campo}\"?")

              if(retorno_otros is not True): # Operacion no confirmada
                retorno = (-1, "\nOperacion no confirmada por el usuario", conexion)
              
              else: # Operacion confirmada. Hacer el cambio
                # Crear la query
                retorno_otros = query.query_update("proyecto", [("proyecto", "descripcion", f"\"{nuevo_campo}\"")], None, [("proyecto", "nombre", "=", f"\"{proyecto[0]}\"")])

                # Ejecutar la query
                retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])

                # Actualziar el valor de la conexion
                conexion = retorno_otros[2]

                if(retorno_otros[0] != 0): # Ejecucion erronea
                  retorno = (-1, retorno_otros[1], conexion)
                
                else:
                  retorno = (0, f"\nDescripcion del proyecto cambiada de {proyecto[1]} a {nuevo_campo}.", conexion)
          
          
          # ##### CAMBIAR FECHA FIN #####
          elif(opcion == "3"):
            valido = True
            retorno_otros = utilidades.pedir_campo(peticiones_campos(2)[2], "general_fecha")

            if(retorno_otros[0] != 0): # La peticion es erronea
              retorno = (-1, retorno_otros[1], conexion)
            
            else: # La peticion es correcta
              # Asignar el valor a una variable
              # Es un str
              nuevo_campo = datetime.datetime.strptime(retorno_otros[2], '%Y-%m-%d').date()
              
              # Comprobar que la fecha sea igual o mayor a la fecha de inicio
              if(nuevo_campo < proyecto[2]):
                retorno = (-1, f"\nLa fecha proporcionada es inferior a la fecha de inicio. {nuevo_campo.strftime("%d-%m-%Y")} < {proyecto[2].strftime("%d-%m-%Y")}", conexion)
              
              else: # La fecha es igual o mayor a la de inicio
                # Pedir confirmacion para la operacion
                retorno_otros = utilidades.pedir_confirmacion(f"\n¿Quiere cambiar la descripcion del proyecto de \"{proyecto[1]}\" a \"{nuevo_campo}\"?")

                if(retorno_otros is not True): # Operacion no confirmada
                  retorno = (-1, "\nOperacion no confirmada por el usuario", conexion)
                
                else: # Operacion confirmada. Hacer el cambio
                  # Crear la query
                  retorno_otros = query.query_update("proyecto", [("proyecto", "fecha_fin", f"\"{nuevo_campo}\"")], None, [("proyecto", "nombre", "=", f"\"{proyecto[0]}\"")])

                  # Ejecutar la query
                  retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])

                  # Actualziar el valor de la conexion
                  conexion = retorno_otros[2]

                  if(retorno_otros[0] != 0): # Ejecucion erronea
                    retorno = (-1, retorno_otros[1], conexion)
                  
                  else:
                    retorno = (0, f"\nFecha de fin de proyecto cambiada de {proyecto[3].strftime("%d-%m-%Y")} a {nuevo_campo.strftime("%d-%m-%Y")}.", conexion)


          # ##### CAMBIAR RESPONSABLE #####
          elif(opcion == "4"):
            valido = True
            
            # Obtener los departamentos en un diccionario
            retorno_otros = empleados_departamento_a_diccionario(conexion, parametros_conexion, proyecto[4])

            # Actualizar el valor de la conexion
            conexion = retorno_otros[2]

            if(retorno_otros[0] == -1): # Ejecucion erronea
              retorno = (-1, "\nError al obtener los empleados que trabajan en el departamento.", conexion)
            
            else: # Ejecucion correcta
              # SIEMPRE, tiene que existor al menos el empleado asignado como 
              # respo nsable a este proyecto.
              empleados = retorno_otros[3]

              # Eliminar el empleado que es el responsable actual
              del(empleados[proyecto[6]])

              # Concatenar los empleados en una cadena de caracteres
              mensaje = f"\nEmpleados del departamento {proyecto[5]}:\n"
              for k in empleados.keys():
                mensaje += f"\t{k} - {empleados[k]}\n"
              
              mensaje += "\nIntroduzca el identificador del empleado que quiera designar como responsable"
              
              # Pedir identificador al usuario
              retorno_otros = utilidades.pedir_campo(mensaje, "general_numero")

              # Peticion incorrecta
              if(retorno_otros[0] != 0):
                retorno = (-1, retorno_otros[1], conexion)
              
              else: # Peticion correcta
                if(retorno_otros[2] == "-1"): # El usuario no cancela la 
                  # operacion
                  retorno = (-1, retorno_otros[1], conexion)
                
                else: # Campo valido
                  nuevo_campo = int(retorno_otros[2]) # El casteo es seguro, ha 
                    # sido validado por una expresion regular
                  
                  if(nuevo_campo not in empleados.keys()):
                    retorno = (-1, "\nEl identificador del empleado es erroneo.", conexion)
                  
                  else: # La clave esta dentro del diccionario
                    retorno_otros = utilidades.pedir_confirmacion(f"¿Quiere cambiar el responsable del proyecto de \"{proyecto[7]}\"  a \"{empleados[nuevo_campo]}\"?")

                    if(retorno_otros == False): # No confirmada
                      retorno = (-1, "\nOperacion no confirmada por el usuario.", conexion)
                    
                    else: # Operacion confirmada
                      # Escribir la query
                      retorno_otros = query.query_update("proyecto", [("proyecto", "responsable", f"{nuevo_campo}")], None, [("proyecto", "nombre", "=", f"\"{proyecto[0]}\"")])

                      # Ejecutar la instruccion
                      retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])

                      # Actualizar el valor de la conexion
                      conexion = retorno_otros[2]

                      if(retorno_otros[0] != 0): # Ejecucion erronea
                        retorno = (-1, retorno_otros[1], conexion)
                      
                      else: # Ejecucion correcta
                        # Borrar de ser necesario el empleado si estaba 
                        # trabajando en el proyecto
                        retorno_otros = query.query_delete_from("empleado_proyecto", [("proyecto", "nombre", "=", f"\"{proyecto[0]}\""), ("empleado_proyecto", "ID_EMPLEADO", "=", f"{nuevo_campo}")], [("left join", "proyecto", "id_proyecto", "id")])

                        print(retorno_otros[2])

                        # Ejecutar instruccion
                        retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])

                        # Actualizar el valor de la conexion
                        conexion = retorno_otros[2]
                        
                        if(retorno_otros[0] != 0): # El empleado no se ha borrado de la lista de empleados de estar presente
                          retorno = (-1, "Empleado responsable modificado. El empleado no se ha borrado de la lista de empleados de estar presente"+retorno_otros[1])
                        
                        else: # Empleado borrado
                          retorno = (0, f"\nResponsable del proyecto {proyecto[0]} cambiado de {proyecto[7]} a {empleados[nuevo_campo]}.", conexion)


          # ##### Anyadir empleados #####
          elif(opcion == "5"):
            valido = True
            retorno = anyadir_empleados(conexion, parametros_conexion, proyecto)


          # ##### Eliminar empleados #####
          elif(opcion == "6"):
            valido = True
            retorno = eliminar_empleados(conexion, parametros_conexion, proyecto)

  return retorno


# ######################################################################### #
def anyadir_empleados(conexion, parametros_conexion:tuple, proyecto:tuple):
  """
  Anyadir un empleado a un proyecto.

  Dado un proyecto, buscar todos los empleados que no trabajan en el, y que 
  no son el responsable.

  Pedir al usuario que introduzca uno de los identificadores, y anyadirlo a la
  lista de empleados del proyecto si se otorga confirmacion.

  Args:
      conn (Connection): 
        Conexion sobre el servidor de la base de datos.

      parametros_conexion (tuple):
        Tupla con 4 posiciones: usuario, contrasenya, puerto, nombre base datos.

      proyecto (tuple): 
        Tupla conteniendo la informacion de un proyecto leida desde la base de 
        datos: Nombre, Descripcion, Fecha_inicio, Fecha_fin, ID_departamento, 
        nombre_departamento, ID_responsable, nombre responsable.


  Returns:
      tuple: tres posiciones:
        - codigo de resultado (int): 
          0 en caso de ejecucion correcta, -1 en cualquier otro caso.
        - mensaje de ejecucion (str): 
          Mensaje para el usuario informando del resultado de la ejecucion 
          del metodo.
        - conexion (Connection):
          Conexion actual a la base de datos.
  """  
  # Local variables
  retorno_otros:tuple = None # Retorno de ejecucion de otros metodos
  retorno:tuple = None # Tupla conteniendo la informacion necesaria para el 
  # retorno del metodo. 3 posiciones: Codigo ejecucion (0 - Correcta;
  # -1 incorrecta), mensaje de resultado de ejecucion, conexion.
  emp_dict:dict[int, str] # Diccionario conteniendo los empleados del
  # pertenecientes a un proyecto del sistema. Clave: int (ID); Valor: str 
  # (Nombre).
  subconsulta_1:str # Subconsulta para obtener los empleados que trabajan en el 
    # proyecto
  subconsulta_2:str # Subconsulta para obtener el identificador del responsable
    # del proyecto.
  mensaje:str # Mensaje para imprimir al usuario
  emp_id:int # Id del empleado introducido por el usuario
  id_proyecto:int # Id del proyecto

  # Local code
  subconsulta_1 = query.query_select("proyecto", [("empleado_proyecto","id_empleado")], [("inner join", "empleado_proyecto", "proyecto", "id", "id_proyecto")], [("proyecto", "nombre", "=", f"\"{proyecto[0]}\"")])[2]

  # Eliminar el punto y coma del final
  subconsulta_1 = subconsulta_1[0:-1]

  subconsulta_2 = query.query_select("proyecto", [("proyecto", "responsable")], None, [("proyecto", "nombre", "=", f"\"{proyecto[0]}\"")])[2]

  # Eliminar el punto y coma del final
  subconsulta_2 = subconsulta_2[0:-1]

  retorno_otros = query.query_select("empleado", [("empleado", "id"), ("empleado", "nombre")], None, [("empleado", "id", "NOT IN", f"({subconsulta_1})"), ("empleado", "id", "NOT IN", f"({subconsulta_2})")])

  # Diccionario con los empleados que no trabajam ni son responsables del 
  # proyecto.
  retorno_otros = empleados_a_diccionario(conexion, parametros_conexion, retorno_otros[2])

  # Actualizar el valor de la conexion
  conexion = retorno_otros[2]

  if(retorno_otros[0] != 0): # Ejecucion erronea
    retorno = (-1, retorno_otros[1], conexion)
  
  else: # Ejecucion correcta
    # Diccionario de empleados a variable
    emp_dict = retorno_otros[3]

    if(emp_dict == {}): # No hay empleados disponibles
      retorno = (0, "\nNo hay empleados disponibles para anyadir.", conexion)
    
    else: # Hay empleados
      mensaje = f"Empleados que no trabajan ni son responsable de {proyecto[0]}:\n"

      for k in emp_dict.keys():
        mensaje += f"\t{k} - {emp_dict[k]}\n"
      
      mensaje += "Introduzca el indice del empleado a anyadir al proyecto"

      retorno_otros = utilidades.pedir_campo(mensaje, "general_numero")

      if(retorno_otros[0] != 0): # Peticion erronea
        retorno = (-1, retorno_otros[1], conexion)
      
      else: # Peticion correcta
        if(retorno_otros[2] == "-1"): # Operacion cancelada
          retorno = (-1, "\nOperacion cancelada.", conexion)
        
        else: # Numero a validar
          emp_id = int(retorno_otros[2]) # Casteo seguro, ha pasado por una 
            # expresion regular
          
          if(emp_id not in emp_dict.keys()): # No es un identificador valido
            retorno = (-1, f"\nEl identificador {emp_id} no es valido.", conexion)
          
          else: # El identificador es valido
            # Pedir confirmacion de la accion
            retorno_otros = utilidades.pedir_confirmacion(f"¿Quiere anyadir al empleado {emp_dict[emp_id]} al proyecto {proyecto[0]}?")

            if(retorno_otros == False):
              retorno = (-1, "\nOperacion cancelada.", conexion)
            
            else: # Operacion confirmada
              # Obtener el id del proyecto
              retorno_otros = query.query_select("proyecto", [("proyecto", "id")],None, [("proyecto", "nombre", "=", f"\"{proyecto[0]}\"")])

              # Ejecutar la instruccion
              retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])

              # Actualizar el valor de la conexion
              conexion = retorno_otros[2]

              if(retorno_otros[0] != 0): # Ejecucion erronea
                retorno = (-1, retorno_otros[1], conexion)
              
              else: # Ejecucion correcta. SIEMPRE existira UN unico resultado
                id_proyecto = retorno_otros[3][0][0]

                # Hacer la query
                retorno_otros = query.query_insert_into("empleado_proyecto", ["id_empleado", "id_proyecto"], [(f"{emp_id}", f"{id_proyecto}")])

                # Ejecutar la instruccion
                retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])

                # Actualizar el valor de la conexion
                conexion = retorno_otros[2]

                if(retorno_otros[0] != 0): # Ejecucion erronea
                  retorno = (-1, retorno_otros[1], conexion)
                
                else: # Ejecucion correcta
                  retorno = (-1, f"\nEmpleado {emp_dict[emp_id]} anyadido al proyecto {proyecto[0]}.", conexion)
  
  return retorno


# ######################################################################### #
def eliminar_empleados(conexion, parametros_conexion:tuple, proyecto:tuple):
  """
  Elimina empleados de un proyecto.

  Dado un proyecto dentro de una tupla, y leido de la base de datos, se obtienen
  los empleados que trabajan en el mismo mediante empleados_a_diccionario.

  Posteriormente, pide al usuario el identificador del empleado que quiere 
  eliminar del proyecto. Tanto si es correcto como sino, pide confirmacion para
  terminar o continuar.

  En el caso de que se decida terminar y existan empleados a borrar, se llama a 
  la creacion y ejecucion de una query.


  Args:
      conn (Connection): 
        Conexion sobre el servidor de la base de datos.

      parametros_conexion (tuple):
        Tupla con 4 posiciones: usuario, contrasenya, puerto, nombre base datos.

      proyecto (tuple): 
        Tupla conteniendo la informacion de un proyecto leida desde la base de 
        datos: Nombre, Descripcion, Fecha_inicio, Fecha_fin, ID_departamento, 
        nombre_departamento, ID_responsable, nombre responsable.


  Returns:
      tuple: tres posiciones:
        - codigo de resultado (int): 
          0 en caso de ejecucion correcta, -1 en cualquier otro caso.
        - mensaje de ejecucion (str): 
          Mensaje para el usuario informando del resultado de la ejecucion 
          del metodo.
        - conexion (Connection):
          Conexion actual a la base de datos.
  """  
  # Local variables
  retorno_otros:tuple = None # Retorno de ejecucion de otros metodos
  retorno:tuple = None # Tupla conteniendo la informacion necesaria para el 
  # retorno del metodo. 3 posiciones: Codigo ejecucion (0 - Correcta;
  # -1 incorrecta), mensaje de resultado de ejecucion, conexion.
  emp_dict:dict[int, str] # Diccionario conteniendo los empleados del
  # pertenecientes a un proyecto del sistema. Clave: int (ID); Valor: str 
  # (Nombre).
  emp_borrar:dict[int, str] = {} # Empleados a borrar del proyecto
  mensaje:str # Mensaje para imprimir al usuario
  continuar:bool = True # Indica si se deben seguir pidiendo empleados a 
    # eliminar del proyecto
  id_usuario:int # Identificador introducido por el usario

  # Local code
  # Obtener los empleados del proyecto
  retorno_otros = query.query_select("proyecto", [("empleado", "id"), ("empleado", "nombre")], [("left join", "empleado_proyecto", "proyecto", "id", "id_proyecto"), ("left join", "empleado", "empleado_proyecto", "id_empleado", "id"), ("left join", "departamento", "empleado", "departamento", "id")], [("proyecto", "nombre", "=", f"\"{proyecto[0].upper()}\"")])

  # Obtener los empleados del proyecto en un diccionario
  retorno_otros = empleados_a_diccionario(conexion, parametros_conexion, retorno_otros[2])
  
  # Actualizar el valor de la conexion
  conexion = retorno_otros[2]

  # Ejecucion incorrecta
  if(retorno_otros[0] != 0):
    retorno = (-1, retorno_otros[1], conexion)
  
  else: # Ejecucion correcta
    # almacenar los empleados en una variable
    emp_dict = retorno_otros[3]
    
    # Comprobar si hay empleados
    if(emp_dict == {}):
      retorno = (0, "\nNo hay empleados que eliminar del proyecto.", conexion)
    
    else: # Hay empleados
      while(continuar and len(emp_dict.keys()) > 0):
        mensaje = f"\nEmpleados del proyecto {proyecto[0]}:\n"
        for k in emp_dict.keys():
          mensaje += f"{k} - {emp_dict[k]}\n"
        
        mensaje += "\nIntroduzca el identificador del empleado que desea borrar del proyecto"

        retorno_otros = utilidades.pedir_campo(mensaje, "general_numero")

        
        if(retorno_otros[0] != 0): # Peticion erronea
          # Imprimir mensaje
          print(retorno_otros[1])

        else: # Peticion correcta
          if(retorno_otros[2] == "-1"): # El usuario cancela la operacion
            continuar = False
          
          else: # Identificador a comprobar
            id_usuario = int(retorno_otros[2])

            if(id_usuario in emp_dict.keys()): # Si es un identificador 
              # valido
              # Introducir en el diccionario a borrar
              emp_borrar[id_usuario] = emp_dict[id_usuario]
              # Borrar del diccionario de presentes
              del(emp_dict[id_usuario])
            
            else: # No es un identificador correcto
              print(f"\nEl identificador {id_usuario} no es correcto.")
        
        if(continuar): # Si el usuario no cancela la operacion
          continuar = utilidades.pedir_confirmacion("¿Quiere seguir eliminando usuarios?")
      
      # Salir del while
      if(emp_borrar == {}): # Si no hay empelados a borrar
        retorno = (0, f"\nNo se han borrado empleados del proyecto {proyecto[0]}", conexion)
      
      else: # Hay empleados que borrar
        # ID de empleados a borrar en str
        mensaje = "("
        for k in emp_borrar.keys():
          mensaje += f"{k},"

        # Eliminar la ultima coma
        mensaje = mensaje[0:-1]

        mensaje += ")"

        # Crear la query
        retorno_otros = query.query_delete_from("empleado_proyecto", [("proyecto", "nombre", "=", f"\"{proyecto[0]}\""), ("empleado_proyecto", "id_empleado", "IN", f"{mensaje}")], [("left join", "proyecto", "id_proyecto", "id")])

        # Ejecutar la instruccion
        retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])

        # Actualizar el valor de la conexion
        conexion = retorno_otros[2]      

        if(retorno_otros[0] != 0): # Ejecucion erronea
          retorno = (-1, retorno_otros[1], conexion)
        
        else: # Ejecucion correcta
          retorno = (0, "\nEmpleados eliminados del proyecto.", conexion)

  return retorno


# ######################################################################### #
def mostrar_proyecto(conexion, parametros_conexion:tuple):
  """
  Crea una cadena de caracteres con la informacion de todos los proyectos.

  Realiza una query a la base de datos, y obtiene todos los proyectos 
  almacenados. Posteriormente uno a uno va pidiendo que se escriban en una 
  cadena de caracteres incluyendo los empleados que trabajan en los mismos.

  Si no hay ningun proyecto, devuelve un mensaje informativo.

  Args:
      conn (Connection): 
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
  proyectos_lista:list[tuple] = None # Lista para almacenar los proyectos leidos
    # de la base de datos.
  proyectos:str = "" # Contiene la informacion de los proyectos en una cadena 
    # de caracteres.
  errores:int = 0 # Numero de proyectos cuya lectura ha sido erronea.


  # Local code
  # Obtener la query para seleccionar todos los proyectos
  retorno_otros = query.query_select("proyecto", [("proyecto", "nombre"), ("proyecto", "descripcion"), ("proyecto", "fecha_inicio"), ("proyecto", "fecha_fin"), ("departamento", "id"), ("departamento", "nombre"), ("empleado", "id"), ("empleado", "nombre")], [("left join", "departamento", "proyecto", "responsable", "id"), ("left join", "empleado", "proyecto", "responsable", "id")])

  # Buscar todos los proyectos
  retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])

  # Actualizar el valor de la conexion
  conexion = retorno_otros[2]

  if(retorno_otros[0] != 0): # Ejecucion erronea
    retorno = (-1, retorno_otros[1], conexion)
  
  else: # Se ha podido hacer la query
    if(len(retorno_otros) == 3): # No hay proyectos
      retorno = (0, "\nNo hay proyectos que mostrar.", conexion)
    
    else: # Hay proyectos que mostrar
      # Guardar los proyectos en una variable
      proyectos_lista = retorno_otros[3]

      # Recorrer la lista e ir llamando a proyecto_a_texto
      for i in proyectos_lista:
        retorno_otros = proyecto_a_texto(conexion, parametros_conexion, i)

        # Actualizar el valor de la conexion
        conexion = retorno_otros[2]

        if(retorno_otros[0] == 0): # Proyecto a texto creado correctamente
          proyectos += retorno_otros[3]
        
        else: # Lectura erronea, almacenar el numero
          errores += 1
      
      # Al acabar el for, si hay algun proyecto erroneo, anyadir al final el 
      # mensaje de error.
      if(errores != 0):
        proyectos += f"\nSe ha producio un error en la lectura de {errores}proyecto/s."
      
      retorno = (0, "Proyectos escritos en texto", conexion, proyectos)
  
  return retorno


# ######################################################################### #
def proyecto_a_texto(conexion, parametros_conexion:tuple, proyecto:tuple):
  """
  Escribe los datos de un proyecto a una cadena de caracteres.

  Dada una tupla obtenida de una query a la base de datos, escribe en una
  cadena de caracteres la informacion del proyecto formateada y legible para
  el usuario.

  En caso de que alguno de los campos tenga valor vacio o NULL, se cambia a un
  valor "amigable" para el usuario como: "Sin Descripcion" o "Sin responsable."

  Args:
      conn (Connection): 
        Conexion sobre el servidor de la base de datos.

      parametros_conexion (tuple):
        Tupla con 4 posiciones: usuario, contrasenya, puerto, nombre base datos.

      proyecto (tuple):
        Tupla obtenida de una query SELECT a la base de datos. Consta de 6
        posiciones: Nombre, Descripcion, Fecha Inicio, Fecha Fin, Departamento
        y Responsable.
  
  Returns:
      str:
        Cadena de caracteres con la informacion del proyecto formateada, lista
        para imprimir.
  """  
  # Local variables
  pro_texto:str = "" # Cadena de texto conteniendo el proyecto
  empleados:tuple = None # Retorno de la consulta a la base de datos sobre la 
    # tabla empleado_proyecto
  queryT:tuple = None # Query para obtener los empleados

  # Local code
  pro_texto += "\nProyecto:\n"
  pro_texto += f"\tNombre: {proyecto[0]}\n"

  if(proyecto[1] is None or proyecto[1] == ""): # La descripcion es nula o 
    # vacia.
    pro_texto += f"\tDescripcion: Sin descripcion.\n"

  else: # Hay descripcion
    pro_texto += f"\tDescripcion: {proyecto[1]}\n"

  # Cambiar fechas de dormato americano a europeo
  pro_texto += f"\tFecha de inicio: {proyecto[2].strftime('%d-%m-%Y')}\n"
  pro_texto += f"\tFecha de fin: {proyecto[3].strftime('%d-%m-%Y')}\n"

  if(proyecto[4] is None): # No hay departamento
    pro_texto += f"\tDepartamento: Sin departamento.\n"

  else: # Hay departamento
    pro_texto += f"\tDepartamento: {proyecto[4]} - {proyecto[5]}\n"

  if(proyecto[6] is None): # No hay un empleado responsabñe
    pro_texto += f"\tResponsable: Sin responsable.\n"
  
  else: # Hay un departamento responsable
    pro_texto += f"\tResponsable: {proyecto[6]} - {proyecto[7]}\n"


  # Empleados que trabajan en un proyecto
  # Crear la query
  queryT = query.query_select("proyecto", [("empleado", "id"), ("empleado", "nombre"), ("departamento", "nombre")], [("left join", "empleado_proyecto", "proyecto", "id", "id_proyecto"), ("left join", "empleado", "empleado_proyecto", "id_empleado", "id"), ("left join", "departamento", "empleado", "departamento", "id")], [("proyecto", "nombre", "=", f"\"{proyecto[0].upper()}\"")])
  

  # Ejecutar la query
  empleados = base_datos.ejecutar_instruccion(conexion, parametros_conexion, queryT[2])

  # Actualizar el valor de la conexion
  conexion = empleados[2]

  # Anyadir la cabecera de empleados
  pro_texto += "\n\tEmpleados:\n"

  if(empleados[0] != 0): # Error al ejecutar
    retorno = (-1, "\nError al leer los empleados de la base de datos.")
  
  else: # Se han leido correctamente
    # Si no hay empleados
    if(empleados[3] == ((None, None, None),)):
      pro_texto+= "\t\tNo hay empleados trabajando en el proyecto.\n"
    
    else: # Si hay emppleados
      for empleado in empleados[3]:
        pro_texto += f"\t\t{empleado[0]} - {empleado[1].upper()} - {empleado[2].upper()}\n"

      pro_texto+= "\n"

    retorno = (0, "Proyecto escrito en una cadena de caracteres", conexion, pro_texto)
  
  return retorno


# ######################################################################### #
def departamentos_a_diccionario(conexion, parametros_conexion:tuple):
  """
  Busca los departamentos presentes en el sistema, y los almacena en un
  diccionario.

  Busca en la base de datos, el ID del departamento, y su nombre.
  Si los puede obtener, almacena el ID como la clave del diccionario,
  y el nombre como el valor.

  Args:
      conn (Connection): 
        Conexion sobre el servidor de la base de datos.

      parametros_conexion (tuple):
        Tupla con 4 posiciones: usuario, contrasenya, puerto, nombre base datos.

  Returns:
      tuple: cuatro posiciones:
        - codigo de resultado (int): 
          0 en caso de ejecucion correcta, -1 en cualquier otro caso.
        - mensaje de ejecucion (str): 
          Mensaje para el usuario informando del resultado de la ejecucion 
          del metodo.
        - conexion (Connection):
          Conexion actual a la base de datos.
        - departamentos (dict[int, str]):
          Diccionario que contiene los departamentos en su interior, el ID como
          clave, y el nombre como valor. En caso de no existir departamentos o 
          de producirse un error, el diccionario es vacio.
  """  
  # Local variables
  retorno_otros:tuple = None # Retorno de ejecucion de otros metodos
  retorno:tuple = None # Tupla conteniendo la informacion necesaria para el 
  # retorno del metodo. 3 o 4 posiciones: Codigo ejecucion (0 - Correcta;
  # -1 incorrecta), mensaje de resultado de ejecucion, conexion, 
  # diccionario de departamentos.
  dep_dict:dict[int, str] = {} # Diccionario conteniendo los departamentos del
  # sistema. Clave: int (ID); Valor: str (Nombre).

  # Local code
  # Hacer la query para obtener el nombre de todos los departamentos
  retorno_otros = query.query_select("departamento", [("departamento", "id"), ("departamento", "nombre")])

  # Ejecutar la query
  retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])

  # Actualizar el valor de la conexion
  conexion = retorno_otros[2]

  if(retorno_otros[0] != 0): # No se pueden leer los departamentos en la base
    # de datos
    retorno = (-1, "\nError al leer los departamentos en la base de datos. Cancelando creacion de nuevo proyecto.", conexion, dep_dict)
  
  else: # Se han podido leer los departamentos
    # No hay departamentos
    if(len(retorno_otros) != 4): # No hay departamentos
      retorno = (0, "\nNo hay departamentos", conexion, dep_dict)
    
    else: # Hay departamentos
      # Comprobar que sea distinto de algo vacio
      if(retorno_otros[3] == ((None, None),)): # No hay departamentos
        retorno = (0, "\nNo hay departamentos", conexion, dep_dict)
      
      else: # Hay departamentos
        # Recorrer la lista de tuplas
        for i in retorno_otros[3]:
          dep_dict[i[0]] = ""+i[1]
        
        retorno = (0, "\nDepartamentos insertados en diccionario", conexion, dep_dict)

  return retorno


# ######################################################################### #
def empleados_departamento_a_diccionario(conexion, parametros_conexion:tuple, id:int):
  """
  Busca los empleados pertenecicnetes a un depertamentos del sistema, y los 
  almacena en un diccionario.

  Busca en la base de datos, el ID del empleado, y su nombre, que trabajan en
  un departamento.
  Si los puede obtener, almacena el ID como la clave del diccionario,
  y el nombre como el valor.

  Args:
      conn (Connection): 
        Conexion sobre el servidor de la base de datos.

      parametros_conexion (tuple):
        Tupla con 4 posiciones: usuario, contrasenya, puerto, nombre base datos.

  Returns:
      tuple: cuatro posiciones:
        - codigo de resultado (int): 
          0 en caso de ejecucion correcta, -1 en cualquier otro caso.
        - mensaje de ejecucion (str): 
          Mensaje para el usuario informando del resultado de la ejecucion 
          del metodo.
        - conexion (Connection):
          Conexion actual a la base de datos.
        - empleados (dict[int, str]):
          Diccionario que contiene los empleados en su interior, el ID como
          clave, y el nombre como valor. En caso de no existir empleados o 
          de producirse un error, el diccionario es vacio.
  """  
  # Local variables
  retorno_otros:tuple = None # Retorno de ejecucion de otros metodos
  retorno:tuple = None # Tupla conteniendo la informacion necesaria para el 
  # retorno del metodo. 4 posiciones: Codigo ejecucion (0 - Correcta;
  # -1 incorrecta), mensaje de resultado de ejecucion, conexion, 
  # diccionario de empleados.
  emp_dict:dict[int, str] = {} # Diccionario conteniendo los empleados del
  # pertenecientes a un departamento del sistema. Clave: int (ID); Valor: str 
  # (Nombre).


  # Local code
  # Hacer la query para obtener el nombre de todos los departamentos
  retorno_otros = query.query_select("empleado", [("empleado", "id"), ("empleado", "nombre")], None, [("empleado", "departamento", "=", f"{1}")])

  # Ejecutar la query
  retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])

  # Actualizar el valor de la conexion
  conexion = retorno_otros[2]

  if(retorno_otros[0] != 0): # No se pueden leer los empleados en la base
    # de datos
    retorno = (-1, "\nError al leer los empleados en la base de datos. Cancelando creacion de nuevo proyecto.", conexion, emp_dict)
  
  else: # Se han podido leer los empleados
    # No hay empleados
    if(len(retorno_otros) != 4): # No hay departamentos
      retorno = (0, "\nNo hay empleados.", conexion, emp_dict)
    
    else: # Hay empleados
      # Comprobar que sea distinto de algo vacio
      if(retorno_otros[3] == ((None, None),)): # No hay empleados
        retorno = (0, "\nNo hay empleados.", conexion, emp_dict)
      
      else: # Hay departamentos
        # Recorrer la lista de tuplas
        for i in retorno_otros[3]:
          emp_dict[i[0]] = ""+i[1]
        
        retorno = (0, "\nEmpleados insertados en diccionario.", conexion, emp_dict)
    
  return retorno


# ######################################################################### #
def empleados_a_diccionario(conexion, parametros_conexion:tuple, query:str):
  """
  Dada una query, se introducen los empelados resultantes de la ejecucion de
  la misma en la base de datos en un diccionario.


  Args:
      conn (Connection): 
        Conexion sobre el servidor de la base de datos.

      parametros_conexion (tuple):
        Tupla con 4 posiciones: usuario, contrasenya, puerto, nombre base datos.

      query (str): Consulta a ejecutar para obtener los empleados. Puede ser de 
        dos tipos: Los empleados que trabajan en un proyecto (eliminar), o los empleados que no trabajan en un proyecto (anyadir).

  Returns:
      tuple: cuatro posiciones:
        - codigo de resultado (int): 
          0 en caso de ejecucion correcta, -1 en cualquier otro caso.
        - mensaje de ejecucion (str): 
          Mensaje para el usuario informando del resultado de la ejecucion 
          del metodo.
        - conexion (Connection):
          Conexion actual a la base de datos.
        - empleados (dict[int, str]):
          Diccionario que contiene los empleados en su interior, el ID como
          clave, y el nombre como valor. En caso de no existir empleados o 
          de producirse un error, el diccionario es vacio.
  """  
  
  # Local variables
  retorno_otros:tuple = None # Retorno de ejecucion de otros metodos
  retorno:tuple = None # Tupla conteniendo la informacion necesaria para el 
  # retorno del metodo. 4 posiciones: Codigo ejecucion (0 - Correcta;
  # -1 incorrecta), mensaje de resultado de ejecucion, conexion, 
  # diccionario de empleados.
  emp_dict:dict[int, str] = {} # Diccionario conteniendo los empleados del
  # pertenecientes a un departamento del sistema. Clave: int (ID); Valor: str 
  # (Nombre).
  
  # Local code
  # Ejecutar la query
  retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, query)

  # Actualizar el valor de la conexion
  conexion = retorno_otros[2]

  if(retorno_otros[0] != 0): # No se pueden leer los departamentos en la base
    # de datos
    retorno = (-1, "\nError al leer los empleados en la base de datos. Cancelando modificacion de proyecto.", conexion, emp_dict)
  
  else: # Se han podido leer los empleados
    # No hay empleados
    if(len(retorno_otros) != 4): # No hay empleados
      retorno = (0, "\nNo hay empleados.", conexion, emp_dict)
    
    else: # Hay empleados
      # Comprobar que sea distinto de algo vacio
      if(retorno_otros[3] == ((None, None),)): # No hay empleados
        retorno = (0, "\nNo hay empleados.", conexion, emp_dict)
      
      else: # Hay departamentos
        # Recorrer la lista de tuplas
        for i in retorno_otros[3]:
          emp_dict[i[0]] = ""+i[1]
        
        retorno = (0, "\nEmpleados insertados en diccionario.", conexion, emp_dict)
    
  return retorno
