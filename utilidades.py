# ############################################################################ #
#                                   IMPORT 
# ############################################################################ #
import re
from re import Match, Pattern
import datetime

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
  "empleado_correo":  ["([A-Z0-9._]{1,80}(@MYSQL\\.COM)){1}"],
  "empleado_cargo":   ["[A-Z0-9.,;&\\-_ ]{1,60}"],
  "empleado_salario": ["[0-9]{1,9}([.][0-9]?[0-9])?", 1134.00, 999999999.99],

  "departamento_nombre":        ["[A-Z0-9.,;&\\- ]{1,60}"],
  "departamento_descripcion":   ["[A-Z0-9.,;&\\-_ ]{0,60}"],

  "proyecto_nombre":      ["[A-Z0-9.,;&\\- ]{1,60}"],
  "proyecto_descripcion": ["[A-Z0-9.,;&\\-_ ]{0,60}"],
  "general_fecha": ["((0?[1-9])|([12][0-9])|(3[0-1]))-((1[0-2])|(0?[1-9]))-[0-9]{1,4}"]
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
        retorno = (0, retorno_validar[1], retorno_validar[2])
    
    intentos -= 1 # Restar una unidad al numero de intentos
  
  if(intentos == 0 and not valido): # Numero maximo de intentos alcanzado y no
    # es un campo valido
    retorno = (-1, "\nNumero maximo de intentos alcanzado. Operacion cancelada.")

  return retorno


# ######################################################################### #
def validar_campo(campo:str, nombre_campo:str):
  """
  Valida el valor de un campo introducido por el usuario.

  En primer lugar obtiene el nombre del campo, para crear mensajes para el 
  usuario. Posteriormente, crea el Pattern y el Matcher en base a la expresion
  regular obtenida de obtener_expresion_regular a traves de nombreCampo.

  Posteriormente realiza un fullmatch de campo.
  - Si no es coincidente se crea la tupla conteniendo "-1" y el mensaje de 
    error.
  - Si coincide, se debe comprobar si hay que realizar comprobaciones 
    adicionales, es decir, es un campo numerico. Se realiza un casting del 
    campo a double y se comprueba con los valores minimo y maximo obtenidos de 
    obtener_expresion_regular. Si no esta entre los valores, se crea un mensaje 
    de error personalizado para el usuario. En otro caso, el campo es valido.

  Args:
      campo (str): 
        Cadena de caracteres introducida por el usuario para comprobar su 
        validez.
      
      nombreCampo (str): 
        Nombre del campo que se tiene que validar. Sirve para obtener la 
        expresion regular que se ha de utilizar para validar el campo.
        DEBE ser una de las claves del diccionario almacenado en 
        obtener_expresion_regular. Se da por hecho de que SIEMPRE sera una 
        clave valida.

  Returns:
      tuple: dos o tres posiciones:
        - codigo de retorno (int): 
          0 en caso de ejecucion correcta, -1 en cualquier otro caso.
        - mensaje de ejecucion (str): 
          Mensaje para el usuario informando del retorno de la ejecucion del 
          metodo.
        - campo (str, optional): 
          El campo introducido por el usuario en caso de ser valido. Es 
          opcional.
  """
  # Local variables
  caracteristicas:list = None # Las caracteristicas del campo, tiene 1 o 3 
  # posiciones: 0 - Expresion regular, 1 - Valor minimo, 2 - Valor maximo
  pattern:Pattern = None # Patron que almacena la expresion regular para validar
  # el campo compilada.
  matcher:Match = None # Objeto devuelto despues de validar el campo con 
  # el Pattern. Si no es valido su valor no cambia.
  retorno_expresion:tuple = None # Tupla que almacena el retorno de
  # obtener_expresion_regular
  campo_t:str = None # Almacena el nombre del campo pedido. Ej: titulo, autor.
  retorno:tuple = None # Tupla conteniendo la informacion necesaria para el 
  # retorno del metodo. 2 o 3 posiciones: Codigo ejecucion (0 - Correcta;
  # -1 incorrecta), mensaje de retorno de ejecucion, campo introducido
  # por el usuario si es valido: Opcional.

  # Local code
  # Obtener el nombre del campo
  campo_t = nombre_campo.split("_")[1]

  # Intentar obtener expresion regular
  retorno_expresion = obtener_expresion_regular(nombre_campo)

  if(retorno_expresion[0] != 0): # Si la expresion no ha sido obtenida
    retorno = (-1, retorno_expresion[1])
  
  else: # La expresion ha sido obtenida
    caracteristicas = retorno_expresion[2]

    # Crear el patron, se utiliza la primera posicion de la lista caracteristicas
    # El caracter ^ se utiliza para que compruebe el inicio de la linea
    # El caracter $ se utiliza para que compruebe el final de la linea
    pattern = re.compile("^"+caracteristicas[0]+"$")
    
    # Comprobar que el patron coincide totalmente
    matcher = pattern.fullmatch(campo)

    if(matcher is not None): # El campo es valido
      # Comprobar si hay que realizar comprobaciones adicionales
      if(campo_t == "fecha"): # Si el campo es una fecha, validarla a parte
        retorno = validar_fecha(campo)
      elif(len(caracteristicas) == 3): # Campo numerico
        campo_num = float(campo) # Se realiza el casting a float por simplicidad,
        # Se puede comparar numeros decimales con numeros enteros.

        # Comprobar valores del campo
        if(campo_num >= caracteristicas[1] and campo_num <= caracteristicas[2]):
          # Campo correcto
          retorno = (0, f"El {campo_t} \"{campo}\" es valido.", campo)

        elif(campo_num < caracteristicas[1]): # Menor que valorMinimo
          retorno = (-1, f"\nEl {campo_t} tiene un valor menor al aceptado. {campo_num} < {caracteristicas[1]}.")

        elif(campo_num > caracteristicas[2]): # Mayor que valor maximo
          retorno = (-1, f"\nEl {campo_t} tiene un valor mayor al aceptado. {campo_num} > {caracteristicas[2]}.")
        
      elif(len(caracteristicas) == 1): # Campo Texto. 
        # No hay que hacer comprobaciones adicionales
        retorno = (0, f"\nEl {campo_t}: \"{campo}\" es valido.", campo)
    
    else: # El campo no es valido
      retorno = (-1, f"\nEl valor \"{campo}\" no es valido para {campo_t}.")

  return retorno


# ######################################################################### #
def pedir_confirmacion(mensaje:str):
  """
  Pide confirmacion al usuario para realizar una operacion.

  Imprime un mensaje por salida estandar (Consola) personalizado para cada 
  accion. Si el usuario introduce s o si, la operacion esta confirmada. 
  En cualquier otro caso, la operacion no se confirma.

  Args:
      mensaje (str): 
        Contiene un mensaje personalizado para pedir la confirmacion de la 
        operacion. Ej: ¿Quiere salir del programa?.

  Returns:
      bool: Devuelve True si el usuario ha confirmado la opcion, False en
      cualquier otro caso.
  """
  # Local variables
  confirmado:bool = False # Almacena si el usuario ha confirmado la operacion.
  entrada:str = None # Caracteres introducidos por el usuario a traves de 
  # entrada estandar (Teclado).


  # Local code
  # Pedir confirmacion al usuario. Se quitan espacion en blanco al inicio
  # y al final y se pasa a minuscula
  entrada = input(mensaje+" (s / Otro caracter): ").strip().lower()

  # Si el usuario introduce s o si, confirma la operacion
  if(entrada == "si" or entrada == "s"):
    confirmado = True
  
  # Devolver resultado
  return confirmado


# ######################################################################### #
def validar_fecha(campo:str, fecha_igual_superior:bool = True):
  """
  Valida una fecha introducida por el usuario.

  A traves de la libreria datetime, se valida la fecha introducida por el
  usuario, comprobando limites numericos y anyos bisiestos.

  Si se anyade la comprobacion de fecha_igual_superior se valida que la fecha
  introducida sea igual o superior a la del dia actual donde se este ejecutando
  el programa python.

  Referencias:
      https://www.geeksforgeeks.org/create-python-datetime-from-string/
      https://www.geeksforgeeks.org/comparing-dates-python/
      https://www.geeksforgeeks.org/formatting-dates-in-python/

  Args:
      campo (str): 
        Fecha introducida por el usuario que sigue el formato dd-mm-aaaa

      fecha_igual_superior (bool, optional):
        Indica si la fecha introducida debe ser igual o superior a la actual 
        del sistema donde se esta ejecutando el programa python.

  Returns:
      tuple: dos o tres posiciones:
        - codigo de retorno (int): 
          0 en caso de ejecucion correcta, -1 en cualquier otro caso.
        - mensaje de ejecucion (str): 
          Mensaje para el usuario informando del retorno de la ejecucion del 
          metodo.
        - fecha (str, optional): 
          Un cadena de caracteres conteniendo una fecha valida en formato
          americano yyyy-mm-dd. Es opcional.
  """  

  # Local variables
  retorno:tuple = None # Tupla conteniendo la informacion necesaria para el 
  # retorno del metodo. 2 o 3 posiciones: Codigo ejecucion (0 - Correcta;
  # -1 incorrecta), mensaje de retorno de ejecucion, fecha valida preparada 
  # para insertar en la base de datos(Opcional)
  fecha:datetime = None # Fecha valida


  # Local code
  try:
    # Convertir la fecha a datetime.date
    # Automaticamente al imprimir el objeto, se imprime como
    # formato americano aceptado por la base e datos
    fecha = datetime.datetime.strptime(campo, "%d-%m-%Y").date()

    if(fecha_igual_superior): # La fecha debe ser superior a la actual
      if(fecha >= datetime.datetime.now().date()): # Comparar con la fecha 
        # actual
        retorno = (0, "Fecha valida", str(fecha))
      
      else: # La fecha no cumple los requisitos
        retorno = (-1, "La fecha no es superior a la actual")
    
    else: # Sin comprobaciones adicionales
      retorno = (0, "Fecha valida", str(fecha))


  except Exception as e: # Si se lanza algun error
    print(e)
    retorno = (-1, "La fecha no es valida.")
  
  return retorno