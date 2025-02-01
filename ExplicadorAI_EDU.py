import openai
import sys
from typing import Dict, List, Optional
import json
import time
from openai import OpenAI

api_key = "API_KEY"

class TutorPython:
    def __init__(self, api_key: str):
        """Inicializar o Tutor de Python com a chave API OpenAI."""
        self.client = OpenAI(api_key=api_key)
        self.historico_conversa = []
        self.nivel_dificuldade = "1º a 4º ano de ensino básico"
        
    def definir_dificuldade(self, nivel: str) -> None:
        """Definir o nível de dificuldade para o tutor."""
        niveis_validos = ["1º a 4º ano de ensino básico", "5º a 6º ano de ensino básico", "7º a 9º ano de ensino básico", "10º a 12º ano de ensino básico", "universidade"]
        if nivel.lower() in niveis_validos:
            self.nivel_dificuldade = nivel.lower()
        else:
            raise ValueError(f"Nível de dificuldade inválido. Escolha entre {niveis_validos}")

    def gerar_resposta(self, entrada_usuario: str) -> str:
        """Gerar uma resposta usando a API OpenAI."""
        try:
            # Construir o contexto da conversa
            mensagens = [
                {"role": "system", "content": f"""És um explicador a ensinar um aluno do {self.nivel_dificuldade} num exercício da escola . Responde em português de Portugal. NUNCA dês a resposta final"""},
            ]
            
            # Adicionar histórico de conversa
            mensagens.extend(self.historico_conversa)
            
            # Adicionar entrada atual do utilizador
            mensagens.append({"role": "user", "content": entrada_usuario})
            
            # Fazer chamada à API
            resposta = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=mensagens,
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extrair e armazenar a resposta
            resposta_tutor = resposta.choices[0].message.content
            self.historico_conversa.append({"role": "user", "content": entrada_usuario})
            self.historico_conversa.append({"role": "assistant", "content": resposta_tutor})
            
            return resposta_tutor
            
        except Exception as e:
            return f"Ocorreu um erro: {str(e)}"


    def exercicio(self, topico: str) -> Dict:
        """Ajudar o aluno com um exercício."""
        try:
            prompt = f"""
            
            Cria um exercício de {topico} para um aluno do {self.nivel_dificuldade}. 
            Vai direto ao assunto e apresenta só o enunciado, não referencies imagens se não for necessário, ou incluires um link.
            
            Responde em português de Portugal."""
            
            resposta = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "És um explicador em português de Portugal que ajuda um aluno a chegar á resposta de um exercício sem lhe dar o resultado final, apenas indicando a direção certa."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8
            )
            
            resposta_tutor = resposta.choices[0].message.content
            self.historico_conversa.append({"role": "assistant", "content": resposta_tutor})
            
            return resposta_tutor
            
        except Exception as e:
            return {"erro": str(e)}

    def limpar_historico(self) -> None:
        """Limpar o histórico da conversa."""
        self.historico_conversa = []

def main():
    """Função principal para demonstrar o uso."""
    # Substitua pela sua chave API OpenAI
    tutor = TutorPython(api_key)
    
    print("Bem-vindo ao Tutor de Python! Escreve 'sair' para terminar.")
    print("Comandos disponíveis:")
    print("- 'definir_dificuldade [nível]': Define o nível de dificuldade (iniciante/intermediário/avançado)")
    print("- 'exercicio [tópico]': Gera um exercício para um tópico específico")
    print("- 'limpar': Limpa o histórico da conversa")
    
    while True:
        entrada_usuario = input("\nTu: ").strip()
        
        if entrada_usuario.lower() == 'sair':
            break
            
        if entrada_usuario.lower() == 'limpar':
            tutor.limpar_historico()
            print("Histórico da conversa limpo.")
            continue
            
        if entrada_usuario.startswith('definir_dificuldade'):
            _, nivel = entrada_usuario.split(' ', 1)
            try:
                tutor.definir_dificuldade(nivel)
                print(f"Nível de dificuldade definido para: {nivel}")
            except ValueError as e:
                print(e)
            continue
            
            
        if entrada_usuario.startswith('exercicio'):
            _, topico = entrada_usuario.split(' ', 1)
            resposta = tutor.exercicio(topico)
            print("\nResposta:")
            print(resposta)
            
            continue
            
        resposta = tutor.gerar_resposta(entrada_usuario)
        print("\nTutor:", resposta)

if __name__ == "__main__":
    main()
    