import cv2
import numpy as np
from ultralytics import YOLO
from dataclasses import dataclass
from typing import Union

# 1. DEFINIÇÃO DA ESTRUTURA DA CARTA
# Usamos um dataclass para criar uma classe 'Card' de forma concisa.
# O __repr__ customizado formata a saída exatamente como você pediu.
@dataclass
class Card:
    cor: str
    numero: Union[int, str]  # Pode ser um número (int) ou um texto (ex: "skip")
    posicao: int

    def __repr__(self):
        # Formata o número como inteiro se for dígito, senão como string com aspas
        numero_repr = self.numero if isinstance(self.numero, int) else f'"{self.numero}"'
        # Formata a cor com aspas
        cor_repr = f'"{self.cor}"'
        
        return f"card(cor={cor_repr}, numero={numero_repr}, posicao={self.posicao})"

# 2. CLASSE YOLO UTILS ATUALIZADA
class YoloUtils:
    def __init__(self):
        pass

    @staticmethod
    def get_uno_color(image, bbox):
        # (Seu código para detectar a cor permanece aqui, sem alterações)
        x, y, w, h = bbox
        x, y, w, h = int(x), int(y), int(w), int(h)
        y_start, y_end = max(0, y), min(image.shape[0], y + h)
        x_start, x_end = max(0, x), min(image.shape[1], x + w)
        roi = image[y_start:y_end, x_start:x_end]
        if roi.size == 0: return "UNKNOWN"
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        color_ranges = {
            'RED':  ([0, 80, 70], [7, 255, 255]), 'RED2': ([170, 80, 70], [179, 255, 255]),
            'BLUE': ([100, 80, 30], [140, 255, 255]), 'GREEN':([40, 40, 40], [90, 255, 255]),
            'YELLOW':([18, 60, 80], [35, 255, 255]),
        }
        lower_filter, upper_filter = np.array([0, 50, 20]), np.array([179, 255, 255])
        color_mask = cv2.inRange(hsv_roi, lower_filter, upper_filter)
        color_counts = {'RED': 0, 'GREEN': 0, 'BLUE': 0, 'YELLOW': 0}
        lower_red1, upper_red1 = np.array(color_ranges['RED'][0]), np.array(color_ranges['RED'][1])
        lower_red2, upper_red2 = np.array(color_ranges['RED2'][0]), np.array(color_ranges['RED2'][1])
        red_mask = cv2.bitwise_or(cv2.inRange(hsv_roi, lower_red1, upper_red1), cv2.inRange(hsv_roi, lower_red2, upper_red2))
        color_counts['RED'] = cv2.countNonZero(cv2.bitwise_and(red_mask, color_mask))
        for color_name in ['GREEN', 'BLUE', 'YELLOW']:
            lower, upper = np.array(color_ranges[color_name][0]), np.array(color_ranges[color_name][1])
            mask = cv2.inRange(hsv_roi, lower, upper)
            color_counts[color_name] = cv2.countNonZero(cv2.bitwise_and(mask, color_mask))
        if not any(color_counts.values()): return "WILD"
        dominant_color = max(color_counts, key=color_counts.get)
        if color_counts[dominant_color] < (roi.size * 0.05 / 3): return "UNKNOWN"
        return dominant_color

    def seeDeck(self):
        model = YOLO("best.pt")
        cap = cv2.VideoCapture(1)

        if not cap.isOpened():
            print("Erro: Não foi possível abrir a webcam.")
            return []

        ret, frame = cap.read()
        cap.release()

        if not ret:
            print("Erro: Falha ao capturar a foto.")
            return []

        results = model(frame, stream=True, verbose=False)
        cartas_detectadas = []

        for result in results:
            for box in result.boxes:
                class_name = result.names[int(box.cls[0].item())]
                xywh = box.xywh[0].tolist()
                
                cartas_detectadas.append({
                    "cor": self.get_uno_color(frame, xywh),
                    "numero_str": class_name,
                    "x": xywh[0]
                })

        # Ordena a lista de dicionários com base na coordenada 'x'
        cartas_detectadas.sort(key=lambda c: c['x'])
        
        # --- LÓGICA ATUALIZADA PARA CRIAR A LISTA DE OBJETOS ---
        lista_final = []
        for i, carta_info in enumerate(cartas_detectadas):
            numero_final = carta_info['numero_str']
            
            # Tenta converter o número da carta para inteiro, se não der, mantém como texto
            if numero_final.isdigit():
                numero_final = int(numero_final)

            # Cria a instância do objeto Card e adiciona à lista
            nova_carta = Card(
                cor=carta_info['cor'],
                numero=numero_final,
                posicao=i + 1  # Posição começa em 1
            )
            lista_final.append(nova_carta)

        print(f"Cartas detectadas: {lista_final}")        
        return lista_final

# --- Execução do Código ---
if __name__ == '__main__':
    detector = YoloUtils()
    detector.seeDeck()