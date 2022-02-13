

def upload_files(files, dir: str, name: str):
    for file in files:
        files[file].save(f"./{dir}/{name}")
        

