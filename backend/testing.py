import time, os

TEXT_FILE = "received_text.txt"

def read_text_from_file():
    """Reads the latest text from the file and processes it."""
    if not os.path.exists(TEXT_FILE):
        print("Waiting for input...")
        return None

    with open(TEXT_FILE, "r") as f:
        print("WORKS")
        text = f.read().strip()
        if text:
            print(f"Processing text: {text}")
            # Do something with the text (replace this with your logic)
            return text
        return None

if __name__ == "__main__":
    print("Listening for text updates...")
    while True:
        text = read_text_from_file()
        if text:
            print(f"Received Text: {text}")  # Process text here
            time.sleep(2)  # Wait before checking again

