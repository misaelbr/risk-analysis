import requests 
import pandas as pd
import os

from dotenv import load_dotenv

load_dotenv()

class DataFetcher:
    """ 
    Gerencia a coleta de dados da API Financeira
    """
    def __init__(self):
        self.api_url = os.getenv('API_URL')
        self.api_key = os.getenv('API_KEY')
        
        if not self.api_url or not self.api_key:
            raise ValueError('[Erro] API_URL e API_KEY não podem ser nulos')
        
    def fetch_historical_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        """ 
        Coleta os dados históricos da API e retorna um pandas DataFrame
        """
        params = {
            "api_key": self.api_key,
            "start_date": start_date,
            "end_date": end_date
        }
        
        try:
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            return pd.DataFrame(data['dataset_data']['data'], columns=data['dataset_data']['column_names'])

        except requests.exceptions.RequestException as e:
            print(f'[Erro] Ocorreu um erro ao buscar dados da API: {e}')
            raise
            
        except KeyError as e:
            print(f'[Erro] Estrutura de dados incompatível: {e}')
            raise
        