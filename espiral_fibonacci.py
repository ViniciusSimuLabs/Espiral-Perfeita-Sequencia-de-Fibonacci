# -*- coding: utf-8 -*-

__author__ = "Vinícius Moraes"
__version__ = "0.0.1"
__license__ = "Não Licenciado"
__date__ = "22/10/2025"


# --- Código ---
import turtle # cria janela e desenha na tela como se fosse um pincel
import time
import math

# variaveis
velocidade_angular = 1 # velocidade que a espiral gira
fib_seq = [0, 1]       # lista com a sequencia de fibonacci (agora so tem os 2 primeiros, o resto adiciona depois)
fib_atual = 1          # guarda qual numero da sequencia esta sendo desenhado
angulo_progresso = 0   # guarda quanto do arco de 90° já desenhou
tamanho_max_tela = 380 # tamanho maximo da espiral

# janela
janela = turtle.Screen()
janela.title("Espiral - Sequência de Fibonacci")
janela.bgcolor("#000000")
janela.setup(width=2560, height=1440)
janela.tracer(0)                                  # desliga a atualização automatica da janela, fica bugado, melhor fazer na mão com o .update

# pinceis turtle
pincel_desenho = turtle.Turtle() # cria o pincel que desenha o quadrado e a espiral
pincel_desenho.speed(0)          # tira o limite de velocidade do pincel, ja ta controlado na velocidade angular
pincel_desenho.hideturtle()      # deixa a seta do pincel invisivel
pincel_desenho.pensize(2)        # da uma ENGROSSADA no pincel

pincel_texto = turtle.Turtle()
pincel_texto.hideturtle()
pincel_texto.penup()  # é esquisito, mas a pira é que é a mesma coisa que levantar o pincel da "folha" pra parar de riscar
pincel_texto.pencolor("#FFFFFF")

while True:
    if fib_atual == len(fib_seq):                # verifica se já esta desenhando o ultimo numero da sequencia na lista
        proximo_fib = fib_seq[-1] + fib_seq[-2]  # soma os dois ultimos numeros da lista fib_seq
        fib_seq.append(proximo_fib)              # adiciona a soma no final da lista

    pincel_desenho.clear() # apagam tudo que foi desenhado no ultimo frame, pra fazer a
    pincel_texto.clear()   # animação basicamente tem que redesenhar tudo em todos os frames
    
    # zoom out fluido
    tamanho_inicial = fib_seq[fib_atual - 1] if fib_atual > 1 else 0                                  # verifica o tamanho da espiral no arco anterior
    tamanho_final = fib_seq[fib_atual]                                                                # determina o tamanho que a espiral tem que ter quando completar o arco atual
    progresso_percentual = angulo_progresso / 90.0
    tamanho_interpolado = tamanho_inicial + (tamanho_final - tamanho_inicial) * progresso_percentual  # calcula o tamanho certinho que a espiral tem que ter nesse quadro
    if tamanho_interpolado > 0:                                                                    
        escala_dinamica = tamanho_max_tela / tamanho_interpolado  # determina a escala que cada os desenhos precisam estar para nao ficar nem grande nem pequeno
    else:
        escala_dinamica = 10
        
    x, y = 0, 0
    heading = 0 

    # desenha tudo na tela
    for i in range(1, fib_atual + 1):
        lado = fib_seq[i] * escala_dinamica # tamanho do quadrado com escala aplicada
        numero_fib = fib_seq[i]             # guarda o numero da sequencia de fibonacci que esta usando nessa rep
        
        # posiciona o lápis de desenho
        pincel_desenho.penup()
        pincel_desenho.goto(x, y)           # move o pincel pra posição certa
        pincel_desenho.setheading(heading)  # coloca o pincel "virado" pro lado certo (angulo certo)
        pincel_desenho.pendown()
        
        pincel_desenho.pencolor("#a3a3a3")
        pincel_desenho.width(1)
        
        # encontra o centro do quadrado pra colocar os numeros depois
        c1_x, c1_y = pincel_desenho.pos() # salva onde o pincel esta agora, o primeiro canto do quadrado
        h1 = math.radians(heading - 90)   # guarda em radianos o angulo do pincel -90°, na pratica é o mesmo que salvar o angulo girando o pincel 90° em sentido horario
        c2_x = c1_x + lado * math.cos(h1) # encontra a posição x do segunto canto do quadrado
        c2_y = c1_y + lado * math.sin(h1) # encontra a posição y do segundo canto do quadrado
        h2 = math.radians(heading - 180)  # guarda em radianos o angulo do pincel -180°, na pratica é o mesmo que salvar o angulo girando o pincel 180° em sentido horario
        c3_x = c2_x + lado * math.cos(h2) # encontra a posição x do terceiro canto do quadrado, diagonal oposta do primeiro canto
        c3_y = c2_y + lado * math.sin(h2) # encontra a poisção y do terceiro canto do quadrado, diagonal oposto do primeiro canto
        centro_x = (c1_x + c3_x) / 2      # tira a média do x das diagonais opostas, encontrando a posição x do centro do quadrado
        centro_y = (c1_y + c3_y) / 2      # tira a média do y das diagonais opostas, encontrando a posição y do centro do quadrado

        # desenha o quadrado
        for _ in range(4):
            pincel_desenho.right(90)
            pincel_desenho.forward(lado)

        # escreve o numero da sequencia de fibonacci nos quadrados
        if numero_fib > 0 and lado > 15:
            pincel_texto.goto(centro_x, centro_y)
            font_size = max(6, min(40, int(lado / 5)))
            pincel_texto.write(numero_fib, align="center", font=("Arial", font_size, "normal"))

        # desenha a espiral
        pincel_desenho.pencolor("#FFFFFF")
        pincel_desenho.width(3)
        
        pincel_desenho.left(90)                       # vira o pincel 90° em sentido anti-horario
        angulo_do_arco = 90
        if i == fib_atual:                            # verifica se o que está sendo desenhado é o arco mais atual
            angulo_do_arco = angulo_progresso         # se é o atual usa o angulo do progresso e não o 90°, já que o arco ainda não está completo
        pincel_desenho.circle(lado, -angulo_do_arco)  # desenha o arco. o ângulo é negativo pra ele desenhar em sentido horario
        
        # atualiza as variaveis para o proximo for
        x, y = pincel_desenho.pos()      # atualiza as coordenadas de x e y para as atuais, para o proximo for
        heading = (heading - 90) % 360   # atualiza a direção inicial pra qual o pincel vai estar apontando no proximo for, girando 90° anti-horario, % 360 pra manter os numeros entre 0° e 359°

    # atualiza o progresso do angulo
    angulo_progresso += velocidade_angular         # adiciona a velocidade no progresso, pra que no proximo for desenhe mais do arco
    if angulo_progresso >= 90:                     # verifica se já terminou o arco
        angulo_excedente = angulo_progresso - 90   # se sim, verifica quanto passou dos 90°
        fib_atual += 1
        angulo_progresso = angulo_excedente       # adiciona o excedente no progresso para no proximo for continuar de onde parou no ultimo

    janela.update()
    time.sleep(0.01)