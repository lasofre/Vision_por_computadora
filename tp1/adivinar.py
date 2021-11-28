import random as rn
def adivinar(intentos):
	num=rn.randint(0,100)
	for i in range(intentos-1,-1,-1):
		num_c=int(input('Ingrese un entero: '))
		if num_c==num:
			print("Felicitaciones!! Adivinó el número en el intento "+str(intentos-i)+".")
			break
		else:
			print("Lo siento le quedan "+str(i)+" intentos.")

