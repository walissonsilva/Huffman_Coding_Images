import cv2
import matplotlib.pyplot as plt
import numpy as np
from sys import getsizeof
from math import log
import subprocess

img = cv2.imread('Imagens/tux.png', cv2.IMREAD_GRAYSCALE)
#img = cv2.imread('Imagens/paisagem.jpg', cv2.IMREAD_GRAYSCALE)

cv2.namedWindow('Imagem', cv2.WINDOW_AUTOSIZE)
cv2.imshow('Imagem', img)
cv2.waitKey()
cv2.destroyWindow('Imagem')

# PLOTANDO O HISTOGRAMA
plt.hist(img.ravel(),256,[0,256]);
plt.show()

# CRIANDO UM VETOR COM O HISTOGRAMA
img_list = img.tolist()
histograma = [0] * 256

for x in range(img.shape[0]):
	for num in range(256):
		histograma[num] += img_list[x].count(num)

# CRIANDO UM VETOR COM AS PROBABILIDADES DE OCORRÊNCIA DE CADA INTENSIDADE DE CINZA
prob = []
for i in range(256):
	prob.append(histograma[i] / (img.shape[0] * img.shape[1])) 

# CALCULANDO A ENTROPIA DA IMAGEM, ANTES DA CODIFICAÇÃO
entropy = 0
for i in range(256):
	if (prob[i] != 0):
		entropy -= (prob[i] * log(prob[i], 2))

# CALCULANDO O COMPRIMENTO MÉDIO DO CÓDIGO, ANTES DA CODIFICAÇÃO
comp_medio = 0
for i in range(256):
	comp_medio += (prob[i] * 8)

file = open('Arquivos/IMG.txt', 'w')

for i in range(256):
	file.write("%d %d" % (i, histograma[i]))
	file.write('\n')
file.close()


########## CODIFICAÇÃO ###########
print("Executando a codificação...")
r = subprocess.call(["./Huffman",])
print("Codificação concluída!")

file = open("Arquivos/encoded.txt", 'r')

# CALCULANDO O NOVO COMPRIMENTO MÉDIO DO CÓDIGO
comprimento_huffman = [0] * 256

for line in file:
	pos = line.find(':')
	comprimento_huffman[int(line[0:pos])] = len(line[pos + 2:-1])
	#print("%d %d" % (int(line[0:pos]), comprimento_huffman[int(line[0:pos])]))

comp_medio_huffman = 0
for i in range(256):
	comp_medio_huffman += (prob[i] * comprimento_huffman[i])


# IMPRIMINDO AS INFORMAÇÕES GERAIS #
print('\n############## ANTES DA CODIFICAÇÃO DE HUFFMAN #################')
print("> H(X) = %f bits/símbolo" % entropy)
print("> Lm =  %f bits/símbolo" % comp_medio)
print("------------------------")
print("| Eficiência = %.2f %% |" % (entropy / comp_medio * 100))
print("------------------------")
print()

print('############## DEPOIS DA CODIFICAÇÃO DE HUFFMAN #################')
print("> H(X) = %f bits/símbolo" % entropy)
print("> Lm =  %f bits/símbolo" % comp_medio_huffman)
print("------------------------")
print("| Eficiência = %.2f %% |" % (entropy / comp_medio_huffman * 100))
print("------------------------")
print()

"""
RLE = []
RLE_TH = []

# APLICANDO O RLE NA IMAGEM ORIGINAL
j = 0

for i in range(img.shape[0]):
	j = 0
	while(j < img.shape[1]):
		qtd = 0
		pixel = img[i, j]
		while(j < img.shape[1] and pixel == img[i, j]):
			qtd += 1
			j += 1
			#print(j)

		RLE.append(qtd)
		RLE.append(pixel)
	# Indicador de fim da i-ésima linha da imagem
	RLE.append(0)
	RLE.append(0)

# Indicador de fim da imagem
RLE.append(0)
RLE.append(1)

# APLICANDO O RLE NA IMAGEM LIMIARIZADA
j = 0
qtd = 0

for i in range(img_th.shape[0]):
	j = 0
	while(j < img_th.shape[1]):
		qtd = 0
		pixel = img_th[i, j]
		while(j < img_th.shape[1] and pixel == img_th[i, j]):
			qtd += 1
			j += 1
			#print(j)

		RLE_TH.append(qtd)
		RLE_TH.append(pixel)
	# Indicador de fim da i-ésima linha da imagem
	RLE_TH.append(0)
	RLE_TH.append(0)
		

# Indicador de fim da imagem
RLE_TH.append(0)
RLE_TH.append(1)

RLE_NP = np.asarray(RLE)
RLE_TH_NP = np.asarray(RLE_TH)

print("\n########### IMAGEM ORIGINAL #############")
print("Tamanho da imagem original: %d" % (img.shape[0] * img.shape[1]))
print("Tamanho após a codificação: %d" % len(RLE_NP))
print("\n########### IMAGEM LIMIARIZADA #############")
print("Tamanho da imagem limiarizada: %d" % getsizeof(img_th))
print("Tamanho após a codificação: %d" % getsizeof(RLE_TH_NP))

cv2.namedWindow('Imagem Original', cv2.WINDOW_NORMAL)
cv2.namedWindow('Imagem Limiarizada', cv2.WINDOW_NORMAL)
cv2.imshow('Imagem Limiarizada', img_th)
cv2.imshow('Imagem Original', img)
cv2.waitKey()
"""