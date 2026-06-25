"""
Módulo de detecção de veículos e pedestres usando YOLOv8
================================================================

Este módulo implementa um detector simples baseado no modelo YOLOv8
pré‑treinado fornecido pela biblioteca `ultralytics`. Ele captura
quadros de uma fonte de vídeo (por exemplo, um arquivo local ou
stream RTSP), realiza a detecção de objetos de interesse e envia as
contagens para a API da CIU. O objetivo é mostrar como integrar a
visão computacional com o backend desenvolvido no ATO 1.

Como usar:

1. Instale as dependências em um ambiente Python isolado (venv):

   pip install ultralytics opencv-python requests

2. Ajuste a variável `SOURCE` para apontar para um arquivo de vídeo
   de teste ou uma URL RTSP de uma câmera.

3. Execute este módulo com `python vision/detector.py` a partir da
   raiz do projeto. Certifique‑se de que a API da CIU esteja em
   execução em http://localhost:8000.

4. O script enviará requisições POST para o endpoint
   `/api/v1/observations`, preenchendo os campos com as contagens
   detectadas e alguns valores simulados para métricas adicionais.

Observação: esta é uma implementação didática. Para uso em produção,
considere otimizações como processamento assíncrono, ajuste fino do
modelo, filtros de ruído e limites de confiança adequados.
"""

from __future__ import annotations

import time
from typing import Dict

import cv2  # type: ignore
import numpy as np
import requests
from ultralytics import YOLO  # type: ignore

# URL da API de observações (ajuste conforme necessário)
API_URL = "http://localhost:8000/api/v1/observations"

# Identificadores padrão para a interseção e câmera. Substitua pelos
# IDs correspondentes cadastrados no banco pelo script de seed.
INTERSECTION_ID = 1
CAMERA_ID = 1

# Fonte de vídeo: pode ser o caminho de um arquivo (e.g. "video.mp4")
# ou uma URL RTSP fornecida pela câmera. Ajuste conforme necessário.
SOURCE = "video.mp4"

def count_objects(class_ids: np.ndarray) -> Dict[str, int]:
    """Conta objetos de interesse a partir dos IDs de classe do modelo.

    O modelo YOLOv8 treinado no conjunto COCO retorna IDs de classes
    entre 0 e 79. Aqui mapeamos apenas as classes de interesse para
    mobilidade urbana: pessoa, bicicleta, carro, moto, ônibus e
    caminhão.

    Args:
        class_ids: array de inteiros representando as classes
                   detectadas em um quadro.

    Returns:
        dicionário com as contagens por tipo de objeto.
    """
    # Mapas de classes de interesse conforme COCO
    CLASSES_TO_COUNT = {
        'pedestrians_count': 0,  # pessoa
        'bicycles_count': 1,     # bicicleta
        'cars_count': 2,         # carro
        'motorcycles_count': 3,  # motocicleta
        'buses_count': 5,        # ônibus
        'trucks_count': 7        # caminhão
    }
    counts = {key: 0 for key in CLASSES_TO_COUNT}
    for name, class_id in CLASSES_TO_COUNT.items():
        counts[name] = int((class_ids == class_id).sum())
    return counts

def send_observation(intersection_id: int, camera_id: int, counts: Dict[str, int]) -> None:
    """Envia uma observação de trânsito para a API.

    Combina as contagens de objetos com métricas simuladas de
    velocidade média, tamanho da fila e nível de congestionamento.
    Envia os dados em formato JSON via HTTP POST.

    Args:
        intersection_id: ID da interseção
        camera_id: ID da câmera
        counts: dicionário com contagens por tipo de objeto
    """
    # Estas métricas são calculadas de forma simples e devem ser
    # aprimoradas em versões futuras.
    total_veiculos = (
        counts['cars_count'] + counts['motorcycles_count'] +
        counts['buses_count'] + counts['trucks_count']
    )
    average_speed = 30.0 - min(total_veiculos * 0.5, 20.0)  # km/h
    queue_length = total_veiculos  # valor fictício para fila
    congestion_level = min(total_veiculos / 50.0, 1.0)

    payload = {
        'intersection_id': intersection_id,
        'camera_id': camera_id,
        'average_speed': round(average_speed, 2),
        'queue_length': queue_length,
        'congestion_level': round(congestion_level, 2),
        **counts,
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=5)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Erro ao enviar observação: {exc}")
    else:
        print(f"Observação enviada: {payload}")

def process_stream(source: str, intersection_id: int, camera_id: int) -> None:
    """Processa um stream de vídeo e envia observações periódicas.

    Args:
        source: caminho ou URL do vídeo/stream
        intersection_id: ID da interseção
        camera_id: ID da câmera
    """
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print(f"Falha ao abrir a fonte de vídeo: {source}")
        return

    # Carrega o modelo YOLOv8 (considera que o arquivo pesa dezenas de MB)
    model = YOLO('yolov8s.pt')

    print("Processando stream... pressione Ctrl+C para interromper.")
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Fim do vídeo ou erro ao ler frame.")
                break

            # Realiza a detecção e obtém as classes detectadas
            results = model.predict(frame, conf=0.5, iou=0.5)
            if results:
                # A API da biblioteca retorna uma lista; pegamos o primeiro item
                detection = results[0]
                class_ids = detection.boxes.cls.cpu().numpy().astype(int)
                counts = count_objects(class_ids)
                send_observation(intersection_id, camera_id, counts)

            # Dorme 1 segundo entre observações para não sobrecarregar a API
            time.sleep(1)
    except KeyboardInterrupt:
        print("Processamento interrompido pelo usuário.")
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    # Ajuste INTERSECTION_ID e CAMERA_ID conforme IDs do seu banco
    process_stream(SOURCE, INTERSECTION_ID, CAMERA_ID)