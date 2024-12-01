# ############################################################################ #
#                                   IMPORT 
# ############################################################################ #
import os
import base_datos
import fichero
import utilidades
import empleado
import departamento
import proyecto


# ############################################################################ #
#                                   GLOBAL 
# ############################################################################ #


# ################################ Methods ################################ #
def iniciar_programa():
  """
  Inicializa el programa.

  En primer lugar comprueba el sistema operativo sobre el que esta ejecutandose
  el fichero .py, solo se acepta Windows y Linux / UNIX, por decision de 
  disenyo.

  En segundo lugar, se recupera el directorio de trabajo, que es el directorio
  que contiene al fichero .py, ademas del separador del sistema de ficheros.

  A continuacion, se intentan obtener los parametros para realziar la conexion
  a la base de datos. De no encontrarse, o no ser validos, la ejecucion 
  finaliza.

  Si se encuentran, se comprueba la instalacion de la libreria PyMySQL, de 
  estar instalad, la ejecucion continua intentando crear una conexion con el
  servidor de la base de datos.

  De resultar exitosa esta accion, la ejecuion puede tomar dos caminos en 
  funcion de si la base de datos existe o no. Para comprobar su existencia,
  se ejecuta la instruccion USE con el nombre de la base de datos.

  - En el caso de existir, se llama al menu principal.

  - En el caso de no existir, se intenta crear utilizando un "script" de creacion. Si esto es exitoso, se muestra el menu. En caso contrario,
    se finaliza la ejecucion del programa.
  """
  # Local variables
  nombre_base_datos = "GESTION_PROYECTOS"
  conector_presente:bool = False # Contiene si la libreria pymysql esta 
  # presente en el sistema.
  nombre_fichero:str = "cfg.ini" # Nombre del fichero de configuracion
    # que contiene los parametros para realizar una conexion al servidor
    # de la base de datos.
  retorno:tuple = None # Tupla conteniendo el retorno de ejecucion de otros
    # metodos.
  separador:str = None # Caracter separador de rutas del sistema de ficheros.
  directorio_trabajo:str = None # Ruta absoluta donde esta almacenado el fichero
    # .py; Contiene el separador al final.
  parametros:tuple = None # Parametros para realizar la conexion con el 
    # servidor de la base de datos: Usuario, Contrasenya y Puerto.
  conexion = None # Conexion con el servidor de la base de datos.
  llamar_menu:bool = False # Almacena si se llama al menu principal o se 
    # finaliza el programa

  

  # Local code
  print("\n"*2+"#"*60)
  print("Inicializando programa...")

  # ##### Comprobar sistema operativo #####
  print("\nComprobando el sistema operativo...")
  retorno = comprobar_sistema_operativo() # Comprobar el sistema operativo

  print(retorno[1]) # Imprimir el mensaje de retorno

  if(retorno[0] == 0): # Sistema operativo valido
    separador = retorno[2] # Asignar el separador a la variable

    # ##### Obtener el directorio de trabajo #####
    print("\nObteniendo el directorio de trabajo...")
    retorno = obtener_directorio_trabajo(separador) # Obtener el directorio
      # de trabajo
    
    print(retorno[1]) # Imprimir el mensaje de retorno

    if(retorno[0] == 0): # Directorio de trabajo obtenido
      directorio_trabajo = retorno[2] # Asignar el directorio de trabajo a la
        # variable
      
      # ##### Obtener configuracion de conexion #####
      print("\nObteniendo parametros de conexion al servidor de la base de datos....")
      retorno = obtener_parametros_conexion(directorio_trabajo, nombre_fichero)

      print(retorno[1]) # Imprimir el mensaje de retorno

      if(retorno[0] == 0): # Parametros obtenidos
        parametros = retorno[2] # Asignar parametros a la variable

        # ##### Instalacion de la libreria PyMySQL #####
        print("Comprobando instalacion del conector PyMySQL...")
        conector_presente = comprobar_instalacion_pymyqsl()

        if(not conector_presente): # La libreria no esta presente
          print("El conector PyMySQL no esta presente en el sistema.")
          print("Sin un conector a la base de datos, el programa no puede continuar")
          print("con la ejecucion.")
          print("\nPuede instalar el conector a traves de pip con el siguiente comando:")
          print("\t\tpip install PyMySQL")
          print("o puede consultar otras formas de instalacion en la documentacion")
          print("oficial del conector:")
          print("https://pymysql.readthedocs.io/en/latest/")
          print("\n"*2+"Terminando ejecucion del programa.")

        else: # Libreria presente
          print("\nConector PyMySQL presente en el sistema.")

          # ##### Realizar conexion al servidor de la base de datos #####
          # Comprueba si hay un servidor con los parametros especificados
          print("Intentando conectar con el servidor...")
          retorno = base_datos.crear_conexion(parametros[0], parametros[1], parametros[2], True)

          print(retorno[1]) # Imprimir mensaje de retorno

          if(retorno[0] == 0): # La conexion es correcta
            # Asignar la conexion a la variabñe
            conexion = retorno[2]

            # ##### Comprobar existencia de base de datos #####
            # Se realiza un use con el nombre de la base de datos, para 
            # comprobar su existencia.
            retorno = base_datos.ejecutar_instruccion(conexion, (parametros[0], parametros[1], parametros[2]), f"USE {nombre_base_datos}")

            print(retorno[1]) # Imprimir mensaje de retorno

            if(retorno[0] == 0): # La base de datos existe.
              print(f"\nLa base de datos {nombre_base_datos} esta presente y lista para utilizar.")
              llamar_menu = True # Incializacion correcta, llamar al menu
            
            else: # La base de datos no esta presente, crearla
              # ##### Crear Base de datos #####
              print("Creando la base de datos...")
              retorno = base_datos.crear_base_datos(conexion, nombre_base_datos, parametros)

              print(retorno[1]) # Imprimir mensaje de retorno

              if(retorno[0] == 0): # Base de datos creada correctamente
                llamar_menu = True
  

  if(llamar_menu): # La inicializacion del programa ha sido correcta
    print("\nInicializacion del programa terminada.")
    print("Cargando menu principal.")
    print("#"*60)
    menu(conexion, (parametros[0], parametros[1], parametros[2], nombre_base_datos))

  else: # Inicializacion erronea, terminar ejecucion
    print("#"*60)


# ######################################################################### #
def comprobar_sistema_operativo():
  """
  Comprueba que sistema operativo esta ejecutando el fichero .py.

  La comprobacion se realiza mediante el atributo name de la libreria os.

  Solo se aceptan sistema operativos Windows (nt), o sistemas operativos
  Linux / UNIX (posix). Esto es una decision de disenyo basada en los sistemas
  operativos a los que los desarrolladores tienen acceso.

  Returns:
      tuple: dos o tres posiciones:
        - codigo de retorno (int): 0 en caso de ejecucion correcta, -1 en
          cualquier otro caso.
        - mensaje de ejecucion (str): Mensaje para el usuario informando del
          retorno de la ejecucion del metodo.
        - separador (str): Caracter separador de rutas del sistema de ficheros.
  """
  # Local variables
  sistema_operativo:str = None # Almacena el nombre del sistema operativo
  # donde se esta ejecutando el fichero .py
  retorno:tuple = None # Tupla conteniendo la informacion necesaria para el 
  # retorno del metodo. 2 o 3 posiciones: Codigo ejecucion (0 - Correcta;
  # -1 incorrecta), mensaje de retorno de ejecucion, el separador del
  # sistema de ficheros: Opcional.


  # Local code
  # Obtener el sistema operativo de la maquina donde se esta ejecutando
  # el fichero python
  sistema_operativo = os.name

  if(sistema_operativo == "nt"): # Si es sistema operativo Windows
    retorno = (0, "\nSistema operativo Windows detectado.", os.sep)
  
  elif(sistema_operativo == "posix"): # Si es sistema operativo Linux / UNIX
    retorno = (0, "\nSistema operativo Linux / UNIX detectado.", os.sep)
  
  else: # Cualquier otro sistema operativo
    retorno = (-1, "\nERROR. El programa no soporta la ejecucion en el sistema "+
    f"operativo {sistema_operativo}.\n Terminando la ejecucion del programa.")
  
  return retorno


# ######################################################################### #
def obtener_directorio_trabajo(separador:str):
  """
  Obtiene el directorio de trabajo del programa.

  Se obtiene a traves de __file__. Tambien se podria obtener a traves de
  sys.argv[0].

  Se obtiene el path, se divide por el caracter separador del sistema de
  ficheros, y se recrea hasta el directorio que contiene el fichero.py

  Returns:
      tuple: Dos posiciones:
        - path del directorio (str): Ruta absoluta del directorio que
          contiene el fichero .py con el caracter separador al final.
        - mensaje de ejecucion (str): Mensaje para el usuario informando del
          retorno de la ejecucion del metodo.
  """
  # Local variables
  path:str = None # Ruta absoluta del fichero .py | Ruta al directorio que
  # contiene el fichero .py
  path_lista:list[str] # Path dividido por separador
  retorno:str # Tupla conteniendo la informacion necesaria para el 
  # retorno del metodo. 2 posiciones: path del directorio de trabajo.
  # Mensaje informativo al usuario de la ejecucion del metodo


  # Local code
  path = __file__ # Obtener el path. En condiciones normales no DEBE lanzar
  # ninguna excepcion

  path_lista = path.split(separador) # Dividir el path

  path = "" # Limpiar el valor de la variable path

  # Recrear el path hasta el directorio que contiene el fichero .py
  # Por motivos practicos, se deja el caracter separador en el ultimo 
  # directorio
  for i in range(0, len(path_lista)-1):
    path += path_lista[i]+separador

  # Crear el retorno del metodo, path y mensaje
  retorno = (0, "\nEl directorio de trabajo queda designado como: "+
          f"\"{path[0:len(path)-1]}\".", path)
  

  return retorno


# ######################################################################### #
def comprobar_instalacion_pymyqsl():
  """
  Comprueba si la libreria PyMySQL esta instalada en el sistema.

  Para comprobar la existencia de la libreria, se intenta realizar un import
  de la misma, gestionandolo con un try / except. En caso de que la libreria
  no este instalada se genera una excepcion y se cambia el valor de una
  variable booleana a False. Si resulta estar instalada, se cambia el valor
  de la variable booleana a True.

  No se puede evitar el lanzamiento de la exception.

  Returns:
      bool: True, Si la libreria lxml esta instalada, False, en cualquier 
      otro caso.
  """
  # Local variables
  instalado:bool = False # Si la libreria PyMySQL esta instalada su valor sera
  # True, en cualquier otro caso, sera False.


  # Local code
  try: # Intentar importar la libreria
    import pymysql
    # Si se llega hasta aqui, la libreria esta instalada
    instalado = True
  
  except ModuleNotFoundError as e: # Si la libreria no esta instalada, se lanza
    # una excepcion, y se cambia el valor a False.
    instalado = False
  
  return instalado


# ######################################################################### #
def obtener_parametros_conexion(directorio_trabajo:str, nombre_fichero:str):
  """
  Obtiene los parametros de conexion con la base de datos del fichero de
  configuracion.

  Args:
      directorio_trabajo (str): 
        Ruta absoluta del fichero que contiene al fichero.py, y donde debe
        estar localizado el fichero de configuracion.

      nombre_fichero (str):
        Fichero de configuracion conteniendo los parametros de la conexion
        al servidor de la base de datos.

  Returns:
      tuple: dos o tres posiciones:
        - codigo de resultado (int): 
          0 en caso de ejecucion correcta, -1 en cualquier otro caso.
        - mensaje de ejecucion (str): 
          Mensaje para el usuario informando del resultado de la ejecucion 
          del metodo.
        - parametros de la conexion (tuple, optional): 
          Tupla conteniendo los parametros de la conexion. 3 posiciones:
          Nombre del usuario, Contrasenya del usuario, puerto donde se
          encuentra ejecutando el servidor de la base de datos. Opcional.
        - 
  """  
  # Local variables
  retorno_otros:tuple = None # Tupla conteniendo el retorno de ejecucion de otros metodos.
  lineas:list[str] = None # Lista de lineas leidas del fichero
  indice:int = None # Indice para recorrer un bucle


  # Local code
  # Intentar leer el contenido del fichero
  retorno_otros = fichero.leer_fichero(directorio_trabajo, nombre_fichero)

  if(retorno_otros[0] == 0): # Si la lectura es correcta
    lineas = retorno_otros[2] # Asignar las lineas leidas a la variable

    # Eliminar lineas en blanco y comentarios ("# ")
    indice = len(lineas)-1

    while(indice >= 0): # Mientras existan lineas por comprobar
      # Eliminar caracteres en blanco
      lineas[indice] = lineas[indice].strip()

      # La linea esta en blanco o es un comentario:
      # Eliminar de la lista
      if(lineas[indice] == "" or lineas[indice]):
        lineas.pop(indice)
      
      # Mirar la siguiente linea
      indice -= 1
    
    # Tras recorrer la lista, comprobar si solo existe una unica linea
    if(len(lineas) == 1):
      # Solo hay una linea, dividirla por ;
      lineas = lineas[0].split(";")

      if(len(lineas) == 3): # Hay 3 posiciones, que corresponden con los tres
        # paramteros requeridos, no se puede comprobar su validez mas alla de 
        # esto.
        retorno = (0, "Parametros leidos del fichero exitosamente", (lineas[0], lineas[1], lineas[2]))
      
      else: # Algo es erroneo
        retorno = (-1, "Numero de parametros en el fichero incorrecto.")
    
    else: # Hay mas de una linea potencialmente valida
      retorno = (-1, "Numero de lineas potencialmente validas incorrecto.")
  
  return retorno


# ######################################################################### #
def menu(conexion, parametros_conexion:tuple):
  """
  Menu principal del programa.

  Imprime por salida estandar (Consola) el menu principal del programa, y pide
  al usuario la introduccion por entrada estandar (Teclado) del indice de la
  opcion que desea realizar. 
    - En caso de ser correcta, se redirige al menu correspondiente. 
    - Por el contrario, si es una opcion erronea se informa al 
  usuario del error.

  Para salir del menu, y por tanto del programa, se pide al usuario confirmar
  la accion.
  """
  # Local variables
  entrada:str = None # Caracteres introducidos por el usuario a traves de 
  # entrada estandar (Teclado).
  salir:bool = False # Almacena si el usuario quiere salir del programa (True)
  # o continuar con la ejecucion (False).

  # Local code
  while(not salir): # Iterar mientras que el usuario no confirme la salida
    # Imprimir menu
    print("\n"*2+"*"*60)
    print("Menu principal:")
    print("1 - Empleado.")
    print("2 - Departamento.")
    print("3 - Proyecto.")
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
    
    elif(entrada == "1"): # Menu Empleado
      empleado.menu_empleado(conexion, parametros_conexion)
      

    elif(entrada == "2"): # Menu Departamento
      departamento.menu_departameto(conexion, parametros_conexion)
    
    elif(entrada == "3"): # Menu proyecto
      proyecto.menu_proyecto(conexion, parametros_conexion)
    
    else: # Opcion erronea
      print(f"\nERROR. La opcion \"{entrada}\" no es una entrada valida.")


# ############################################################################ #
#                                    MAIN 
# ############################################################################ #
if __name__ == "__main__":
  # Local variables 
  
  # Local code
  iniciar_programa()
  