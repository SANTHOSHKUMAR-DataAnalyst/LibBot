import time
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from sql import update_database

# File watcher class
class ExcelFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Check if the modified file is the dataset file
        if event.src_path.endswith("Library_Books_Dataset.csv"):
            print("Dataset file modified. Updating database...")
            try:
                # Read the dataset file
                df = pd.read_csv("C:/Users/HP/Downloads/Library_Books_Dataset.csv")
                print("Dataset file read successfully.")
                
                # Ensure the dataset file has the correct columns
                required_columns = ["title", "author", "year", "rack", "shelf"]
                if all(column in df.columns for column in required_columns):
                    print("Updating database...")
                    update_database(df)
                    print("Database updated successfully.")
                else:
                    print("Dataset file does not contain the required columns.")
            except Exception as e:
                print(f"Error: {e}")

# Monitor the dataset file for changes
if __name__ == "__main__":
    path = "C:/Users/HP/Downloads"  # Directory containing the dataset file
    event_handler = ExcelFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    print(f"Monitoring directory: {path}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()