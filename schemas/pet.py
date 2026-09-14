import re
from datetime import datetime, date
from typing import Optional, List
from model.pet import Pet

# Constantes de validação
ESPECIES_OPCOES = ["Cachorro", "Gato"]
PET_SEXO_OPCOES = ["Fêmea", "Macho"]
UFS_VALIDAS = {
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 
    'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 
    'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
}

# Funções Auxiliares / Helpers
def parse_date_ddmmyyyy(value: str) -> Optional[date]:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%d/%m/%Y").date()
    except ValueError:
        return None

def format_date_ddmmyyyy(d: date) -> Optional[str]:
    if not d:
        return None
    return d.strftime("%d/%m/%Y")

def normalize_color_to_masculine(color: str) -> Optional[str]:
    if not color:
        return None
    
    c = re.sub(r'\s+', ' ', color.strip()).lower()
    
    if c == 'cinza':
        return 'cinza'
    
    if c.endswith('a'):
        c = c[:-1] + 'o'
        
    return c

def is_valid_uf(uf: str) -> bool:
    if not uf:
        return False
    return uf.strip().upper() in UFS_VALIDAS

# Serializadores de Resposta
def apresenta_pet(pet: Pet) -> dict:
    """ Retorna a representação de um único pet em formato JSON/Dicionário """
    return {
        "id": pet.id,
        "nome": pet.nome,
        "especie": pet.especie,
        "sexo": pet.sexo,
        "cor_pelagem": pet.cor_pelagem,
        "raca": pet.raca,
        "idade": pet.idade,
        "bairro": pet.bairro,
        "municipio": pet.municipio,
        "uf": pet.uf,
        "foto": pet.foto,
    }

def apresenta_pets(pets: List[Pet]) -> list:
    """ Retorna uma lista formatada de pets """
    return [apresenta_pet(p) for p in pets]