# setup_dvc.py
import os
import subprocess

# Check if DVC is already initialized
if not os.path.exists(".dvc"):
    subprocess.run(["dvc", "init", "-f"], check=True)

# Check if the dvc-storage branch exists
try:
    subprocess.run(["git", "rev-parse", "--verify", "dvc-storage"], check=True, capture_output=True)
except subprocess.CalledProcessError:
    # Create a new branch for DVC storage
    subprocess.run(["git", "checkout", "-b", "dvc-storage"], check=True)
    subprocess.run(["git", "commit", "--allow-empty", "-m", "Initialize dvc-storage branch"], check=True)
    subprocess.run(["git", "push", "origin", "dvc-storage"], check=True)
    subprocess.run(["git", "checkout", "main"], check=True)

# Check if the DVC remote exists
try:
    subprocess.run(["dvc", "remote", "list"], check=True, capture_output=True, text=True).stdout.index("storage")
except (subprocess.CalledProcessError, ValueError):
    # Configure DVC to use the new branch as a remote
    repo_url = f"https://github.com/{os.environ['GITHUB_REPOSITORY']}.git"
    subprocess.run(["dvc", "remote", "add", "-d", "storage", repo_url], check=True)
    subprocess.run(["dvc", "remote", "modify", "storage", "branch", "dvc-storage"], check=True)

print("DVC initialized and configured with a Git-based remote.")
