# ############################################################################ #
#                                   IMPORT 
# ############################################################################ #
import utilidades
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