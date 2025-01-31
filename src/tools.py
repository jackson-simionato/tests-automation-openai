def load_file(fname):
    try:
        with open(fname, 'r') as f:
            return f.read()
    except IOError as e:
        print(f"Error loading file: {e}")
        return None

def save_file(fname, content):
    try:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)
    except IOError as e:
        print(f"Error saving file: {e}")