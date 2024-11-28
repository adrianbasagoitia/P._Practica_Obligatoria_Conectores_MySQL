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


# ############################################################################ #
#                                    MAIN 
# ############################################################################ #
if __name__ == "__main__":
  # Local variables 
  
  # Local code
  pass
  