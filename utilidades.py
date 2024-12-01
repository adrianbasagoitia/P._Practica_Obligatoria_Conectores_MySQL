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