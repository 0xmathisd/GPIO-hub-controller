import subprocess, sys, time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

color_green,color_cyan,color_red,color_yellow,color_end='\033[32m','\033[36m','\033[31m','\033[33m','\033[0m'
ports_first_generation=[[2,4],[1,17],[6,9,14,20,25]]
ports_second_generation=[[2,4],[1,17],[6,9,14,20,25,30,34,39]]
#__________________________5v_____3v___________ground__________

var_help=['--help','-help','help','--manual','-manual']
port="None"
etat="None"
ports=40

status=["Pas d'erreurs détectées !",True]

var_for=[False,0]
var_flicker=[False,0,0,0]


print("","-"*57,"\n|        "+color_green+"GPIO hub controller |  For all raspberry pi  "+color_end+"    |\n","-"*57)
print("|       "+color_cyan+"            version:    2.2            "+color_end+"           |\n|     "+color_cyan+"              author:     petitcroco            "+color_end+"    |\n","-"*57)

if ("-pinout" in sys.argv):
	print("*"*26, "pinout", "*"*25)
	print(subprocess.call(['pinout', '--color']))
	exit()

for arg in var_help:
	if arg in sys.argv:
		print("|             "+color_red+"            Usage :            "+color_end+"             |")
		print("| $ python3 gestion.py [broche] [on/off]                  |")
		print(" "+"-"*(57))
		print("| -pinout:  Details de sortie des broches GPIO disponibles|")
		print("| -pins:40  Rasp Pi avec GPIO a 40 pins  [par default]    |")
		print("| -pins:26  Rasp Pi avec GPIO a 26 pins (1er generation)  |")
		print("| -force  Forcer l'utilisation des broches: 5v,3v3,Ground |")
		print("| -setmode:BOARD  se réferer par le numéro de la broche du|\n|                connecteur [par default]                 |")
		print("| -setmode:BCM  se réferer par le numéro 'Broadcom SOC    |\n|              channel' soit les numéro associé au GPIO   |\n")
		print("| -for [secondes]  met dans l'état [on/off] choisi pendant|\n|                 le délai et reviens à l'état initial    |\n")
		print("| -flicker:[mode] [secondes]  alterne l'état [on/off]     |\n|                 pendant le délai et en fonction du mode:|\n")
		print("|          -flicker:min toutes les 1.5 secondes           |",)
		print("|          -flicker:med toutes les 0.9 secondes           |")
		print("|          -flicker:max toutes les 0.3 secondes           |\n","-"*57)
		exit()

if ("on" in sys.argv):
	etat='on'
if ("off" in sys.argv):
	etat='off'

if ("-setmode:BCM" in sys.argv):
	GPIO.setmode(GPIO.BCM)
	for i in range(40):
		try:
			if (str(i+1)==sys.argv[0]) or (str(i+1)==sys.argv[1]) or (str(i+1)==sys.argv[2]):
				port=i+1
		except:
			port="None"
else:
	GPIO.setmode(GPIO.BOARD)
	if ("-pins:26" in sys.argv):
		ports=26
		for i in range(26):
			try:
				if (str(i+1)==sys.argv[0]) or (str(i+1)==sys.argv[1]) or (str(i+1)==sys.argv[2]):
					port=i+1
					if ("-force" not in sys.argv):
						if (port in ports_first_generation[0]):
							status=["Le port choisi est une alimentation 5v !", False]
						if (port in ports_first_generation[1]):
							status=["Le port choisi est une alimentation 3.3v !", False]
						if (port in ports_first_generation[2]):
							status=["Le port choisis est la masse !(use -pinout)", False]
			except:
				port="None"
	else:
		for i in range(40):
			try:
				if (str(i+1)==sys.argv[0]) or (str(i+1)==sys.argv[1]) or (str(i+1)==sys.argv[2]):
					port=i+1
					if ("-force" not in sys.argv):
						if (port in ports_second_generation[0]):
							status=["Le port choisi est une alimentation 5v !", False]
						if (port in ports_second_generation[1]):
							status=["Le port choisi est une alimentation 3.3v !", False]
						if (port in ports_second_generation[2]):
							status=["Le port choisis est la masse !(use -pinout)", False]
			except:
				port="None"

# '-for'
for i in range (len(sys.argv)):
	if (sys.argv[i]=='-for'):
		var_for[0]=i

try:
	if var_for[0]>=1:
		var_for[1]=sys.argv[var_for[0]+1]

except:
	status=["'-for:' est utilisé sans attribut !", False]

for i in range (len(sys.argv)):
	if (sys.argv[i]=='-flicker:min'):
		var_flicker=[i,"'min'",0,1500]

	if (sys.argv[i]=='-flicker:med'):
		var_flicker=[i,"'med'",0,900]

	if (sys.argv[i]=='-flicker:max'):
		var_flicker=[i,"'max'",0,300]

	if (sys.argv[i]=='-flicker') or (sys.argv[i]=='-flicker:'):
		status=["'-flicker:[mode]' est utilisé sans mode !", False]

try:
	if var_flicker[0]>=1:
		var_flicker[2]=sys.argv[var_flicker[0]+1]

except:
	status=["'-flicker:"+var_flicker[1]+" est utilisé sans attribut !", False]

print("|          "+color_red+"               Execution               "+color_end+"        |"+color_yellow)
print(" nombre total de broches sur l'appareil :",ports)
if GPIO.getmode()==10:
	print(" mode: BOARD -> 10")
elif GPIO.getmode()==11:
	print(" mode : BCM -> 11")
print(" port:",port,"\n état:",etat,"")

if var_for[0]!=False:
	print(" mode -for activé:")
	print("   pendant",var_for[1],"seconde(s)"+color_end)

if var_flicker[0]!=False:
	print(" mode -flicker activé avec la fonction",var_flicker[1],":")
	print("   pendant",var_flicker[2],"seconde(s)"+color_end)

if (var_flicker[0]!=False) and (var_for[0]!=False):
    status=["'-flicker' et '-for' à la fois !", False]

if port=="None":
	status=["Le port n'est pas donné ou incorrect !", False]

if ((etat!="on") and (etat!="off")):
	if var_flicker[0]==False:
		status=["variable [on/off] non déclarée ou incorrecte !", False]

if ((etat!="on") and (etat!="off")) and port=="None":
	status=["Aucun arguments n'est donné !", False]

if status[1]==True:
	print("\n  \033[7;40;32mrendering : "+status[0]+color_end+"\n","-"*57)
	GPIO.setup(port, GPIO.OUT)
	if (var_flicker[0]!=False):
		for i in range (int(int(var_flicker[2])/int(var_flicker[3])*500)):
			GPIO.output(port, 1)
			time.sleep(var_flicker[3]/1000)
			GPIO.output(port, 0)
			time.sleep(var_flicker[3]/1000)

		print(" "*6+"Try '--help' or '--manual' for more information\n\n\n\n")
		exit()

	elif ("-for" in sys.argv):
		var_for[0]=GPIO.input(port)
		if (var_for[0]==0):
			if etat=="on":
				GPIO.output(port, 1)
		else:
			if etat=="off":
				GPIO.output(port,0)
		time.sleep(int(var_for[1]))
		GPIO.output(port, var_for[0])
	else:
		if etat=="on":
			GPIO.output(port, 1)
		if etat=="off":
			GPIO.output(port,0)

else:
	print("\n  \033[7;40;31mrendering : "+status[0]+color_end+"\n","-"*57)

print(" "*6+"Try '--help' or '--manual' for more information\n\n\n\n")
