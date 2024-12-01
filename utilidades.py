# ############################################################################ #
#                                   IMPORT 
# ############################################################################ #


# ############################################################################ #
#                                   GLOBAL 
# ############################################################################ #


# ################################ Methods ################################ #
def obtener_expresion_regular(clave:str):
  """
  Almacena las expresiones regulares para la validacion de campos del programa.

  Dado el nombre del campo del parametro, se intenta buscar en el diccionario
  contenido como variable local el nombre del campo como clave.

  Args:
      clave (str): 
        Nombre del campo que es la clave en el diccionario.

  Returns:
      tuple: dos o tres posiciones:
        - codigo de retorno (int): 0 en caso de ejecucion correcta, -1 en
          cualquier otro caso.
        - mensaje de ejecucion (str): Mensaje para el usuario informando del
          retorno de la ejecucion del metodo.
        - expresion_regular (list): La expresion regular para validar el campo
          pedido y opcionalmente valores minimo y maximo aceptados.
  """
  # Local variables
  expresion:str = None # Expresion regular pedida por el usuario
  expresiones_regulares:dict[str, str] = {
  "empleado_nombre":  ["[A-Z0-9.,;&\\- ]{1,120}"],
  "empleado_correo":  ["([A-Z0-9._]{1,80}(@MYSQL\.COM)){1}"],
  "empleado_cargo":   ["[A-Z0-9.,;&\\-_ ]{1,60}"],
  "empleado_salario": ["[0-9]{1,9}([.][0-9]?[0-9])?", 0.01, 999999999.99],

  "departamento_nombre":        ["[A-Z0-9.,;&\\- ]{1,60}"],
  "departamento_descripcion":   ["[A-Z0-9.,;&\\-_ ]{0,60}"],

  "proyecto_nombre":      ["[A-Z0-9.,;&\\- ]{1,60}"],
  "proyecto_descripcion": ["[A-Z0-9.,;&\\-_ ]{0,60}"]
  } # Diccionario que contiene las expresiones regulares para la validacion de
    # campos del programa.
    #  - La clave es un String (str), conteniento el nombre del campo a 
    #    validar. Se compone del tipo de "objeto" del campo a validar, seguido 
    #    del caracter '_' y por ultimo el nombre del campo a validar. Ej: 
    #    disco_titulo; venta_DNI.
    #  - El valor es un String (str), que contiene la expresion regular para 
    #    validar el campo.


  # Local code
  # Intentar obtener la expresion pedida
  expresion = expresiones_regulares.get(clave)

  if(expresion is None): # Si el nombre del campo no existe en el diccionario
    retorno = (-1, "El campo pedido no existe.")
  
  else: # Si esta contenido en el diccionario
    retorno = (0, "Campo valido", expresion)


  return retorno


# ######################################################################### #
def pedir_campo(mensaje:str, nombre_campo:str):
  """
  Pide al usuario el valor de un campo.

  El metodo realiza un bucle, un maximo de cinco veces. En el mismo, se 
  imprime por salida estandar (Consola) al usuario un mensaje para la peticion
  de un campo. El usuario, debe introducir el valor del mismo por entrada
  estandar (Teclado).

  La operacion, se puede cancelar por el usuario introduciendo "-1". Si el 
  usuario no cancela la operacion, se procede a validar el campo en otro metodo.

  En cualquier resultado de la validacion, se imprime al usuario un mensaje
  indicando lo sucedido. Ej: Campo valido, Campo erroneo, ...

  Args:
      mensaje (str): 
        Mensaje personalizado para la peticion del campo. Se imprime
        por salida estandar (Consola) para que el usuario tenga informacion de 
        que debe introducir.

      nombre_campo (str): 
        El nombre del campo que se esta introduciendo, sirve para        
        posteriormente validar el valor introducido por el usuario.

  Returns:
      tuple: dos o tres posiciones:
        - codigo de retorno (int): 
          0 en caso de ejecucion correcta, -1 en cualquier otro caso.
        - mensaje de ejecucion (str): 
          Mensaje para el usuario informando del retorno de la ejecucion del 
          metodo.
        - campo (str, optional): 
          El campo introducido por el usuario en caso de ser valido, es 
          opcional.
  """
  # Local variables
  entrada:str = None # Caracteres introducidos por el usuario a traves de 
  # entrada estandar (Teclado).
  intentos:int = 5 # Numero de intentos restantes que tiene el 
  # usuario para introducir un valor correcto para el campo pedido.
  valido:bool = False # Guarda si el campo introducido es valido o no.
  retorno_validar:tuple = None # Tupla conteniendo la informacion del retorno
  # del metodo validar_campo
  retorno:tuple = None # Tupla conteniendo la informacion necesaria para el 
  # retorno del metodo. 2 o 3 posiciones: Codigo ejecucion (0 - Correcta;
  # -1 incorrecta), mensaje de retorno de ejecucion, campo introducido
  # por el usuario: Opcional.


  # Local code
  while(not valido and intentos > 0): # Iterar mientras el campo no sea valido
    # y existen intentos

    # Pedir valor del campo al usuario. Por comodidad y para evitar problemas 
    # con sistemas sensibles a mayusculas y minusculas, toda letra almacenada 
    # sera una letra mayuscula.
    entrada = input(mensaje+f"(-1 para cancelar)\n{intentos} intentos restantes: ").strip().upper()

    if(entrada == "-1"): # El usuario cancela la operacion
      # Cambiar valor de booleano para salir del bucle y construir tupla
      valido = True
      retorno = (-1, "\nOperacion cancelada por el usuario.")
    
    else: # Validar el campo introducido por el usuario
      retorno_validar = validar_campo(entrada, nombre_campo)

      print(retorno_validar[1]) # En todo caso, imprimir mensaje

      if(retorno_validar[0] != -1): # El campo es valido
        # Cambiar valor de booleano para salir del bucle y construir tupla
        valido = True
        retorno = (0, retorno_validar[1], entrada)
    
    intentos -= 1 # Restar una unidad al numero de intentos
  
  if(intentos == 0 and not valido): # Numero maximo de intentos alcanzado y no
    # es un campo valido
    retorno = (-1, "\nNumero maximo de intentos alcanzado. Operacion cancelada.")

  return retorno
