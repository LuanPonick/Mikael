import cv2
import numpy as np
from ultralytics import YOLO

class YoloUtils:
    def __init__(self):
        pass

    # Método para detectar a cor da carta
    @staticmethod
    def get_uno_color(image, bbox):

        x, y, w, h = bbox
        x, y, w, h = int(x), int(y), int(w), int(h)

        # Garante que a ROI não comece fora da imagem
        y_start = max(0, y)
        y_end = min(image.shape[0], y + h)
        x_start = max(0, x)
        x_end = min(image.shape[1], x + w)

        roi = image[y_start:y_end, x_start:x_end]

        if roi.size == 0:
            return "UNKNOWN"

        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        color_ranges = {
            'RED':  ([0, 80, 70], [7, 255, 255]),
            'RED2': ([170, 80, 70], [179, 255, 255]),
            'BLUE': ([100, 80, 30], [140, 255, 255]),
            'GREEN':([40, 40, 40], [90, 255, 255]),
            'YELLOW':([18, 60, 80], [35, 255, 255]),
        }

        # Filtro geral para remover pixels muito escuros ou muito claros
        lower_filter = np.array([0, 50, 20])
        upper_filter = np.array([179, 255, 255])
        color_mask = cv2.inRange(hsv_roi, lower_filter, upper_filter)

        color_counts = {'RED': 0, 'GREEN': 0, 'BLUE': 0, 'YELLOW': 0}

        # Lógica para o vermelho (que cruza o 0 do HUE)
        lower_red1, upper_red1 = np.array(color_ranges['RED'][0]), np.array(color_ranges['RED'][1])
        lower_red2, upper_red2 = np.array(color_ranges['RED2'][0]), np.array(color_ranges['RED2'][1])
        red_mask1 = cv2.inRange(hsv_roi, lower_red1, upper_red1)
        red_mask2 = cv2.inRange(hsv_roi, lower_red2, upper_red2)
        red_mask = cv2.bitwise_or(red_mask1, red_mask2)
        final_red_mask = cv2.bitwise_and(red_mask, color_mask) # Aplica filtro geral
        color_counts['RED'] = cv2.countNonZero(final_red_mask)

        # Lógica para outras cores
        for color_name in ['GREEN', 'BLUE', 'YELLOW']:
            lower, upper = np.array(color_ranges[color_name][0]), np.array(color_ranges[color_name][1])
            mask = cv2.inRange(hsv_roi, lower, upper)
            final_mask = cv2.bitwise_and(mask, color_mask) # Aplica filtro geral
            color_counts[color_name] = cv2.countNonZero(final_mask)

        # Determina a cor dominante
        if not any(color_counts.values()):
            return "WILD" # Retorna WILD se nenhuma cor for detectada

        dominant_color = max(color_counts, key=color_counts.get)
        
        # Threshold para evitar falsos positivos
        # A cor dominante deve ocupar pelo menos 5% dos pixels da ROI
        if color_counts[dominant_color] < (roi.size * 0.05 / 3):
            return "UNKNOWN" # Cor detectada é muito fraca

        return dominant_color

    def seeDeck(self):
        model = YOLO("best.pt")
        # Nota: cv2.VideoCapture(0) é geralmente a webcam padrão.
        # Use 1 se você tiver certeza que essa é a câmera correta.
        cap = cv2.VideoCapture(1)

        if not cap.isOpened():
            print("Erro: Não foi possível abrir a webcam.")
            return # Use return para sair do método

        print("Capturando uma foto da webcam...")
        ret, frame = cap.read()
        cap.release()
        print("Webcam liberada.")

        if not ret:
            print("Erro: Falha ao capturar a foto.")
            return

        print("Foto capturada. Processando com o modelo YOLO...")
        results = model(frame, stream=True, verbose=False)
        cartas = []

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0].item())
                class_name = result.names[class_id]
                xywh = box.xywh[0].tolist()
                x1, y1, x2, y2 = box.xyxy[0].tolist()

                # A coordenada 'x' do centro da carta, usada para ordenar
                x_centro = xywh[0]

                detected_color = self.get_uno_color(frame, xywh)
                label = f"{detected_color} {class_name}"

                # Adiciona o dicionário completo à lista temporária
                cartas.append({"Carta": {"cor": detected_color, "numero": class_name, "x": x_centro}})
                
                # Desenha na imagem para visualização
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # --- NOVA LÓGICA DE ORDENAÇÃO ---

        # 1. Ordena a lista 'cartas' com base na chave 'x' (do menor para o maior)
        cartas.sort(key=lambda item: item['Carta']['x'])
        
        # 2. Cria o dicionário final no formato "carta0", "carta1", ...
        cartas_ordenadas = {}
        for i, item_carta in enumerate(cartas):
            chave = f"carta{i}"
            # O valor será o dicionário interno {"cor": ..., "numero": ...}
            # Opcional: Removendo a chave 'x' do dicionário final para limpá-lo
            del item_carta['Carta']['x']
            cartas_ordenadas[chave] = item_carta['Carta']

        # --- FIM DA NOVA LÓGICA ---

        cv2.imshow("Resultado da Deteccao - Pressione qualquer tecla para fechar", frame)
        
        # Imprime o dicionário final, ordenado e formatado
        print("Cartas detectadas e ordenadas:")
        print(cartas_ordenadas)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        # Retorna o resultado para que possa ser usado por outro código, se necessário
        return cartas_ordenadas

# --- Execução do Código ---
if __name__ == '__main__':
    detector = YoloUtils()
    detector.seeDeck()