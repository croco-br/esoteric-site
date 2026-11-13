import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent

with (ROOT / 'cards.json').open('r') as f:
    cards = json.load(f)
    
with (ROOT / 'readings.json').open('r') as f:
    readings = json.load(f)    
    
def generate_reading(reading_type):
    tarot_cards = cards.get('tarot_cards', [])
    reading_list = readings.get('reading_list', [])

    selected_reading = reading_list.get(reading_type)

    num_cards = len(selected_reading['questions'])
    selected_cards = random.sample(tarot_cards, min(num_cards, len(tarot_cards)))
    
    result = {
        "reading_type": reading_type,
        "questions_and_cards": list(zip(selected_reading['questions'], selected_cards))
    }
    
    return result
