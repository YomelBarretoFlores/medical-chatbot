import os
import subprocess
import sys

def main():
    print("Medical Chatbot Launcher")
    print("------------------------")
    
    print("1. Start Chatbot (requires existing index)")
    print("2. Re-ingest Data (recreates index from PDFs) & Start")
    
    choice = input("Enter your choice (1/2): ").strip()
    
    if choice == '2':
        print("\nStarting ingestion process... this may take a while.")
        try:
            
            subprocess.run([sys.executable, "store_index.py"], check=True)
            print("\nIngestion complete!")
        except subprocess.CalledProcessError as e:
            print(f"\nError during ingestion: {e}")
            return
        except KeyboardInterrupt:
            print("\nIngestion cancelled.")
            return

    print("\nStarting Flask Application...")
    try:
        
        subprocess.run([sys.executable, "app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nApp crashed: {e}")
    except KeyboardInterrupt:
        print("\nApp stopped.")

if __name__ == "__main__":
    main()
