

import subprocess

def git_commit_existing_files(commit_message):
    # Stage modified and deleted files, but not new files
    
    subprocess.run(['git', 'add', '-u'], check=True)

    # Commit the changes with the provided commit message
    subprocess.run(['git', 'commit', '-m', commit_message], check=True)

    print("Changes committed successfully.")

# Usage
git_commit_existing_files("Your commit message")

