def isTxidPresent(block, txid):
    for i in range(len(block)):
        if block[i][0] == txid:
            return True, i
    return False, -1

def addParentsRecursive(parents):
    if parents == '':
        print("All parents added!")
        return 0
    parents = parents.split(';')
    w = 0
    for parent in parents:
        w = 0
        if parent != '':
            isPresent, idx = isTxidPresent(mempool, parent)
            if isPresent:
                tx = mempool[idx]
                newBlock.insert(0, [tx[0], int(tx[1]), int(tx[2]), tx[3]])
                w += int(tx[2])
    return w + addParentsRecursive(newBlock[0][3])

specialTxid = '4c50e3dad7f98bceb6441f96b23748dea84fbdb7cedd603441e6ea4a574d04a6'
mempool = ""
with open('data/mempool.csv', 'r') as f:
    mempool = f.read().strip()
mempool = [[e for e in line.split(',')] for line in mempool.split('\n')]

specialTx = mempool[isTxidPresent(mempool, specialTxid)[1]]
totalWeight = int(specialTx[2])
newBlock = [[specialTx[0], int(specialTx[1]), int(specialTx[2]), specialTx[3]]]
totalWeight += addParentsRecursive(newBlock[0][3])
for line in mempool:
    isOk = True
    weight = int(line[2])
    if ((weight + totalWeight) > 4000000):
        # isOk = False
        continue
    for parent in line[3].split(";"):     
        if parent == '':
            continue
        if not isTxidPresent(newBlock, parent)[0]:
            isOk = False
            break
    if isTxidPresent(newBlock, line[0])[0]:
        continue
        # isOk = False
    if isOk:    
        newBlock.append([line[0], int(line[1]), weight, line[3]])
        totalWeight += weight
sats = sum([x[1] for x in newBlock])
newBlockSize = len(newBlock)
isSpecialTxidPresent = isTxidPresent(newBlock, specialTxid)[0]
if newBlockSize > 0 and sats >= 50000 and totalWeight <= 4000000 and isSpecialTxidPresent:
    with open("solutions/exercise01.txt", 'w') as f:
        for line in newBlock:
            f.write(line[0]+'\n')
    print("Output written to solutions/exercise01.txt")
else:
    print("Didn't meet the criteria")
print(f"Total Weight: {totalWeight}")
print(f"NewBlock: {len(newBlock)}")
print(f"Sats: {sats}")
print(f"Does it has the special txid: {isSpecialTxidPresent}")