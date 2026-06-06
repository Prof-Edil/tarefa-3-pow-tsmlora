import hashlib

def merkle_root(hashes):
    if len(hashes) == 1:
        return hashes[0]
    if len(hashes) % 2 == 0:
        newHashes = [hashlib.sha256(hashes[i]+hashes[i+1]).digest() for i in range(0, len(hashes), 2)]
        return merkle_root(newHashes)
    else:
        newHashes = [hashlib.sha256(hashes[i]+hashes[i+1]).digest() for i in range(0, len(hashes)-1, 2)]
        newHashes.append(hashlib.sha256(hashes[-1]+hashes[-1]).digest())
        return merkle_root(newHashes)

def find_txid(block, txid):
    txid_bytes = bytes.fromhex(txid)
    for i in range(len(block)):
        if block[i] == txid_bytes:
            return i
    return -1

def get_sibling(level, idx):
    if idx % 2 == 0:
        if idx + 1 < len(level):
            return level[idx + 1]
        return level[idx]
    return level[idx - 1]

specialTxid = '49ff8cccf1ca12179e9ae7a4760f550b5a18401b27e1e057604e27c3e10c08fb'
rawTxid = []
with open('data/ex02_txid_list.txt', 'r') as f:
    rawTxid = f.read().strip().split('\n')
rawTxid = [bytes.fromhex(s) for s in rawTxid]
specialTxidIdx = find_txid(rawTxid, specialTxid)
hashAll = merkle_root(rawTxid)
rightTxid = get_sibling(rawTxid, specialTxidIdx)
nextLevel = []
proof = []
level = rawTxid
idx = specialTxidIdx
while len(level) > 1:
    proof.append(get_sibling(level, idx))
    nextLevel = []
    for i in range(0, len(level), 2):
        left = level[i]
        if i + 1 < len(level):
            right = level[i + 1]
        else:
            right = left
        nextLevel.append(hashlib.sha256(left + right).digest())
    idx //= 2
    level = nextLevel
print(f"Merkle root: {hashAll.hex()}")
for p in proof:
    print(p.hex())
with open("solutions/exercise02.txt", "w") as f:
    f.write(hashAll.hex() + "\n")
    for p in proof:
        f.write(p.hex() + "\n")