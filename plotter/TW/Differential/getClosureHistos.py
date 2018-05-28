import ROOT as r
import varList as vl
import sys, os
from array import array
print "===== Plots for closure test comparisons procedure\n"

storagepath = "/nfs/fanae/user/vrbouza/Storage/TW/MiniTrees/"
pathToTree    = ""

def GetLastFolder(stpth):
    savefolders   = next(os.walk(stpth))[1]
    saveyears     = map(int, [i[6:]  for i in savefolders])
    savefolders   = [i for i in savefolders if int(i[6:]) == max(saveyears)]
    savemonths    = map(int, [i[3:5] for i in savefolders])
    savefolders   = [i for i in savefolders if int(i[3:5]) == max(savemonths)]
    savedays      = map(int, [i[:2]  for i in savefolders])
    savefolders   = [i for i in savefolders if int(i[:2]) == max(savedays)]
    return (stpth + savefolders[0] + "/")


if (len(sys.argv) > 1):
    varName     = sys.argv[1]
    print "> Chosen variable:", varName, "\n"
    if (len(sys.argv) > 2):
        if sys.argv[2] == 'last':
            pathToTree    = GetLastFolder(storagepath)
        else:
            pathToTree    = storagepath + sys.argv[2] + "/"
    else:
        pathToTree  = "../../../TW_temp/"
    print "> Minitrees will be read from:", pathToTree, "\n"
else:
    print "> Default choice of variable and minitrees\n"
    varName     = 'LeadingLepEta'
    pathToTree  = "../../../TW_temp/"


NameOfTree = "Mini1j1t";

r.gROOT.SetBatch(True)
r.gROOT.LoadMacro('../../Histo.C+')
r.gROOT.LoadMacro('../../Looper.C+')
r.gROOT.LoadMacro('../../Plot.C+')
r.gROOT.LoadMacro('../../PlotToPyC.C+')


binning     = array('f', vl.varList[varName]['genbinning'])
binningreco = array('f', vl.varList[varName]['recobinning'])
if not os.path.isdir('temp/{var}_'.format(var = varName)):
    os.system('mkdir -p temp/{var}_'.format(var = varName))
print "> Beginning to produce the histogram", "\n"

p = r.PlotToPyC(r.TString(vl.varList[varName]['var_gen']), r.TString('1/TWeight*TWeight_normal*(Tpassgen == 1)'), r.TString('All'), len(binning)-1, binning, r.TString('TGen' + varName), r.TString(''))
p.SetPath(pathToTree); p.SetTreeName(NameOfTree);
p.SetLimitFolder('temp/{var}_/'.format(var = varName));
p.SetPathSignal(pathToTree);
p.verbose = True
p.verbose = False

p.AddSample("UNF_TW",    "tW", r.itBkg, 2)
p.AddSample("UNF_TbarW", "tW", r.itBkg);

p.NoShowVarName = True;
p.SetOutputName("ClosureTest_" + varName);
p.SaveHistograms();
del p

p = r.PlotToPyC(r.TString(vl.varList[varName]['var']), r.TString('Tpassreco == 1'), r.TString('All'), len(binningreco)-1, binningreco, r.TString('T' + varName), r.TString(''))
p.SetPath(pathToTree); p.SetTreeName(NameOfTree);
p.SetLimitFolder('temp/{var}_/'.format(var = varName));
p.SetPathSignal(pathToTree);
p.verbose = True
p.verbose = False

p.AddSample("TW",    "tW", r.itBkg, 2)
p.AddSample("TbarW", "tW", r.itBkg);

p.NoShowVarName = True;
p.SetOutputName("ClosureTest_recobinning_" + varName);
p.SaveHistograms();
del p

print "> Done!", "\n"
