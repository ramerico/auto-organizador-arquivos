import os
import shutil
from pathlib import Path
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class OrganizeRules:
    """Gerencia as regras de organização dos arquivos"""
    
    def __init__(self, custom_rules: Dict = None):
        # Regras padrão por extensão
        self.default_rules = {
            # Imagens
            '.jpg': 'Imagens', '.jpeg': 'Imagens', '.png': 'Imagens', 
            '.gif': 'Imagens', '.bmp': 'Imagens', '.svg': 'Imagens', '.webp': 'Imagens',
            
            # Documentos
            '.pdf': 'Documentos', '.doc': 'Documentos', '.docx': 'Documentos',
            '.txt': 'Documentos', '.rtf': 'Documentos', '.odt': 'Documentos',
            
            # Planilhas
            '.xls': 'Planilhas', '.xlsx': 'Planilhas', '.csv': 'Planilhas',
            
            # Apresentações
            '.ppt': 'Apresentacoes', '.pptx': 'Apresentacoes',
            
            # Vídeos
            '.mp4': 'Videos', '.avi': 'Videos', '.mkv': 'Videos', 
            '.mov': 'Videos', '.wmv': 'Videos', '.flv': 'Videos',
            
            # Áudios
            '.mp3': 'Audios', '.wav': 'Audios', '.flac': 'Audios', 
            '.aac': 'Audios', '.ogg': 'Audios',
            
            # Arquivos compactados
            '.zip': 'Compactados', '.rar': 'Compactados', '.7z': 'Compactados',
            '.tar': 'Compactados', '.gz': 'Compactados',
            
            # Código
            '.py': 'Codigo/Python', '.js': 'Codigo/JavaScript', '.html': 'Codigo/Web',
            '.css': 'Codigo/Web', '.json': 'Codigo/Dados', '.xml': 'Codigo/Dados',
            '.java': 'Codigo/Java', '.cpp': 'Codigo/Cpp', '.c': 'Codigo/C',
            
            # Executáveis
            '.exe': 'Executaveis', '.msi': 'Executaveis', '.app': 'Executaveis',
            '.deb': 'Executaveis', '.sh': 'Scripts',
            
            # Outros
            '.torrent': 'Torrents', '.iso': 'Discos', '.log': 'Logs'
        }
        
        # Regras especiais por tamanho
        self.size_rules = {
            'large_files': {
                'min_size_mb': 100,
                'folder': 'Arquivos_Grandes_+100MB'
            }
        }
        
        # Merge com regras customizadas
        if custom_rules:
            self.default_rules.update(custom_rules)
    
    def get_destination_folder(self, file_path: Path, file_size_mb: float) -> Tuple[str, str]:
        """
        Determina a pasta de destino baseado nas regras
        Retorna: (nome_pasta, motivo)
        """
        # Regra 1: Verificar tamanho
        if self.size_rules['large_files']['min_size_mb']:
            if file_size_mb >= self.size_rules['large_files']['min_size_mb']:
                return self.size_rules['large_files']['folder'], "Arquivo grande (+100MB)"
        
        # Regra 2: Verificar extensão
        extension = file_path.suffix.lower()
        folder = self.default_rules.get(extension)
        
        if folder:
            return folder, f"Extensão {extension}"
        
        # Regra 3: Sem regra definida
        return "Outros", "Extensão não mapeada"
    
    def should_process_file(self, filename: str) -> bool:
        """Define se o arquivo deve ser processado"""
        # Ignorar arquivos temporários e ocultos
        ignore_patterns = ['.tmp', '.temp', '~', '.crdownload', '.part']
        return not any(pattern in filename.lower() for pattern in ignore_patterns)