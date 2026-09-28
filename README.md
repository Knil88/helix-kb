# Helix Formazione — parser e indice della knowledge base

Programma Python che, data una cartella di documenti (`.txt`, `.md`, `.csv`), estrae contenuto e metadati, li normalizza in un modello comune e costruisce un indice ricercabile. I file vuoti, corrotti o con estensione non gestita vengono scartati con un motivo; lo scan continua.

Aggiungere un formato = una sottoclasse di `FormatParser` + una riga in `PARSERS` (`helix_kb/parsers.py`).

**Repository:** https://github.com/Knil88/helix-kb  
**Colab di consegna:** *(il link si aggiunge dopo)*  

Questo repository è la **fonte del codice**. Il notebook Colab clona la repo e importa i moduli.

## Struttura

```text
helix_kb/          pacchetto Python
  document.py      modello Document
  exceptions.py    errori di parsing
  parsers.py       lettori per formato + parse_folder
  knowledge_base.py indice (list, search, filter, stats)
  cli.py           interfaccia da riga di comando
archive/           archivio di prova (sera R2)
```

## Installazione (Windows)

```text
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

Solo standard library: `requirements.txt` non aggiunge dipendenze esterne.

## Esecuzione

Cartella `archive/` inclusa nel repository (15 file di prova, di cui 3 casi limite):

```text
helix-kb --folder archive --index kb_index.json
```

Oppure:

```text
python -m helix_kb.cli --folder archive
```
