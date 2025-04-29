import os
import json
import logging
import glob
import shutil
# Funzione per ottenere il percorso base del progetto
def get_base_dir():
    return os.path.dirname(os.path.abspath(__file__))

# Funzione per ottenere la cartella logs
def get_logs_dir():
    log_dir = os.path.join(get_base_dir(), 'logs')
    os.makedirs(log_dir, exist_ok=True)  # Crea la cartella logs se non esiste
    return log_dir

# Funzione per ottenere la cartella response dentro logs
def get_response_dir():
    response_dir = os.path.join(get_logs_dir(), 'response')
    os.makedirs(response_dir, exist_ok=True)  # Crea la cartella response se non esiste
    return response_dir

# ✅ **Percorso fisso per il log globale**
def get_log_path():
    return os.path.join(get_logs_dir(), 'LOG.log')

# ✅ **Percorso per i file JSON di risposta API**
def get_response_json_path(api_name, details):
    return os.path.join(get_response_dir(), f'RESPONSE_{api_name}_{details}.json')

# Funzione per caricare la configurazione JSON
def load_config():
    config_path = os.path.join(get_base_dir(), 'config.json')
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                return json.load(f) or {}  # Se il file è vuoto, ritorna un dict vuoto
        except json.JSONDecodeError:
            print(f"⚠️  Errore: {config_path} è corrotto. Ricreazione del file...")
            return {}  
    return {}  

def load_credentials():
    credentials_path = os.path.join(get_base_dir() ,'EnvironmentCredentials', 'credentials.json')
    if os.path.exists(credentials_path):
        try:
            with open(credentials_path, 'r') as f:
                return json.load(f) or {}  # Se il file è vuoto, ritorna un dict vuoto
        except json.JSONDecodeError:
            print(f"⚠️  Errore: {credentials_path} è corrotto. Ricreazione del file...")
            return {}  
    return {}  


# Funzione per salvare la configurazione nel file JSON
def save_config(config):
    with open(os.path.join(get_base_dir(), 'config.json'), 'w') as f:
        json.dump(config, f, indent=4)

# Funzione per aggiungere un campo alla configurazione
def update_config(key, value):
    config = load_config()
    config.setdefault("path", {})[key] = value  
    save_config(config)

# ✅ **Funzione per configurare il logging globale**
def setup_logging():
    log_path = get_log_path()

    # ✅ Resetta i gestori esistenti prima di riconfigurarlo
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return log_path  # Restituisce il percorso del file log

# ✅ **Funzione per eliminare il file di log e tutti i file nella cartella response**
def reset_log():
    log_path = get_log_path()
    response_path = get_response_dir()
    
    # Eliminazione del file di log
    if os.path.exists(log_path):
        os.remove(log_path)
        print(f"🗑️ Log eliminato: {log_path}")

    # Eliminazione di tutti i file nella cartella response
    if os.path.exists(response_path):
        files = glob.glob(os.path.join(response_path, '*'))  # Trova tutti i file
        for f in files:
            os.remove(f)
            print(f"🗑️ Eliminato file nella response: {f}")

    # Dopo la pulizia, ricrea il file di log
    setup_logging()

def remove_pycache():
    """
    Recursively removes all `__pycache__` directories in the project.

    @return: None

    Process:
    - Searches for all `__pycache__` directories starting from the project's base directory.
    - Deletes each `__pycache__` folder along with its contents.
    - Logs the operation.

    Requirements:
    - Logging should be configured using `setup_logging()` before calling this function.

    Raises:
    - Logs an error if a directory cannot be removed.
    """

    base_dir = get_base_dir()
    removed_dirs = []

    for root, dirs, files in os.walk(base_dir):
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            try:
                shutil.rmtree(pycache_path)
                removed_dirs.append(pycache_path)
                logging.info(f"🗑️ Removed: {pycache_path}")
            except Exception as e:
                logging.error(f"❌ Error removing {pycache_path}: {e}")

    if removed_dirs:
        print(f"✅ Removed {len(removed_dirs)} `__pycache__` directories.")
    else:
        print("⚠️ No `__pycache__` directories found.")
