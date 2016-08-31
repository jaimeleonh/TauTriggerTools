from ROOT import *
import numpy as n

## FIXME: copy triggerNames structure for storing HLT info as well

# the hadd of all the output ntuples
fname = 'NTuple_Merge_10Ago_MaxIso.root'
pt = [26, 30, 34]
numberOfHLTTriggers = 6

#######################################################
fIn = TFile.Open(fname)
tIn = fIn.Get('Ntuplizer/TagAndProbe')
tTriggerNames = fIn.Get("Ntuplizer/triggerNames")
outname = fname.replace ('.root', '_forFit.root')
fOut = TFile (outname, 'recreate')
tOut = tIn.CloneTree(0)

briso   = [n.zeros(1, dtype=int) for x in range (0, len(pt))]
brnoiso = [n.zeros(1, dtype=int) for x in range (0, len(pt))]
hltPathTriggered_OS   = [n.zeros(1, dtype=int) for x in range (0, numberOfHLTTriggers)]

for i in range (0, len(pt)):
    name = ("hasL1_" + str(pt[i]))
    tOut.Branch(name, brnoiso[i], name+"/I")
    name += "_iso"
    tOut.Branch(name, briso[i], name+"/I")

for i in range (0, numberOfHLTTriggers):
    tTriggerNames.GetEntry(i)
    name = ("hasHLTPath_" + tTriggerNames.triggerNames.Data())
    tOut.Branch(name, hltPathTriggered_OS[i], name+"/I")

nentries = tIn.GetEntries()
for ev in range (0, nentries):
    tIn.GetEntry(ev)
    if (ev%10000 == 0) : print ev, "/", nentries

    for i in range (0, len(pt)):
        briso[i][0] = 0
        brnoiso[i][0] = 0

    for i in range (0, numberOfHLTTriggers):
        hltPathTriggered_OS[i][0] = 0

    L1iso = True if tIn.l1tIso == 1 else False
    L1pt = tIn.l1tPt
    if tIn.isOS == True:
        for i in range(0, len(pt)):
            # print L1pt, pt[i]
            #
                if L1pt > pt[i]:
                    brnoiso[i][0] = 1
                    # print "SUCCESS!! ", brnoiso[i]
                    if L1iso:
                        briso[i][0] = 1

        triggerBits = tIn.tauTriggerBits
        for bitIndex in range(0, numberOfHLTTriggers):
                if ((triggerBits >> bitIndex) & 1) == 1:
                    hltPathTriggered_OS[bitIndex][0] = 1

    tOut.Fill()

tOut.Write()
fOut.Close()
