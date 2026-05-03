import os
import shutil
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import logging
from .rules import OrganizeRules

logger = logging.getLogger(__name__)

class FileOrganizer:
    """Responsável por organizar arquivos baseado nas regras"""
    
    def __init__(self, watch_folder: str, organize_folder: str):
        self.watch_folder = Path(watch_folder)
        self.organize_folder = Path(organize_folder)
        self.rules = OrganizeRules()
        self.stats = {
            'moved': 0,
            'errors': 0,
            'folders_created': set()
        }
        
    def organize_file(self, file_path: Path) -> bool:
        """Organiza um único arquivo"""
        try:
            # Verificar se arquivo ainda existe
            if not file_path.exists():
                return False
            
            # Calcular tamanho do arquivo em MB
            file_size_mb = file_path.stat().st_size / (1024 * 1024)
            
            # Determinar destino
            dest_folder_name, reason = self.rules.get_destination_folder(file_path, file_size_mb)
            dest_folder = self.organize_folder / dest_folder_name
            
            # Criar pasta destino se não existir
            dest_folder.mkdir(parents=True, exist_ok=True)
            self.stats['folders_created'].add(dest_folder)
            
            # Definir nome final (evitar conflitos)
            dest_path = dest_folder / file_path.name
            if dest_path.exists():
                # Adicionar timestamp se arquivo já existe
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
                dest_path = dest_folder / new_name
            
            # Mover arquivo
            shutil.move(str(file_path), str(dest_path))
            self.stats['moved'] += 1
            
            logger.info(f"✅ Movido: {file_path.name} → {dest_folder_name}/ ({reason})")
            return True
            
        except Exception as e:
            self.stats['errors'] += 1
            logger.error(f"❌ Erro ao processar {file_path.name}: {str(e)}")
            return False
    
    def organize_all_files(self) -> Dict:
        """Organiza todos os arquivos na pasta monitorada"""
        logger.info(f"🚀 Iniciando organização completa: {self.watch_folder}")
        
        files = [f for f in self.watch_folder.iterdir() if f.is_file()]
        
        for file_path in files:
            if self.rules.should_process_file(file_path.name):
                self.organize_file(file_path)
        
        self.print_summary()
        return self.stats
    
    def print_summary(self):
        """Exibe resumo da organização"""
        logger.info("\n" + "="*50)
        logger.info("📊 RESUMO DA ORGANIZAÇÃO")
        logger.info("="*50)
        logger.info(f"📁 Total movidos: {self.stats['moved']}")
        logger.info(f"❌ Erros: {self.stats['errors']}")
        logger.info(f"📂 Pastas criadas: {len(self.stats['folders_created'])}")
        logger.info("="*50 + "\n")