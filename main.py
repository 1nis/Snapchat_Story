import json
import uuid
import requests
import os
import re
import time
import logging
from datetime import datetime
from tqdm import tqdm
from logging.handlers import RotatingFileHandler

class SnapchatDownloader2025:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._configure_logging()
        self.session = requests.Session()
        self._configure_session()

    def _configure_logging(self):
        """Configuration avancée du logging avec 3 niveaux de traces"""
        log_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(module)s:%(lineno)d - %(message)s'
        )

        # Fichier de log avec rotation
        file_handler = RotatingFileHandler(
            'snapchat_debug.log',
            maxBytes=5*1024*1024,  # Gestion taille max de fichier (ici 5 Mo)
            backupCount=3,
            encoding='utf-8'
        )
        file_handler.setFormatter(log_formatter)
        file_handler.setLevel(logging.DEBUG)

        # Console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        console_handler.setLevel(logging.INFO)

        # Logger principal
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def _configure_session(self):
        """Journalisation détaillée de la configuration"""
        self.logger.debug("Configuration de la session HTTP...")
        try:
            device_id = f"ANDROID-{uuid.uuid4().hex.upper()}"
            self.session.headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 14; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36',
                'X-Snapchat-Device-ID': device_id,
                'Accept-Language': 'fr-FR,fr;q=0.9'
            }
            self.logger.debug(f"Headers configurés avec Device-ID: {device_id}")
        except Exception as e:
            self.logger.critical("Échec configuration session: %s", str(e), exc_info=True)
            raise

    def _get_profile_url(self, username: str) -> str:
        """Journalisation des URLs générées"""
        url = f"https://www.snapchat.com/add/{username.lstrip('@')}"
        self.logger.debug(f"URL générée: {url}")
        return url

    def _get_story_data(self, username: str) -> dict:
        """Journalisation détaillée du processus d'extraction"""
        self.logger.info("Début extraction données pour @%s", username)
        try:
            profile_url = self._get_profile_url(username)
            
            self.logger.debug("Requête GET vers: %s", profile_url)
            response = self.session.get(profile_url, allow_redirects=True, timeout=15)
            response.raise_for_status()

            self.logger.debug("Analyse réponse HTTP %d", response.status_code)
            if 'Ce compte est privé' in response.text:
                self.logger.warning("Compte privé détecté")
                raise PermissionError("Accès refusé - Compte privé")

            json_match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', response.text)
            if not json_match:
                self.logger.error("Balise JSON introuvable dans le HTML")
                return {}

            self.logger.debug("Tentative désérialisation JSON")
            return json.loads(json_match.group(1))

        except requests.HTTPError as e:
            self.logger.error("Erreur HTTP %d: %s", e.response.status_code, str(e), exc_info=True)
            return {}
        except json.JSONDecodeError as e:
            self.logger.error("Échec décodage JSON: %s", str(e), exc_info=True)
            return {}
        except Exception as e:
            self.logger.error("Erreur inattendue: %s", str(e), exc_info=True)
            return {}

    def download_stories(self, username: str):
            """Journalisation complète du flux principal"""
            self.logger.info("=== Début processus pour @%s ===", username)
            try:
                start_time = time.time() 
                
                data = self._get_story_data(username)
                
                if not data:
                    self.logger.warning("Aucune donnée disponible après extraction")
                    return

                # Extraction des URLs avec type de média
                media_data = [
                    (snap['snapUrls']['mediaUrl'], snap.get('snapMediaType'))
                    for snap in data.get('props', {}).get('pageProps', {}).get('story', {}).get('snapList', [])
                    if snap.get('snapMediaType') in [0, 1]  # 0=Image, 1=Video
                ]

                if not media_data:
                    self.logger.warning("Liste de médias vide - Vérifier : %s", self._get_profile_url(username))
                    return

                save_dir = f"downloads/{username}_{datetime.now().strftime('%Y%m%d')}"
                self.logger.debug("Création répertoire: %s", save_dir)
                os.makedirs(save_dir, exist_ok=True)

                success_count = 0
                for idx, (url, media_type) in enumerate(media_data, 1):
                    try:
                        # Génération du nom de fichier avec extension correcte
                        extension = self._get_extension(media_type, url)
                        filename = f"{idx}_{datetime.now().strftime('%H%M%S')}{extension}"
                        filepath = os.path.join(save_dir, filename)
                        
                        self.logger.debug("Téléchargement %d/%d: %s", idx, len(media_data), url)
                        
                        if self._download(url, filepath):
                            success_count += 1
                            self.logger.debug("Fichier sauvegardé: %s", filepath)
                        
                        time.sleep(1.5)
                    
                    except Exception as e:
                        self.logger.error("Échec téléchargement média: %s", str(e), exc_info=True)

                self.logger.info("=== Succès: %d/%d (en %.2fs) ===", 
                            success_count, len(media_data), time.time()-start_time)

            except Exception as e:
                self.logger.critical("ÉCHEC CRITIQUE: %s", str(e), exc_info=True)
                raise

    def _get_extension(self, media_type: int, url: str) -> str:
            """Détermine l'extension du fichier selon le type de média"""
            if media_type == 1:
                return '.mp4'
            elif media_type == 0:
                return '.jpg'
            else:
                return os.path.splitext(url)[1]  # Fallback sur l'extension originale

    def _download(self, url: str, path: str) -> bool:
        """Journalisation détaillée du téléchargement"""
        try:
            self.logger.debug("Début téléchargement: %s", url)
            with self.session.get(url, stream=True, timeout=30) as r:
                r.raise_for_status()
                
                content_type = r.headers.get('Content-Type', '')
                if 'video' in content_type:
                    path = path.replace('.jpg', '.mp4')
                elif 'image' in content_type:
                    path = path.replace('.mp4', '.jpg')
                
                total_size = int(r.headers.get('content-length', 0))
                self.logger.debug("Taille détectée: %d octets", total_size)
                
                with open(path, 'wb') as f, tqdm(
                    desc=f"Download {os.path.basename(path)}",
                    total=total_size,
                    unit='B',
                    unit_scale=True
                ) as bar:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                        bar.update(len(chunk))
            
            self.logger.debug("Téléchargement réussi: %s", path)
            return True
            
        except Exception as e:
            self.logger.error("ÉCHEC %s: %s", url, str(e), exc_info=True)
            return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py username")
        sys.exit(1)

    try:
        SnapchatDownloader2025().download_stories(sys.argv[1].lstrip('@'))
    except Exception as e:
        logging.critical("ERREUR NON GÉRÉE: %s", str(e), exc_info=True)
        sys.exit(1)
