#autor:Joao Vitor de Andrade Porto  RA170291
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from tkinter import *
#problema envolve avaliar a nota a partir da atencao que um aluno presta em aula e do quanto ele estuda em casa

#definicao de variaveis
atencao=ctrl.Antecedent(np.arange(0,11,1),'atencao')
estudo=ctrl.Antecedent(np.arange(0,11,1),'estudo')
nota=ctrl.Consequent(np.arange(0,11,1),'nota')

#funcao de pertinencia para atencao durante as aulas
atencao['baixa']=fuzz.trimf(atencao.universe,[0,0,5])
atencao['media']=fuzz.trapmf(atencao.universe,[3,4,6,8])
atencao['alta']=fuzz.gaussmf(atencao.universe,10,1.9)

#funcao de pertinencia para o estudo em casa
estudo['baixo']=fuzz.trapmf(estudo.universe,[0,0,1,4])
estudo['medio']=fuzz.gaussmf(estudo.universe,5,2)
estudo['alto']=fuzz.trimf(estudo.universe,[6,10,10])

#funcao de pertinencia para a aula
nota.automf(names=['baixa','media','alta'])

#definicao das regras
r1=ctrl.Rule(estudo['alto'] & atencao['alta'],nota['alta'])
r2=ctrl.Rule(estudo['baixo'] | atencao['baixa'],nota['baixa'])
r3=ctrl.Rule(estudo['medio'], nota['media'])
r4=ctrl.Rule(estudo['medio'] & atencao['alta'],nota['media'])
r5=ctrl.Rule(atencao['media'] & estudo['alto'],nota['media'])

#criacao do controlador e simulador
nota_ctrl=ctrl.ControlSystem([r1,r2,r3,r4,r5])
nota_simu=ctrl.ControlSystemSimulation(nota_ctrl)

#inicio da montagem da interface
it=Tk()

#funcao para ver o grafico contendo as funcoes relacioadas a atencao
def sAt():
    global atencao
    atencao.view()

#funcao para ver o grafico contendo as funcoes relacioadas ao estudo
def sEs():
    global estudo
    estudo.view()

#funcao para ver o grafico contendo as funcoes relacioadas a nota
def sNo():
    global nota
    nota.view()

#funcao geral para inserir os termos que o usuario digitou na simulacao e computar a mesma
def simula():
    global t1,t2,nota_simu
    nota_simu.input['atencao']=float(t1.get())
    nota_simu.input['estudo']=float(t2.get())
    nota_simu.compute()

#simulacao textual apresentando no campo de texto correspondente o resultadp
def simulat():
    global t3
    simula()
    t3.set(nota_simu.output['nota'])

#funcao para representar graficamente a parte da nota da simulacao
def simulaNo():
    simula()
    nota.view(sim=nota_simu)

#funcao para representar graficamente a parte da atencao da simulacao
def simulaAt():
    simula()
    atencao.view(sim=nota_simu)

#funcao para representar graficamente a parte do estudo da simulacao
def simulaEs():
    simula()
    estudo.view(sim=nota_simu)

#insercao dos componemtes na interface formando uma estrutura de 3 colunas
lp=Label(it,text="Funcoes de pertinencia")
ba=Button(it,text="Atencao",command=sAt)
be=Button(it,text="Estudo",command=sEs)
bn=Button(it,text="Nota",command=sNo)
ls=Label(it,text="Campos para teste")
lp.grid(column=1,row=0)
ba.grid(column=0,row=1)
be.grid(column=1,row=1)
bn.grid(column=2,row=1)
ls.grid(column=1,row=2)
#variaveis de string que serao usadas nos campos de texto para adquirir e alterar seus valores
t1=StringVar()
t2=StringVar()
t3=StringVar()
#inicializacao de todas em 0 para evitar possiveis erros vindos de mau uso do programa (simular sem preencher nada)
t1.set(0)
t2.set(0)
t3.set(0)
l1=Label(it,text="Digite o nível de atenção do aluno (de 0 a 10)")
e1=Entry(it,width=15,textvariable=t1)
l2=Label(it,text="Digite o nível de estudo do aluno (de 0 a 10)")
e2=Entry(it,width=15,textvariable=t2)
l3=Label(it,text="aqui está a nota simulada obtida do aluno (de 0 a 10)")
e3=Entry(it,width=15,textvariable=t3)
b1=Button(it,text="simular textualmente",command=simulat)
lw=Label(it,text="representacao grafica")
bnr=Button(it,text="Nota",command=simulaNo)
bar=Button(it,text="Atencao",command=simulaAt)
ber=Button(it,text="Estudo",command=simulaEs)
l1.grid(column=1,row=3)
e1.grid(column=1,row=4)
l2.grid(column=1,row=5)
e2.grid(column=1,row=6)
b1.grid(column=1,row=7)
l3.grid(column=1,row=8)
e3.grid(column=1,row=9)
lw.grid(column=1,row=10)
bar.grid(column=0,row=11)
ber.grid(column=1,row=11)
bnr.grid(column=2,row=11)
#loop para manter a interface aberta a todo momento ate o usuario fechar ela manualmente
it.mainloop()
