import requests

PESSOA_SERVICE_BASE_URL = "http://localhost:5000/teachers"
ALUNO_SERVICE_BASE_URL = "http://localhost:5000/students"

class PessoaServiceClient:
    @staticmethod
    def get_professor_data(professor_id):
        url = f"{PESSOA_SERVICE_BASE_URL}/{professor_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"Professor com ID {professor_id} não encontrado no serviço externo.")
            else:
                print(f"Erro HTTP ao acessar o serviço de professores: {e.response.status_code} - {e.response.text}")
            return None
        except requests.RequestException as e:
            print(f"Erro de conexão ao acessar o serviço de professores: {e}")
            return None
        except Exception as e:
            print(f"Erro inesperado ao obter dados do professor: {e}")
            return None

    @staticmethod
    def get_aluno_data(aluno_id):
        """
        Obtém os dados de um aluno específico do serviço externo.
        (Adicionado para enriquecer respostas também, se necessário)
        
        Args:
            aluno_id (int): O ID do aluno no serviço externo.

        Returns:
            dict or None: Um dicionário com os dados do aluno, ou None se não encontrado/erro.
        """
        url = f"{ALUNO_SERVICE_BASE_URL}/{aluno_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"Aluno com ID {aluno_id} não encontrado no serviço externo.")
            else:
                print(f"Erro HTTP ao acessar o serviço de alunos: {e.response.status_code} - {e.response.text}")
            return None
        except requests.RequestException as e:
            print(f"Erro de conexão ao acessar o serviço de alunos: {e}")
            return None
        except Exception as e:
            print(f"Erro inesperado ao obter dados do aluno: {e}")
            return None