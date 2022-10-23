
def add_path(path):
    
    import sys
    if path not in sys.path:
        sys.path.insert(0, path)


add_path('./repository')