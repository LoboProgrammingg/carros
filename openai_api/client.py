import google.generativeai as genai
import os
genai.configure(api_key="AIzaSyCwELzwb39KYYc0oD5EEojGGI9eeFutFi8")

def get_car_ai_bio(model, brand, year):
    model_name = "gemini-1.0-pro-latest"
    prompt = f'''
    Me mostre uma descricao de venda para o carro {model} {brand} {year} em apenas 250 
    caracteres Fale coisas especificas desse modelo.'''
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text