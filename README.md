# Casa Arcana

Casa Arcana reúne quatro ferramentas esotéricas numa única aplicação FastAPI: gerador de sons, oráculo astrológico, mapa natal e Tarot. Cada ferramenta tem uma rota própria e a página inicial apresenta a navegação comum.

## Executar localmente

Requer Python 3.10 ou superior. NumPy e SciPy usam versões compatíveis com o interpretador selecionado.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

For local tests, install development-only dependencies with `pip install -r requirements-dev.txt`.

Abra http://127.0.0.1:5000.

## Rotas

- `/` — página inicial
- `/sound/` e `/sound/frequencies` — sons de chakras e frequências; `/sound/audio/{note}` serve áudio WAV
- `/oracle/` — oráculo astrológico
- `/natal/`, `/natal/glossary` — mapa natal e glossário; `POST /natal/calculate` e `GET /natal/api/glossary`
- `/tarot/` — leituras de Tarot; `POST /tarot/reading`

O cálculo do mapa natal usa Nominatim para resolver cidades que não estejam entre as localidades de demonstração; esse fluxo precisa de acesso à rede. Os projetos de origem permanecem separados e não são alterados.

## Deploy

Use o comando de start `uvicorn main:app --host 0.0.0.0 --port $PORT` e instale as dependências de `requirements.txt`.
