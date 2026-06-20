# Arquitetura Geral – Central de Inteligência Urbana (CIU)

## Visão geral

Esta documentação descreve a arquitetura de alto nível da **Central de Inteligência Urbana (CIU)**, focando na Fase 1 (Cidade Observável). A CIU foi concebida como uma plataforma modular capaz de evoluir de um sistema de monitoramento para um ecossistema de otimização e automação de mobilidade urbana.

O diagrama abaixo apresenta os principais componentes e fluxos de dados:

```
Câmeras / Sensores
      ↓
Módulo de Captura
      ↓
IA de Visão Computacional
      ↓
Processamento de Eventos
      ↓
Banco de Dados + Dados Geográficos
      ↓
API Backend (FastAPI)
      ↓
Dashboard Web / Mapa / Relatórios
      ↓
Gestores públicos / Agentes de trânsito
```

### Camada de Campo

Compõe-se de **câmeras de monitoramento** instaladas em cruzamentos estratégicos, além de outros sensores (por exemplo, botoeiras, sensores de chuva ou alagamento) que serão adicionados em fases futuras. Para iniciar o projeto em Recife, selecionamos alguns cruzamentos com base nas câmeras divulgadas no portal oficial da prefeitura e da CTTU. Esses pontos incluem:

- **Av. Abdias de Carvalho x Av. do Forte** – interseção importante na zona oeste; listada no portal da CTTU como CAM‑LB01【542935923486676†L60-L69】.
- **Av. Beberibe x Rua São Bento** – cruzamento na zona norte, identificado como CAM‑LB02【542935923486676†L60-L69】.
- **Av. Norte x Cruz Cabugá** – ponto de ligação entre as regiões central e norte, indicado como CAM‑LB04【542935923486676†L60-L69】.
- **Antonio Falcão x Domingos Ferreira** – interseção próxima à praia de Boa Viagem, constando como CAM‑LB07【542935923486676†L60-L69】.

Esses cruzamentos servirão como **provas de conceito** para calibrar a detecção de veículos e validar a plataforma. A tabela `intersections` de nosso banco de dados será populada com esses registros iniciais por meio do script de *seed*.

### Camada de Inteligência

Nesta fase, a CIU utiliza **YOLO** e **OpenCV** para detectar e classificar veículos e pedestres. O processamento pode ocorrer em edge (no próprio dispositivo) ou em servidor dedicado, dependendo do volume de dados e da disponibilidade de GPUs. O modelo de visão computacional gera métricas como contagem de veículos, tamanho das filas e velocidade média, que são então enviadas ao backend.

### Camada de Dados

O backend utiliza **PostgreSQL** com a extensão **PostGIS** para armazenar cruzamentos, câmeras e observações de trânsito. A modelagem é simples e eficiente para a Fase 1: cada observação registra a contagem de tipos de veículos, pedestres, velocidade média e nível de congestionamento. Para dados de séries temporais mais volumosos ou processamento de eventos em tempo real, consideramos o uso de **Redis** ou **Kafka** em fases futuras.

### Camada de Aplicação

Implementada com **FastAPI**, esta camada expõe uma API REST que permite o cadastro de cidades, cruzamentos e câmeras, além de fornecer endpoints para registrar e consultar observações de trânsito. As rotas são versionadas e preparadas para expansão futura. O backend também integra **Alembic** para migrações e segue os princípios SOLID e DDD para um código sustentável.

### Camada de Interface

O frontend (a ser desenvolvido) será um **dashboard React com TypeScript**. Ele consumirá a API para exibir mapas interativos (via **Leaflet** e **OpenStreetMap**), gráficos e rankings de congestionamento. A interface permitirá que gestores filtrem por cidade, cruzamento ou período, façam exportação de CSV e visualizem indicadores em tempo real.

## Integrações adicionais

### Plataforma OpenAI e agente IA

A CIU pode integrar **modelos de linguagem** para responder a perguntas dos gestores (“Qual é o cruzamento mais congestionado hoje?”), gerar relatórios ou oferecer assistência urbana ao cidadão. Se você já vinculou a plataforma OpenAI e criou um agente de IA conectado ao seu repositório GitHub, isso é um passo adiante para automação de suporte e geração de insights. Lembre-se de proteger chaves de API em variáveis de ambiente e garantir que o acesso aos modelos esteja de acordo com as políticas de privacidade.

### GitHub

Hospedar este projeto em um repositório **GitHub** é recomendável para versionamento, colaboração e integração contínua. Com o repositório configurado, você pode habilitar pipelines de CI/CD (por exemplo, GitHub Actions) para executar testes e publicar novas versões automaticamente. Verifique se as credenciais de banco e outras informações sensíveis permanecem fora do controle de versão, utilizando arquivos `.env` ou segredos do GitHub.

## Próximos passos

1. **Rodar a aplicação localmente** usando o `docker-compose.yml` fornecido para subir o banco e o backend.
2. **Executar o script `seed.py`** para popular a base de dados com Recife e os cruzamentos iniciais.
3. **Criar o frontend** com React, incluindo componentes de mapa e gráficos, consumindo a API.
4. **Configurar testes automatizados** (pytest) e pipelines de CI/CD.
5. **Evoluir para a fase recomendativa** (Fase 2), incorporando algoritmos de previsão e recomendação que analisem as observações históricas para sugerir ajustes semafóricos.