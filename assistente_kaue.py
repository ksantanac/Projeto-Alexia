import speech_recognition as sr
import pyttsx3
import wikipedia
import requests
from googletrans import Translator
import webbrowser
from api_key import api_keym, api_gemini
import subprocess
import google.generativeai as genai


reconhecedor = sr.Recognizer()
sintetizador = pyttsx3.init()

wikipedia.set_lang("pt")

def falar(texto):
    sintetizador.say(texto)
    sintetizador.runAndWait()

def reconhecer_fala(timeout=None):
    with sr.Microphone() as mic:
        reconhecedor.adjust_for_ambient_noise(mic)
        try:
            print("Ouvindo...")
            audio = reconhecedor.listen(mic, timeout=timeout)
            print("Reconhecendo...")
            texto = reconhecedor.recognize_google(audio, language="pt-BR")
            print("Você disse: " + texto)
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

def cadastrar_evento():
    falar("Ok, qual evento devo cadastrar?")
    evento = reconhecer_fala()
    if evento:
        with open("agenda.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(evento + "\n")
        falar(f"Evento '{evento}' cadastrado com sucesso.")
    else:
        falar("Não foi possível cadastrar o evento.")

def ler_agenda():
    try:
        with open("agenda.txt", "r", encoding="utf-8") as arquivo:
            eventos = arquivo.readlines()
        if eventos:
            falar("Aqui estão seus eventos cadastrados:")
            for evento in eventos:
                falar(evento.strip())
        else:
            falar("Sua agenda está vazia.")
            falar("Deseja cadastrar um evento?")
            resposta = reconhecer_fala()
            if resposta and 'sim' in resposta.lower():
                cadastrar_evento()
            else:
                falar("Ok, não foi cadastrado nenhum evento.")
    except FileNotFoundError:
        falar("Você ainda não tem eventos cadastrados. Deseja cadastrar?")
        resposta = reconhecer_fala()
        if resposta and 'sim' in resposta.lower():
            cadastrar_evento()
        else:
            falar("Ok, não foi cadastrado nenhum evento.")

def limpar_agenda():
    with open("agenda.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write("")
    falar("Sua agenda foi limpa com sucesso.")

def perguntar_a_wikipedia(query):
    try:
        falar("Pesquisando na Wikipedia...")
        summary = wikipedia.summary(query, sentences=1)
        falar(summary)
        print(summary)
    except wikipedia.DisambiguationError as e:
        falar("A consulta retornou muitos resultados. Por favor, seja mais específico.")
    except wikipedia.PageError:
        falar("Não encontrei nenhum resultado para a sua pesquisa.")
    except Exception as e:
        falar(f"Erro ao realizar a pesquisa: {e}")

def obter_conselho_traduzido():
    r = requests.get('https://api.adviceslip.com/advice')
    conselho = r.json()['slip']['advice']
    tradutor = Translator()
    conselho_traduzido = tradutor.translate(conselho, src='en', dest='pt').text
    return conselho_traduzido

def deseja_continuar():
    falar('Mestre, posso ajudar em algo mais?')
    for r in range(3):  # Tentar reconhecer até 3 vezes
        resposta = reconhecer_fala()
        if resposta:
            if 'sim' in resposta.lower():
                falar('O que você precisa, mestre?')
                return True
            elif 'não' in resposta.lower() or 'nao' in resposta.lower():
                falar('Obrigado, mestre. Até a próxima!')
                return False
        falar('Não consegui entender. Você precisa de mais alguma coisa?')
    falar('Não houve resposta clara. Até a próxima, mestre!')
    return False

def previsao_do_tempo(cidade):
    api_key = api_keym  # Substitua pela sua chave da API do OpenWeatherMap
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + cidade + "&appid=" + api_key + "&lang=pt&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        weather = data["weather"][0]
        temperatura = main["temp"]
        descricao = weather["description"]
        falar(f"Atualmente, em {cidade}, está {descricao} com temperatura de {temperatura} graus Celsius.")
    else:
        falar("Cidade não encontrada.")

def ouvir_comando_inicial():
    while True:
        comando_inicial = reconhecer_fala()
        if comando_inicial:
            comando_inicial_lower = comando_inicial.lower()
            if "ok sexta-feira" in comando_inicial_lower:
                return True
            elif "sair" in comando_inicial_lower:
                falar("Até logo, mestre.")
                return False
            else:
                falar('Fale "ok sexta-feira" para iniciar o programa ou "sair" para encerrar.')
        else:
            falar('Não consegui entender. Por favor, fale "ok sexta-feira" para iniciar o programa ou "sair" para encerrar.')

def abrir_pagina_web(url):
    webbrowser.open(url)
    falar(f"Abrindo")

def abrir_vscode():
    try:
        subprocess.Popen(r"C:\Users\Kaue\AppData\Local\Programs\Microsoft VS Code\Code.exe")
        falar("Abrindo o aplicativo.")
    except Exception as e:
        falar(f"Não consegui abrir o aplicativo: {e}")


def geminiAi(pergunta):
    # Configure a chave da API
    genai.configure(api_key=api_gemini)

    # Lista os modelos disponíveis e verifica se eles suportam 'generateContent'
    model_name = None
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            model_name = m.name
            break

    if model_name:
        # Inicializa o modelo
        model = genai.GenerativeModel(model_name)

        # Gera o conteúdo com a pergunta

        response = model.generate_content(f"{pergunta}")

        # Imprime apenas o texto da resposta
        resposta = response.text

        return resposta

    else:
        print("Nenhum modelo com suporte para 'generateContent' foi encontrado.")



def main():
    falar("Fala comigo!")
    while True:
        if ouvir_comando_inicial():
            falar("Sim, mestre. O que posso fazer?")
            while True:
                comando = reconhecer_fala(timeout=5)
                if comando:
                    comando_lower = comando.lower()

                    if "cadastrar evento na agenda" in comando_lower:
                        cadastrar_evento()
                        if not deseja_continuar():
                            break

                    elif "ler agenda" in comando_lower:
                        ler_agenda()
                        if not deseja_continuar():
                            break

                    elif "limpar agenda" in comando_lower:
                        limpar_agenda()
                        if not deseja_continuar():
                            break

                    elif "perguntar" in comando_lower:
                        falar("O que você quer pesquisar?")
                        query = reconhecer_fala(timeout=6)
                        if query:
                            perguntar_a_wikipedia(query)
                        if not deseja_continuar():
                            break

                    elif "preciso de um conselho" in comando_lower:
                        falar(f'Aqui está o seu conselho Mestre: {obter_conselho_traduzido()}')
                        if not deseja_continuar():
                            break

                    elif "previsão do tempo" in comando_lower:
                        falar("Para qual cidade você quer a previsão do tempo?")
                        cidade = reconhecer_fala(timeout=10)
                        if cidade:
                            previsao_do_tempo(cidade)
                        if not deseja_continuar():
                            break

                    elif "abrir youtube" in comando_lower:
                        abrir_pagina_web("https://www.youtube.com")
                        if not deseja_continuar():
                            break

                    elif "abrir twitch" in comando_lower:
                        abrir_pagina_web("https://www.twitch.tv")
                        if not deseja_continuar():
                            break

                    elif "abrir vs code" in comando_lower:
                        abrir_vscode()
                        if not deseja_continuar():
                            break

                    elif "falar com gemini" in comando_lower:
                        falar("O que você gostaria de saber?")
                        pergunta = reconhecer_fala(timeout=10)
                        if pergunta:
                            resposta = geminiAi(pergunta)
                            if resposta:
                                falar(f"{resposta}")
                            else:
                                falar("Não consegui obter uma resposta do Gemini.")
                        if not deseja_continuar():
                            break


                    elif "sair" in comando_lower:
                        falar("Até logo, mestre.")
                        return
                    else:
                        falar("Comando não reconhecido. Por favor, diga novamente.")
                else:
                    falar("Não consegui entender. Por favor, diga novamente.")
        else:
            break

if __name__ == "__main__":
    main()
