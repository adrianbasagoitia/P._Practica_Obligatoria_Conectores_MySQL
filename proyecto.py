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

  # Local code
  while(not salir): # Iterar mientras que el usuario no confirme la salida
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
      salir = utilidades.pedir_confirmacion("¿Quiere salir del programa?")

      if(salir): # Si la salida esta confirmada
        print("\nAdios.")
      else: # Si la salida no se confirma
        print("\nSalida cancelada.")
    
    elif(entrada == "1"): # Alta proyecto
      alta_proyecto(conexion, parametros_conexion)
      

    elif(entrada == "2"): # Baja proyecto
      baja_proyecto(conexion, parametros_conexion)
    
    elif(entrada == "3"): # Buscar proyecto
      buscar_proyecto(conexion, parametros_conexion)
    
    elif(entrada == "4"): # Modificar proyecto
      modificar_proyecto(conexion, parametros_conexion)
    
    elif(entrada == "3"): # Mostrar proyectos
      mostrar_proyecto(conexion, parametros_conexion)
    
    else: # Opcion erronea
      print(f"\nERROR. La opcion \"{entrada}\" no es una entrada valida.")


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
      tuple: dos posiciones:
        - codigo de resultado (int): 
          0 en caso de ejecucion correcta, -1 en cualquier otro caso.
        - mensaje de ejecucion (str): 
          Mensaje para el usuario informando del resultado de la ejecucion 
          del metodo.
  """  
  # Local variables
  nombre_campos:list[str] = ["proyecto_nombre", "proyecto_descripcion"]
  campos:list[str] = [] # Lista de los campos validos proporcionados por el 
    # usuario.
  continuar:bool = True # Continuar con la ejecucion del bucle
  indice:int = 0 # Indice para iterar en un bucle
  retorno_otros:tuple = None # Tupla conteniendo el retorno de otros metodos


  # Local code
  # Pedir los campos
  while(indice < len(nombre_campos) and continuar):
    retorno_otros = utilidades.pedir_campo(peticiones_campos(indice)[2], nombre_campos[indice])


    if(retorno_otros[0] == -1):
      print(retorno_otros[1]) # Imprimir el mensaje de resultado solo en caso 
        # de error. En caso afirmativo, ya se ha mostrado.
      
      # Terminar la ejecucion del bucle
      continuar = False
    
    else: # Ejecucion correcta 
      campos.append(retorno_otros[2]) # anyadir a la lista de campos validos
      indice += 1 # Pedir el siguiente campo
  
  if(continuar): # Todos los campos pedidos son validos y han sido anyadidos
    # Hacer la query
    retorno_otros = query.query_insert_into("proyecto", ["nombre", "descripcion", "fecha_inicio", "fecha_fin"], [(f"\"{campos[0]}\"", f"\"{campos[1]}\"", "NOW()", "NOW()")])

    print(retorno_otros[2]) # Imprimir la query, solo debug

    # Ejecutar la instruccion
    retorno_otros = base_datos.ejecutar_instruccion(conexion, parametros_conexion, retorno_otros[2])

    print(retorno_otros[1]) # Imprimir mensaje, solo debug


    if(retorno_otros[0] == 0): # Insercion correcta
      retorno = (0, "Proyecto insertado en la base de datos.")
    
    else: # Insercion erronea
      retorno = (-1, retorno_otros[1]) # Devolver el menasje de error devuelto
        # de la ejecucion de la instruccion
  
  return retorno