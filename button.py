import cv2

# === Classe Botão ===
class Botao:
    def __init__(self, posicao, largura, altura, valor):
        self.posicao = posicao
        self.largura = largura
        self.altura = altura
        self.valor = valor

    def desenhar(self, quadro, hover=False):
        x, y = self.posicao
        cor = (0, 128, 255) if hover else (50, 50, 50)  # Azul para hover, cinza escuro para padrão
        cv2.rectangle(quadro, self.posicao, (x + self.largura, y + self.altura), cor, cv2.FILLED)
        cv2.rectangle(quadro, self.posicao, (x + self.largura, y + self.altura), (200, 200, 200), 3)  # Borda cinza clara
        cv2.putText(quadro, self.valor, (x + 15, y + 45), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)

    def esta_sobre(self, x, y):
        bx, by = self.posicao
        return bx < x < bx + self.largura and by < y < by + self.altura