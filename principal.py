# ############################################################################ #
#                                   IMPORT 
# ############################################################################ #


# ############################################################################ #
#                                   GLOBAL 
# ############################################################################ #


# ################################ Methods ################################ #
def iniciar_programa():
  # Local variables
  conector_presente:bool = False # Contiene si la libreria pymysql esta 
  # presente en el sistema.


  # Local code
  print("\n"*2+"#"*60)
  print("Inicializando programa...")

  # Comprobar instalacion de pymsql
  print("Comprobando instalacion del conector PyMySQL...")
  conector_presente = comprobar_instalacion_pymyqsl()

  if(conector_presente):
    print("\nConector PyMySQL presente en el sistema.")
  
  else:
    print("El conector PyMySQL no esta presente en el sistema.")
    print("Sin un conector a la base de datos, el programa no puede continuar")
    print("con la ejecucion.")
    print("\nPuede instalar el conector a traves de pip con el siguiente comando:")
    print("pip install PyMySQL")
    print("o puede consultar otras formas de instalacion en la documentacion")
    print("oficial del conector:")
    print("https://pymysql.readthedocs.io/en/latest/")

    print("\n"*2+"Terminando ejecucion del programa."+"\n"+"#"*60, end=" ")


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


# ############################################################################ #
#                                    MAIN 
# ############################################################################ #
if __name__ == "__main__":
  # Local variables 
  
  # Local code
  pass
  