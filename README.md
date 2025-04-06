# Bitdoglab: O jogo da vida de John Conway

## Descrição
O Jogo da Vida de John Conway é um autômato celular criado pelo matemático britânico John Horton Conway em 1970. Este projeto tem como objetivo implementar o Jogo da Vida utilizando a placa BitDogLab, demonstrando suas funcionalidades de forma lúdica e preparando para projetos mais complexos no futuro.

## Proposta do Projeto
A proposta é fazer uma implementação do Jogo da Vida de John Conway no display da placa BitDogLab. Este jogo segue um conjunto de regras que determinam a evolução do estado da tela ao longo do tempo:
1. Toda célula viva com menos de dois vizinhos vivos morre por isolamento.
2. Toda célula viva com mais de três vizinhos vivos morre por superpopulação.
3. Toda célula viva com dois ou três vizinhos vivos permanece viva.
4. Toda célula morta com exatamente três vizinhos vivos torna-se viva (nascimento).

Referência: [Wikipedia - Jogo da Vida](https://pt.wikipedia.org/wiki/Jogo_da_vida)

## Objetivos
Demonstrar as funcionalidades da placa BitDogLab por meio de um jogo, nos preparando para projetos futuros com maior grau de complexidade.

## Tecnologias Utilizadas
- Python
- MicroPython
- BitDogLab

## Componentes Utilizados
- Matriz de LEDs RGB
- Joystick
- Display OLED
- Botão A
- Botão B

## Como Executar o Projeto
1. Clone o repositório:
   ```sh
   git clone https://github.com/Danielgb23/game_of_life_bitdoglab.git
   ```
2. Navegue até o diretório do projeto:
   ```sh
   cd game_of_life_bitdoglab
   ```
3. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```
4. Execute o projeto:
   ```sh
   python main.py
   ```

## Estrutura do Projeto
- `main.py`: Arquivo principal para execução do jogo.
- `game_of_life.py`: Contém a lógica do autômato celular.

## Resultados Esperados
Um exemplo funcional e prático do Jogo da Vida em uma grade limitada de 128x64. As células vivas (acesas) inseridas pelo usuário na matriz de LEDs devem evoluir de acordo com as regras do jogo.

## Vídeo
Para uma visão geral do projeto, assista ao vídeo: [Link para o Vídeo](https://youtu.be/jUXryB5bY1Y)

## Contribuição
Contribuições são bem-vindas! Para contribuir, siga os passos abaixo:
1. Faça um fork do projeto.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova feature'`).
4. Faça push para a branch (`git push origin feature/nova-feature`).
5. Abra um Pull Request.

## Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
