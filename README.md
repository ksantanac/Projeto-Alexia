# Sexta-Feira Virtual Assistant

Sexta-Feira Virtual Assistant é um assistente pessoal controlado por voz, inspirado na inteligência artificial do personagem Tony Stark, Jarvis. Este projeto foi desenvolvido em Python e utiliza várias bibliotecas para reconhecimento de fala, síntese de fala, consultas à Wikipedia, previsões do tempo e muito mais.

## Funcionalidades

1. **Reconhecimento de Fala**: Utiliza a biblioteca `speech_recognition` para ouvir e interpretar comandos de voz.
2. **Síntese de Fala**: Utiliza a biblioteca `pyttsx3` para converter texto em fala.
3. **Consultas à Wikipedia**: Faz pesquisas na Wikipedia e lê resumos das páginas.
4. **Previsão do Tempo**: Obtém a previsão do tempo para uma cidade especificada usando a API do OpenWeatherMap.
5. **Gerenciamento de Agenda**: Permite cadastrar, ler e limpar eventos em uma agenda.
6. **Obter Conselhos**: Faz uma solicitação a uma API para obter um conselho diário e o traduz para o português.
7. **Abrir Páginas Web**: Pode abrir páginas web específicas, como YouTube e Twitch.
8. **Abrir Aplicativos**: Pode abrir aplicativos locais, como o Visual Studio Code.

## Requisitos

- Python 3.x
- Bibliotecas Python:
  - `speech_recognition`
  - `pyttsx3`
  - `wikipedia`
  - `requests`
  - `googletrans`
  - `webbrowser`

## Instalação

1. Clone o repositório para o seu ambiente local:
    ```sh
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```

2. Instale as dependências necessárias:
    ```sh
    pip install -r requirements.txt
    ```

3. Substitua a chave de API do OpenWeatherMap na função `previsao_do_tempo` pela sua chave de API:
    ```python
    api_key = "sua_chave_de_api"
    ```

## Uso

Execute o arquivo principal do projeto:
```sh
python main.py
```

Ao iniciar, o assistente solicitará que você diga "ok sexta-feira" para iniciar o programa. A partir daí, você pode dar vários comandos de voz, como cadastrar eventos na agenda, ler a agenda, limpar a agenda, fazer perguntas à Wikipedia, obter previsões do tempo, abrir páginas web ou abrir aplicativos.

## Comandos

Alguns dos comandos que você pode usar incluem:

- "Cadastrar evento na agenda"
- "Ler agenda"
- "Limpar agenda"
- "Perguntar" (seguido da sua pergunta para a Wikipedia)
- "Preciso de um conselho"
- "Previsão do tempo" (seguido da cidade desejada)
- "Abrir YouTube"
- "Abrir Twitch"
- "Abrir VS Code"
- "Sair"

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests para melhorias e correções de bugs.

## Exemplo de Código

Aqui está um exemplo de como algumas funcionalidades estão implementadas:

```python
def falar(texto):
    sintetizador.say(texto)
    sintetizador.runAndWait()

def reconhecer_fala(timeout=None):
    with sr.Microphone() as mic:
        reconhecedor.adjust_for_ambient_noise(mic)
        try:
            audio = reconhecedor.listen(mic, timeout=timeout)
            texto = reconhecedor.recognize_google(audio, language="pt-BR")
            return texto
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            falar(f"Erro ao se comunicar com o serviço de reconhecimento: {e}")
            return None
        except Exception as e:
            falar(f"Ocorreu um erro: {e}")
            return None
```

Para mais detalhes sobre a implementação completa, consulte o código no repositório.

## Contato

Para perguntas e suporte, entre em contato com [kauesantana_13@hotmail.com](mailto:seu-email@example.com).

Este projeto foi criado como uma demonstração de um assistente virtual em Python. Sinta-se à vontade para adaptar e expandir conforme necessário!
