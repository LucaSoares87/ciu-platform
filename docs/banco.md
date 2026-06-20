# Modelagem do Banco de Dados

Esta fase da CIU utiliza um banco de dados relacional PostgreSQL com a extensão **PostGIS** habilitada para suportar dados geoespaciais. A modelagem foca em representar **cidades**, **cruzamentos**, **câmeras** e **observações de trânsito** de forma simples e extensível.

## Tabelas principais

### `cities`
| Coluna     | Tipo      | Descrição                               |
|-----------|-----------|-----------------------------------------|
| id        | integer   | Chave primária (PK)                      |
| name      | varchar   | Nome da cidade                          |
| state     | char(2)   | Sigla do estado                         |

Cada cidade pode possuir diversos cruzamentos.

### `intersections`
| Coluna       | Tipo    | Descrição                                                |
|-------------|--------|----------------------------------------------------------|
| id          | integer| Chave primária (PK)                                       |
| city_id     | integer| Chave estrangeira (FK) para `cities.id`                   |
| name        | varchar| Nome do cruzamento (ex.: "Av. Abdias x Av. do Forte")     |
| latitude    | float  | Latitude do ponto (opcional)                             |
| longitude   | float  | Longitude do ponto (opcional)                            |
| description | text   | Descrição ou observações adicionais                      |

Um cruzamento pode ter várias câmeras e várias observações.

### `cameras`
| Coluna        | Tipo    | Descrição                                             |
|--------------|--------|-------------------------------------------------------|
| id           | integer| Chave primária (PK)                                    |
| intersection_id | integer| Chave estrangeira para `intersections.id`           |
| name         | varchar| Nome de referência para a câmera (ex.: "Câmera principal") |
| rtsp_url     | varchar| URL RTSP para streaming de vídeo (pode ser nula)       |
| status       | varchar| Estado da câmera (ex.: "ACTIVE", "INACTIVE")          |

Uma câmera está sempre associada a um cruzamento e pode gerar muitas observações.

### `traffic_observations`
| Coluna            | Tipo      | Descrição                                                             |
|------------------|-----------|-----------------------------------------------------------------------|
| id               | integer   | Chave primária (PK)                                                    |
| intersection_id  | integer   | Chave estrangeira para `intersections.id`                              |
| camera_id        | integer   | Chave estrangeira para `cameras.id`                                    |
| timestamp        | datetime  | Data e hora da observação                                             |
| cars_count       | integer   | Contagem de carros                                                    |
| motorcycles_count| integer   | Contagem de motos                                                     |
| buses_count      | integer   | Contagem de ônibus                                                   |
| trucks_count     | integer   | Contagem de caminhões                                                |
| bicycles_count   | integer   | Contagem de bicicletas                                               |
| pedestrians_count| integer   | Contagem de pedestres                                                |
| average_speed    | float     | Velocidade média estimada (km/h)                                     |
| queue_length     | integer   | Comprimento da fila (número de veículos)                             |
| congestion_level | float     | Nível de congestionamento (0 a 1 ou em percentual)                   |

Cada observação corresponde a um intervalo de tempo, podendo ser registrada a cada minuto ou em períodos mais curtos, dependendo da frequência da captura.

## Scripts de seed

O arquivo `app/seed.py` cria a cidade de **Recife** e insere alguns cruzamentos do Grande Recife, conforme identificado no portal de trânsito local【542935923486676†L60-L69】. As câmeras são adicionadas com URLs RTSP fictícias para demonstração. Para rodar o seed, execute:

```bash
docker-compose run --rm backend python -m app.seed
```

Esse comando inicializa uma sessão do Python dentro do contêiner do backend, cria os registros e finaliza a execução.

## Expansão futura

Para fases posteriores (cidade recomendativa e semi-autônoma), novas tabelas poderão ser adicionadas, como:

- `signal_plans`: planos semafóricos por cruzamento.
- `recommendations`: histórico de recomendações com justificativas.
- `audit_logs`: trilhas de auditoria de ações automáticas ou manuais.
- `weather_conditions`: armazenamento de dados meteorológicos correlacionados.

Além disso, bancos NoSQL ou filas de mensagens (Kafka, RabbitMQ) poderão ser integrados para escalabilidade e processamento em tempo real.