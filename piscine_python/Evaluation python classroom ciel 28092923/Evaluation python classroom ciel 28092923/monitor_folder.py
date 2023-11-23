import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return

        # Obtenez les informations sur le fichier
        file_path = event.src_path
        file_name = os.path.basename(file_path)

        # Générez le contenu du fichier journal
        log_content = f"Date/Heure : {datetime.now()}\nNom du fichier : {file_name}\n"

        # Nom du fichier journal
        log_file_name = "log.txt"

        # Ajoutez une nouvelle ligne au fichier journal existant ou créez un nouveau fichier s'il n'existe pas
        with open(log_file_name, 'a') as log_file:
            log_file.write(log_content + '\n')

        print(f"Ajout d'une nouvelle ligne au fichier journal : {log_file_name}")

if __name__ == "__main__":
    path = "/home/souquetl/script_eval"
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        print(f"Monitoring {path}... Press Ctrl+C to stop.")
        observer.join()
    except KeyboardInterrupt:
        observer.stop()

    observer.join()