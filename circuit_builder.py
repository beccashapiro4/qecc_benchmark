from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, QISKitError

# Grabs quantum register k from qc
def getQReg(qc,k):   
    desired = list(qc.get_qregs().items())
    return desired[k][1]

def buildCirc(qc, cr, circuitArray, perm):
    qr = getQReg(qc,0)
    n = len(perm)
    
    firstPerm = perm.copy()
    for gate in circuitArray:
        #print(gate)
        addGate(qc, gate, perm)
    qc.barrier()

    registerPerm = {}
    for i in perm.keys():
        registerPerm[firstPerm[i]] = perm[i]

    return registerPerm



def addGate(qc, gate, perm):
    qr = getQReg(qc,0)
    gateSet = {
        "X": addX,
        "Z": addZ,
        "H": addH,
        "P": addS,
        "CNOT": addCX,
        "CZ": addCZ,
        "Permute": permute
    }
    
    # convert gate string to gate array
    gateSpec = gate.split()
    
    # get appropriate function to add desired generators
    addGens = gateSet.get(gateSpec[0])
    if addGens is None:
        print("Some nonsense was ignored")
    else:
        addGens(qc, gateSpec[1:],perm)
    
    
def addX(qc, gateNums,perm):
    qr = getQReg(qc,0)
    
    for num in gateNums:
        qub = perm[int(num)]
        qc.x(qr[qub])
        
def addZ(qc, gateNums,perm):
    qr = getQReg(qc,0)
    
    for num in gateNums:
        qub = perm[int(num)]
        qc.z(qr[qub])

def addH(qc, gateNums,perm):
    qr = getQReg(qc,0)
    
    for num in gateNums:
        qub = perm[int(num)]
        qc.h(qr[qub])
        
def addS(qc, gateNums,perm):
    qr = getQReg(qc,0)
    
    for num in gateNums:
        qub = perm[int(num)]
        qc.s(qr[qub])
        
def addCX(qc, gateNums,perm):
    qr = getQReg(qc,0)
    
    qub1 = perm[int(gateNums[0])]
    qub2 = perm[int(gateNums[1])]
    qc.cx(qr[qub1], qr[qub2])
    
def addCZ(qc, gateNums,perm):
    qr = getQReg(qc,0)
    
    qub1 = perm[int(gateNums[0])]
    qub2 = perm[int(gateNums[1])]
    qc.cz(qr[qub1], qr[qub2])

def permute(qc, gateOrder,perm):
    n = len(perm)
    permCopy = perm.copy()
    for i in range(n):
        perm[i+1] = permCopy[int(gateOrder[i])]
    print(perm)
    
    # this keeps track of the last permutation that occurred
    # so we can measure by it
    '''
    lastPerm = {}
    for i in range(n):
        lastPerm[n-i] = i
    lastPermCopy = lastPerm.copy()
    for i in range(n):
        lastPerm[i+1] = lastPermCopy[int(gateOrder[i])]
    print("Last Perm:" + str(lastPerm))
    return lastPerm
    '''
