import subprocess

WORKERS = 12
procs = []

for i in range(WORKERS):
    procs.append(subprocess.Popen(["python", "implementations/exercise03.py", str(i), str(WORKERS)]))

for p in procs:
    p.wait()