import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random as rd
import time
ponto=0
words_by_level = {
    "fácil": ["gato", "cachorro", "maçã", "leite", "sol"],
    "médio": ["casa", "escola", "amigo", "janela", "amarelo"],
    "difícil": ["tecnologia", "universidade", "informação", "pronúncia", "imaginação"]
}
def verificar_palavra():
    global ponto
    translator = Translator()
    traducao = translator.translate(palavra, src='pt', dest='en').text
    time.sleep(2)
    duration = 3  # segundos de gravação
    sample_rate = 44100
    print("Fale agora...")
    recording = sd.rec(
    int(duration * sample_rate), # o número de amostras a serem registradas
    samplerate=sample_rate,      # taxa de amostras
    channels=1,                  # 1 significa gravação mono
    dtype="int16")               # tipo de dados para as amostras registradas
    sd.wait()  # aguardando o término da gravação 
    
    wav.write("output.wav", sample_rate, recording)
    print("Gravação concluída, estou reconhecendo...")
    
    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)
            
    try:
        text = recognizer.recognize_google(audio, language="en")
        print("Seu resultado foi:", text)
        time.sleep(3)
        if text.strip().lower() == traducao.strip().lower():
            print("✅ Acertou!")
            ponto+=1
            print(f'voce tem {ponto} ponto(s)')
            time.sleep(3)
        else:
            print(f"❌ Errou! A resposta certa era: {traducao}")
            print(f'voce tem {ponto} pontos')
            time.sleep(3)
            
    except sr.UnknownValueError:             # - se o Google não conseguiu entender a fala devido a ruídos ou silêncio
        print("A fala não pôde ser reconhecida.")
    except sr.RequestError as e:             # - se não houver conexão com a Internet ou a API estiver indisponível
        print(f"Service error: {e}")
while True:
    print('Bem vindo ao jogo da pronuncia')
    dificuldade=input('qual dificuldade voce quer Dificil(D),Medio(M) ou Facil(F)?').lower()
    if dificuldade == 'd':
        palavra=rd.choice(words_by_level["difícil"])
        print(palavra)
        verificar_palavra()
    elif dificuldade == 'm':
        palavra=rd.choice(words_by_level["médio"])
        print(palavra)
        verificar_palavra()
    elif dificuldade == 'f':
        palavra=rd.choice(words_by_level["fácil"])
        print(palavra)
        verificar_palavra()
    else:
        print("Opção inválida!")