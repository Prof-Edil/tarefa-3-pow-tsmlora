import hashlib
import sys
import os

WORKER_ID = int(sys.argv[1])
STEP = int(sys.argv[2])

MERKLE_ROOT = "c0a692de10b69e2381a2856dcb0d0736dcd307bf25af7ce74831bf25793de626"
PREVIOUS_BLOCK = "00000000d1145790a8694403d4063f323d499e655c83426834d4ce2f8dd4a2ee"
TARGET = int("00000000ffff0000000000000000000000000000000000000000000000000000", 16)
version = (2).to_bytes(4, "big")
timestamp_start = 1230999306
timestamp_end = 1231716625
found = False

for ts in range(timestamp_start, timestamp_end + 1):
    timestamp = ts.to_bytes(4, "big")
    nonce = WORKER_ID
    while nonce < (1 << 64):
        nonce_bytes = nonce.to_bytes(8, "big")
        header = version + bytes.fromhex(PREVIOUS_BLOCK) + bytes.fromhex(MERKLE_ROOT) + timestamp + nonce_bytes
        h = hashlib.sha256(header).digest()
        if int.from_bytes(h, "big") <= TARGET:
            try:
                fd = os.open("solutions/exercise03.txt", os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                with os.fdopen(fd, "w") as f:
                    f.write(header.hex())
                print("FOUND")
                print("HASH:", h.hex())
            except FileExistsError:
                pass
            found = True
            break
        nonce += STEP
    if found:
        break