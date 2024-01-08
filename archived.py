def abc():
    file = get_most_recent_file()
    filename = tail(file)
    key = match(filename, "[a-zA-Z]+")

    system_command("""
        tar -xvf $file
    """, file)
    unzipped_file = get_most_recent_file()
    file_path = Path(unzipped_file)

        sudo cp $filename/$key /usr/local/bin/


