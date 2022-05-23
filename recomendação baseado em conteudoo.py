avaliacoesUsuario = {'Ana': 
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

avaliacoesFilme = {'Freddy x Jason': 
		{'Ana': 2.5, 
		 'Marcos:': 3.0 ,
		 'Pedro': 2.5, 
		 'Adriano': 3.0, 
		 'Janaina': 3.0 },
	 
	 'O Ultimato Bourne': 
		{'Ana': 3.5, 
		 'Marcos': 3.5,
		 'Pedro': 3.0, 
		 'Claudia': 3.5, 
		 'Adriano': 4.0, 
		 'Janaina': 4.0,
		 'Leonardo': 4.5 },
				 
	 'Star Trek': 
		{'Ana': 3.0, 
		 'Marcos:': 1.5,
		 'Claudia': 3.0, 
		 'Adriano': 2.0 },
	
	 'Exterminador do Futuro': 
		{'Ana': 3.5, 
		 'Marcos:': 5.0 ,
		 'Pedro': 3.5, 
		 'Claudia': 4.0, 
		 'Adriano': 3.0, 
		 'Janaina': 5.0,
		 'Leonardo': 4.0},
				 
	 'Norbit': 
		{'Ana': 2.5, 
		 'Marcos:': 3.0 ,
		 'Claudia': 2.5, 
		 'Adriano': 2.0, 
		 'Janaina': 3.5,
		 'Leonardo': 1.0},
				 
	 'Star Wars': 
		{'Ana': 3.0, 
		 'Marcos:': 3.5,
		 'Pedro': 4.0, 
		 'Claudia': 4.5, 
		 'Adriano': 3.0, 
		 'Janaina': 3.0}
}

from math import sqrt

def euclidiana(base, usuario1, usuario2):
	si = {}
	for item in base[usuario1]:
		if item in base[usuario2]: si[item] = 1

	if len(si) == 0: return 0

	soma = sum([pow(base[usuario1][item] - base[usuario2][item], 2)
		for item in base[usuario1] if item in base[usuario2]])
	return 1/(1 + sqrt(soma))

# print(euclidiana(avaliacoesUsuario, 'Ana', 'Pedro'))

def getSimilares(base, usuario):
	similaridade = [(euclidiana(base, usuario, outro), outro)
		for outro in base if outro != usuario]
	similaridade.sort()
	similaridade.reverse()
	return similaridade[0:30]

# print(getSimilares(avaliacoesFilme, 'Star Wars'))

def getRecomendacoesUsuario(base, usuario):
	totais = {}
	somarSimilaridade = {}
	for outro in base:
		if outro == usuario: continue
		similaridade = euclidiana(base, usuario, outro)

		if similaridade <= 0: continue

		for item in base[outro]:
			if item not in base[usuario]:
				totais.setdefault(item, 0)
				totais[item] += base[outro][item] * similaridade
				somarSimilaridade.setdefault(item, 0)
				somarSimilaridade[item] += similaridade
	rankings = [(total / somarSimilaridade[item], item) for item, total in totais.items()]
	rankings.sort()
	rankings.reverse()
	return rankings[0:30]

# print(getRecomendacoesUsuario(avaliacoesFilme, 'Star Wars'))

def carregarMovieLens(path='C:/ml-100k'):
	filmes = {}
	for linha in open(path + '/u.item'):
		(id, titulo) = linha.split('|')[0 : 2]
		filmes[id] = titulo
	# print(filmes)

	base = {}
	for linha in open(path + '/u.data'):
		(usuario, idFilme, nota, tempo) = linha.split('\t')
		base.setdefault(usuario, {})
		base[usuario][filmes[idFilme]] = float(nota)

	return base

baseDados = carregarMovieLens()

# print(getSimilares(baseDados, '69'))

# print(getRecomendacoesUsuario(baseDados, '90'))

def calculaItensSimilares(base):
	result = {}
	for item in base:
		notas = getSimilares(base, item)
		result[item] = notas
	return result

itensSimilares = calculaItensSimilares(avaliacoesFilme)

# print(itensSimilares)

def getRecomendacoesItens(baseUsuario, similaridadeItens, usuario):
	notasUsuario = baseUsuario[usuario]
	notas = {}
	totalSimilaridade = {}
	for (item, nota) in notasUsuario.items():
		for (similaridade, item2) in similaridadeItens[item]:
			if item2 in notasUsuario: continue
			notas.setdefault(item2, 0)
			notas[item2] += similaridade * nota
			totalSimilaridade.setdefault(item2, 0)
			totalSimilaridade[item2] += similaridade
	rankings = [(score/totalSimilaridade[item], item) for item, score in notas.items()]
	rankings.sort()
	rankings.reverse()
	return rankings

listaItens = calculaItensSimilares(avaliacoesFilme)

# print(getRecomendacoesItens(avaliacoesUsuario, listaItens, 'Pedro'))