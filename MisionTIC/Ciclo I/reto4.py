import os
import time

contactos=[]

def agregarContacto(nombre,celular,cumpleanos,email):
    contactos.append({"Nombre":nombre,"Celular":celular,"Cumpleanos":cumpleanos,"Email":email})

def buscarContacto():
    print('Agenda de contactos MisionTIC 2022')
    print('**************************************************')
    print('**************************************************')
    print('Buscar Contacto')
    print('**************************************************')
    contacto=input('Ingrese el nombre del contacto a buscar:')
    for i in range(len(contactos)):
        if contacto in contactos[i].values():
            print(contactos[i])
        else:
            print('¡Contacto no encontrado!')
    print('**************************************************')
    input('Ingrese enter para volver al menú principal')
    os.system("cls")
    
def visualizarTodos():
    print('Agenda de contactos MisionTIC 2022')
    print('**************************************************')
    print('**************************************************')
    print('Visualizar Contactos')
    print('**************************************************')
    for i in range(len(contactos)):
        print(contactos[i])
    print('**************************************************')
    input('Ingrese enter para volver al menú principal')
    os.system("cls")
    
def solicitarCumpleanos():
    while(True):
        try:
            dia=int(input('Ingrese el día de nacimiento:'))
        except:
            print('Ingrese un valor válido')
        else:
            if 1<=dia<=31:
                break
            else:
                print('Ingrese un valor válido')
    
    while(True):
        try:
            mes=int(input('Ingrese el mes de nacimiento:'))
        except:
            print('Ingrese un valor válido')
        else:
            if 1<=mes<=12:
                break
            else:
                print('Ingrese un valor válido')
    
    while(True):
        try:
            ano=int(input('Ingrese el año de nacimiento:'))
        except:
            print('Ingrese un valor válido')
        else:
            if 1<=2021-ano<=100:
                break
            else:
                print('Ingrese un valor válido')
    cumpleanos=(dia,mes,ano)
    return cumpleanos

def solicitarDatos():
    print('Agenda de contactos MisionTIC 2022')
    print('**************************************************')
    print('**************************************************')
    print('Agregar contacto nuevo')
    print('**************************************************')
    nombre=input('Ingrese el nombre del contacto:')
    celular=input('Ingrese el número de celular del contacto:')
    cumpleanos=solicitarCumpleanos()
    email=input('Ingrese el email del contacto:')
    agregarContacto(nombre,celular,cumpleanos,email)
    print('**************************************************')
    print('Contacto agregado satisfactoriamente')
    print('**************************************************')
    time.sleep(3)

def pintarMenu():
    print('Agenda de contactos MisionTIC 2022')
    print('**************************************************')
    print('**************************************************')
    print('[A]gregar Contacto')
    print('[B]uscar Contacto')
    print('[V]isualizar todos los contactos')
    print('[S]alir del programa')
    print('**************************************************')
    print('**************************************************')
    opcion=input('Seleccione una opción:')
    return opcion

def main():
    while(True):
        opcion=pintarMenu()	
        if opcion=='A' or opcion=='a':
            os.system('cls')
            solicitarDatos()
            os.system('cls')
        elif opcion=='B' or opcion=='b':
            os.system('cls')
            buscarContacto()
            os.system('cls')
        elif opcion=='V' or opcion=='v':
            os.system('cls')
            visualizarTodos()
            os.system('cls')
        elif opcion=='S' or opcion=='s':
            os.system('cls')
            break
        else:
            print('Ingrese un valor válido')
            time.sleep(3)
            os.system("cls")
            
if __name__=="__main__":
	main()
