#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  simpy-tutorial.py

import random # módulo gerador de números aleatórios
import simpy # biblioteca de simulação

TEMPO_MEDIO_CHEGADAS = 1.0 #taxa média entre duas chegadas sucessivas
TEMPO_MEDIO_ATENDIMENTO = 0.5 #tempo médio de atendimento no servidor

def geraChegadas(env, nome, servidorRes):
	#função que gera chegadas de entidades no sistema, a uma taxa definida pela variável TEMPO_MEDIO_CHEGADAS
	contaChegada = 0
	while True:
		#random.expovariate gera intervalos de tempo exponencialmente distribuídos --> 1.0/taxa
		yield env.timeout(random.expovariate(lambd=1.0/TEMPO_MEDIO_CHEGADAS)) # yield retorna um gerador que causa um atraso de tempo definido por env.timeout
		contaChegada += 1 # contador
		print "\n%.2f %s %i chegou ao sistema" %(env.now, nome, contaChegada) 
		env.process(atendimentoServidor(env, nome + " " + str(contaChegada), servidorRes)) #inicia o processo de atendimento (função atendimentoServidor)

def atendimentoServidor(env, nome, servidor):
	request = servidor.request() #realiza uma requisição para utilizar o servidor
	
	yield request #aguarda até a liberação do recurso
	
	print "%.2f Servidor inicia o atendimento do %s" %(env.now, nome)
	
	yield env.timeout(TEMPO_MEDIO_ATENDIMENTO) #causa um atraso de tempo (env.timeout) de 0.5
	
	print "%.2f Servidor termina o atendimento do %s" %(env.now, nome)
	
	yield servidor.release(request) #libera o recurso que estava ocupado


random.seed(1000) #semente para o gerador de números aleatórios, garante a sequência de números gerados será sempre a mesma
env = simpy.Environment() # variável que representa o ambiente de simulação do SimPy
servidorRes = simpy.Resource(env, capacity=2) #cria o recurso a ser ocupado pelas entidades
env.process(geraChegadas(env, "Cliente", servidorRes)) # cria o processo de chegadas definido pela função "geraChegadas"
env.run(until=5) # executa a simulação por 5 unidades de tempo
