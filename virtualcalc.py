import cv2
import numpy as np
import time
import math
import mediapipe as mp

# === Configuração do Mediapipe ===
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.85, min_tracking_confidence=0.85)

# === Classe Botão ===
class Botao:
    def __init__(self, posicao, largura, altura, valor):
        self.posicao = posicao
        self.largura = largura
        self.altura = altura
        self.valor = valor

    def desenhar(self, quadro, hover=False):
        x, y = self.posicao
        cor = (0, 128, 255) if hover else (30, 30, 30)  # Azul para hover, cinza escuro para padrão
        cv2.rectangle(quadro, self.posicao, (x + self.largura, y + self.altura), cor, cv2.FILLED)
        cv2.rectangle(quadro, self.posicao, (x + self.largura, y + self.altura), (200, 200, 200), 3)  # Borda cinza clara
        cv2.putText(quadro, self.valor, (x + 15, y + 45), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)

    def esta_sobre(self, x, y):
        bx, by = self.posicao
        return bx < x < bx + self.largura and by < y < by + self.altura

# === Layout da Calculadora ===
teclas = [
    ["7", "8", "9", "+"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "*"],
    ["C", "0", "=", "/"]
]

lista_botoes = []
for i in range(4):
    for j in range(4):
        xpos = j * 80 + 50  # Ajustando espaçamento horizontal
        ypos = i * 80 + 150  # Ajustando espaçamento vertical
        lista_botoes.append(Botao((xpos, ypos), 60, 60, teclas[i][j]))  # Ajustando tamanho dos botões

expressao = ""
tempo_ultimo_clique = 0
delay_clique = 1

cap = cv2.VideoCapture(0)

while True:
    sucesso, quadro = cap.read()
    quadro = cv2.flip(quadro, 1)
    rgb = cv2.cvtColor(quadro, cv2.COLOR_BGR2RGB)
    resultado = hands.process(rgb)

    altura, largura, canais = quadro.shape

    # Desenhar todos os botões
    for botao in lista_botoes:
        botao.desenhar(quadro)

    # Exibir a expressão atual
    cv2.rectangle(quadro, (50, 50), (450, 130), (50, 50, 50), cv2.FILLED)
    cv2.putText(quadro, expressao, (60, 115), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 255, 0), 2)

    if resultado.multi_hand_landmarks:
        marcacoes_mao = resultado.multi_hand_landmarks[0]
        lista_marcacoes = []
        for id, lm in enumerate(marcacoes_mao.landmark):
            cx, cy = int(lm.x * largura), int(lm.y * altura)
            lista_marcacoes.append((cx, cy))

        mp_drawing.draw_landmarks(quadro, marcacoes_mao, mp_hands.HAND_CONNECTIONS)

        # Verificar "pinça" (ponta do polegar e indicador)
        if lista_marcacoes:
            x1, y1 = lista_marcacoes[4]   # Ponta do polegar
            x2, y2 = lista_marcacoes[8]   # Ponta do indicador
            comprimento = math.hypot(x2 - x1, y2 - y1)

            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            tempo_atual = time.time()

            if comprimento < 40 and (tempo_atual - tempo_ultimo_clique) > delay_clique:
                for botao in lista_botoes:
                    if botao.esta_sobre(cx, cy):
                        selecionado = botao.valor

                        if selecionado == "C":
                            expressao = ""
                        elif selecionado == "=":
                            try:
                                expressao = str(eval(expressao))
                            except:
                                expressao = "Erro"
                        else:
                            expressao += selecionado

                        tempo_ultimo_clique = tempo_atual

                # Feedback visual
                cv2.circle(quadro, (cx, cy), 15, (0, 0, 255), cv2.FILLED)

    cv2.imshow("Calculadora Virtual - Dia 7", quadro)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
