avaliacoes = {'Ana': 
		{'Freddy x Jason': 2.5, 
		 'O Ultimato Bourne': 3.5,
		 'Star Trek': 3.0, 
		 'Exterminador do Futuro': 3.5, 
		 'Norbit': 2.5, 
		 'Star Wars': 3.0},
	 
	  'Marcos': 
		{'Freddy x Jason': 3.0, 
		 'O Ultimato Bourne': 3.5, 
		 'Star Trek': 1.5, 
		 'Exterminador do Futuro': 5.0, 
		 'Star Wars': 3.0, 
		 'Norbit': 3.5}, 

	  'Pedro': 
	    {'Freddy x Jason': 2.5, 
		 'O Ultimato Bourne': 3.0,
		 'Exterminador do Futuro': 3.5, 
		 'Star Wars': 4.0},
			 
	  'Claudia': 
		{'O Ultimato Bourne': 3.5, 
		 'Star Trek': 3.0,
		 'Star Wars': 4.5, 
		 'Exterminador do Futuro': 4.0, 
		 'Norbit': 2.5},
				 
	  'Adriano': 
		{'Freddy x Jason': 3.0, 
		 'O Ultimato Bourne': 4.0, 
		 'Star Trek': 2.0, 
		 'Exterminador do Futuro': 3.0, 
		 'Star Wars': 3.0,
		 'Norbit': 2.0}, 

	  'Janaina': 
	     {'Freddy x Jason': 3.0, 
	      'O Ultimato Bourne': 4.0,
	      'Star Wars': 3.0, 
	      'Exterminador do Futuro': 5.0, 
	      'Norbit': 3.5},
			  
	  'Leonardo': 
	    {'O Ultimato Bourne':4.5,
             'Norbit':1.0,
	     'Exterminador do Futuro':4.0}
}


from math import sqrt

def euclidiana(usuario1, usuario2):
	si = {}
	for item in avaliacoes[usuario1]:
		if item in avaliacoes[usuario2]: si[item] = 1

	if len(si) == 0: return 0

	soma = sum([pow(avaliacoes[usuario1][item] - avaliacoes[usuario2][item], 2)
		for item in avaliacoes[usuario1] if item in avaliacoes[usuario2]])
	return 1/(1 + sqrt(soma))

# print(euclidiana('Leonardo', 'Ana'))

def getSimilares(usuario):
	similaridade = [(euclidiana(usuario, outro), outro)
		for outro in avaliacoes if outro != usuario]
	similaridade.sort()
	similaridade.reverse()
	return similaridade

# print(getSimilares('Claudia'))

def getRecomendacoes(usuario):
	totais = {}
	somarSimilaridade = {}
	for outro in avaliacoes:
		if outro == usuario: continue
		similaridade = euclidiana(usuario, outro)

		if similaridade <= 0: continue

		for item in avaliacoes[outro]:
			if item not in avaliacoes[usuario]:
				totais.setdefault(item, 0)
				totais[item] += avaliacoes[outro][item] * similaridade
				somarSimilaridade.setdefault(item, 0)
				somarSimilaridade[item] += similaridade
	rankings = [(total / somarSimilaridade[item], item) for item, total in totais.items()]
	rankings.sort()
	rankings.reverse()
	return rankings

print(getRecomendacoes('Leonardo'))