# Sistema de Análise de Varejo com Visão Computacional

Este projeto utiliza YOLOv8 e OpenCV para monitorar o fluxo de clientes em uma loja, identificando entradas, pagamentos e calculando a taxa de conversão.

## Funcionalidades
- **Contagem de Pessoas**: Detecta quem entra na loja.
- **Rastreamento de Zonas**: Monitora se o cliente passou pelo caixa.
- **Cálculo de Conversão**: Exibe a taxa de compra vs. entrada em tempo real.
- **Overlay Visual**: Mostra zonas e estatísticas na tela.

## Pré-requisitos
- Python 3.8 ou superior instalado.
- Webcam ou arquivo de vídeo.

## Instalação e Execução

### Opção 1: Automática (Windows)
1. Dê um duplo clique no arquivo `setup_and_run.bat`.
2. O script irá configurar o ambiente e iniciar a detecção.

### Opção 2: Manual
1. Abra um terminal na pasta do projeto.
2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute o sistema:
   ```bash
   python main.py
   ```

   python main.py
   ```

## Reconhecimento Facial
Para que o sistema reconheça pessoas (funcionários ou VIPs):
1. Coloque fotos das pessoas na pasta `faces_db` que será criada automaticamente.
2. Nomeie os arquivos com o nome da pessoa (ex: `joao_silva.jpg`).
3. Ao reiniciar o sistema, ele aprenderá esses rostos e exibirá o nome ao lado da pessoa detectada.

## Integração WZStation (EZStation)
O sistema foi projetado para integrar-se com video management systems como o EZStation via RTSP.

1. No WZStation/EZStation, habilite o stream RTSP para a câmera desejada.
2. Obtenha a URL RTSP (exemplo: `rtsp://admin:123456@192.168.1.10:554/cam/realmonitor?channel=1&subtype=0`).
3. Edite o arquivo `main.py` e atualize a linha de conexão:

```python
# main.py
# Substitua pelo seu link RTSP
connector = WZStationConnector("rtsp://admin:123456@IP_DA_CAMERA:554/...")
```

Se nenhum link for fornecido, o sistema usará a webcam padrão.

## Configuração de Zonas
As zonas (Entrada, Caixa, Saída) estão definidas no arquivo `zones.py`.
Você pode ajustar as coordenadas dos polígonos editando este arquivo para corresponder ao layout da sua câmera/loja.

```python
self.zones = {
    "entry": np.array([[x1, y1], [x2, y2], ...]), # Área da porta
    "checkout": np.array([...]),                  # Área do caixa
    # ...
}
```

## Controles
- Pressione **'q'** na janela de vídeo para encerrar o programa.
