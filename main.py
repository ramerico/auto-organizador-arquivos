#!/usr/bin/env python3
"""
Auto-Organizador de Arquivos
Monitora e organiza automaticamente arquivos em pastas específicas
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent))

from src.organizer import FileOrganizer
from src.monitor import FileMonitor

# Configurar logging
def setup_logging(log_level: str = "INFO"):
    """Configura o sistema de logs"""
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Criar pasta de logs se não existir
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Log file com data
    log_file = log_dir / f"organizer_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Configurar handlers
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(log_format, date_format))
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format, date_format))
    
    # Configurar root logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def main():
    """Função principal"""
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # Configurar argumentos de linha de comando
    parser = argparse.ArgumentParser(description="Auto-Organizador de Arquivos")
    parser.add_argument("--mode", choices=["once", "monitor"], default="once",
                       help="Modo de execução: once (única vez) ou monitor (contínuo)")
    parser.add_argument("--watch", type=str, 
                       default=os.getenv("WATCH_FOLDER", str(Path.home() / "Downloads")),
                       help="Pasta a ser monitorada")
    parser.add_argument("--organize", type=str,
                       default=os.getenv("ORGANIZE_FOLDER", str(Path.home() / "Organizado")),
                       help="Pasta onde organizar os arquivos")
    parser.add_argument("--log-level", type=str,
                       default=os.getenv("LOG_LEVEL", "INFO"),
                       choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                       help="Nível de logging")
    
    args = parser.parse_args()
    
    # Configurar logging
    logger = setup_logging(args.log_level)
    
    # Validar pastas
    watch_path = Path(args.watch)
    organize_path = Path(args.organize)
    
    if not watch_path.exists():
        logger.error(f"❌ Pasta não encontrada: {watch_path}")
        sys.exit(1)
    
    # Criar pasta de organização se não existir
    organize_path.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"📂 Monitorando: {watch_path}")
    logger.info(f"📂 Organizando em: {organize_path}")
    logger.info(f"⚙️ Modo: {args.mode}")
    
    # Executar modo escolhido
    if args.mode == "once":
        organizer = FileOrganizer(watch_path, organize_path)
        organizer.organize_all_files()
    else:
        monitor = FileMonitor(watch_path, organize_path)
        monitor.start()

if __name__ == "__main__":
    main()