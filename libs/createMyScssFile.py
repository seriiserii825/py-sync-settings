import os
import subprocess
def createMyScssFile():
    if not os.path.exists('src/scss/my.scss'):
        subprocess.run(["touch", "src/scss/my.scss"], check=True)
