from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import logging
from pathlib import Path
from .organizer import FileOrganizer

logger = logging.getLogger(__name__)

class FileHandler(FileSystemEventHandler):
    """Handler para eventos do sistema de arquivos"""
    
    def __init__(self, organizer: FileOrganizer, delay_seconds: int = 2):
        self.organizer = organizer
        self.delay = delay_seconds
        self.pending_files = {}
        
    def on_created(self, event):
        """Quando um arquivo é criado"""
        if not event.is_directory:
            # Pequeno delay para garantir que o arquivo foi completamente escrito
            time.sleep(self.delay)
            self.organizer.organize_file(Path(event.src_path))
    
    def on_modified(self, event):
        """Quando um arquivo é modificado"""
        if not event.is_directory:
            self.organizer.organize_file(Path(event.src_path))

class FileMonitor:
    """Monitora pastas em tempo real"""
    
    def __init__(self, watch_folder: str, organize_folder: str):
        self.watch_folder = watch_folder
        self.organizer = FileOrganizer(watch_folder, organize_folder)
        self.observer = Observer()
        
    def start(self):
        """Inicia o monitoramento"""
        event_handler = FileHandler(self.organizer)
        self.observer.schedule(event_handler, self.watch_folder, recursive=False)
        self.observer.start()
        
        logger.info(f"👀 Monitorando: {self.watch_folder}")
        logger.info(f"📂 Organizando em: {self.organizer.organize_folder}")
        logger.info("🔘 Pressione Ctrl+C para parar")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Para o monitoramento"""
        self.observer.stop()
        self.observer.join()
        logger.info("\n✅ Monitoramento encerrado")