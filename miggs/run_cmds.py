import subprocess
import time


def run_cmd(cmd, dry_run=False):
    if dry_run:
        print(cmd)
        return
    
    print(f"Running command: {cmd}")
    
    # Start the process holding the command
    process = subprocess.Popen(cmd, shell=True)
    
    while process.poll() is None:
        time.sleep(1)
        
    process.communicate()
    
    if process.returncode != 0:
        raise Exception(f"Command failed with return code {process.returncode}")
    
        