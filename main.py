import cv2
import numpy as np
from ultralytics import YOLO
#importação de bibliotecas necessárias para processamento de vídeo, manipulação de arrays e uso do modelo YOLO para detecção de objetos. 
 
#VIDEO_PATH = "multa_validada.mp4"
#VIDEO_PATH = "multa_invalida.mp4"
VIDEO_PATH = "revisao_multa.mp4"

CLASSES_VEICULOS = [2, 3, 5, 7]     

print("[1/2] Carregando modelo neural para inspeção de emergência...")
model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(VIDEO_PATH) 

frames_analisados = 0
frames_com_sirene = 0
veredito_final = "PROCESSANDO..."
cor_veredito = (255, 255, 255)

#Fiquei com preguiça de comentar o resto do código, mas basicamente ele faz a leitura de um vídeo, detecta veículos e verifica se há luzes de emergência ativas, fornecendo um veredito final sobre a infração
#PS: o código não é perfeito, mas funciona bem para o propósito de demonstração.
#Alguém vai ler isso? Eu vou mandar no grupo e eu duvido que vocês vão ler até aqui, mas se você leu, parabéns! você é uma pessoa curiosa e dedicada.

def detectar_luz_emergencia(crop_veiculo):
    """
    Analisa o terço superior do veículo em busca de emissões
    saturadas características de giroflex (vermelho, azul e âmbar).
    """
    if crop_veiculo.size == 0:
        return False
    
    altura, _, _ = crop_veiculo.shape
    teto = crop_veiculo[0:int(altura * 0.30), :]
    
    hsv = cv2.cvtColor(teto, cv2.COLOR_BGR2HSV)
    
    mascara_vermelho1 = cv2.inRange(hsv, np.array([0, 140, 160]), np.array([10, 255, 255]))
    mascara_vermelho2 = cv2.inRange(hsv, np.array([170, 140, 160]), np.array([180, 255, 255]))
    mascara_azul = cv2.inRange(hsv, np.array([100, 140, 160]), np.array([130, 255, 255]))
    
    mascara_sirene = mascara_vermelho1 | mascara_vermelho2 | mascara_azul
    densidade_luz = cv2.countNonZero(mascara_sirene) / (teto.shape[0] * teto.shape[1] + 1e-5)
    
    return densidade_luz > 0.03

print("[2/2] Executando auditoria do vídeo...")

while cap.isOpened():
    sucesso, frame = cap.read()
    if not sucesso:
        break

    frames_analisados += 1
    
    resultados = model(frame, classes=CLASSES_VEICULOS, verbose=False)
    
    sirene_no_frame = False
    
    for r in resultados:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            veiculo_crop = frame[y1:y2, x1:x2]
            
            if detectar_luz_emergencia(veiculo_crop):
                sirene_no_frame = True
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 165, 255), 3)
                cv2.putText(frame, "SIRENE / GIROFLEX ATIVO", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)
            else:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (200, 200, 200), 1)

    if sirene_no_frame:
        frames_com_sirene += 1

    taxa_emergencia = (frames_com_sirene / frames_analisados) if frames_analisados > 0 else 0
    
    if taxa_emergencia >= 0.15:
        veredito_final = "MULTA ANULADA (EMERGENCIA IDENTIFICADA)"
        cor_veredito = (0, 255, 0)      
    else:
        veredito_final = "MULTA VALIDADA (INFRACAO COMUM)"
        cor_veredito = (0, 0, 255)      

    # Painel HUD de Auditoria de Trânsito
    cv2.rectangle(frame, (10, 10), (620, 85), (20, 20, 20), -1)
    cv2.putText(frame, f"SISTEMA DSIN - AUDITORIA DE RADAR", (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, f"STATUS: {veredito_final}", (20, 65),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, cor_veredito, 2)

    cv2.imshow("DSIN Traffic - Verificador de Infracoes", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print("\n" + "="*50)
print(f"RELATORIO DE AUDITORIA DSIN:")
print(f"Frames Avaliados: {frames_analisados}")
print(f"Frames com Evidencia de Sirene: {frames_com_sirene}")
print(f"Decisao Final da IA: {veredito_final}")
print("="*50 + "\n")