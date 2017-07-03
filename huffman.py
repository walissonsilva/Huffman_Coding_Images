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
