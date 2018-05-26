import ROOT
from varList import *
import sys, os
from multiprocessing import Pool
print "===== BDT's histograms procedure with systs. profiling\n"

storagepath = "/nfs/fanae/user/vrbouza/Storage/TW/MiniTrees/"
pathToTree  = ""
NameOfTree  = "Mini1j1t";
systlist    = "JES,Btag,Mistag,PU,ElecEff,MuonEff,Trig"

if (len(sys.argv) > 1):
    nCores      = int(sys.argv[1])
    print ('> Parallelization will be done with ' + str(nCores) + ' cores')
else:
    print '> Sequential execution mode chosen'
    nCores      = 1

if (len(sys.argv) > 2):
    varName     = sys.argv[2]
    print "> Chosen variable:", varName, "\n"
    if (len(sys.argv) > 3):
        if sys.argv[2] == 'last':
            pathToTree    = GetLastFolder(storagepath)
        else:
            pathToTree    = storagepath + sys.argv[3] + "/"
    else:
        pathToTree  = "../../../TW_temp/"
    print "> Minitrees will be read from:", pathToTree, "\n"
else:
    print "> Default choice of variable and minitrees\n"
    varName     = 'LeadingLepEta'
    pathToTree  = "../../../TW_temp/"


ROOT.gROOT.SetBatch(True)
ROOT.gROOT.LoadMacro('../../Histo.C+')
ROOT.gROOT.LoadMacro('../../Looper.C+')
ROOT.gROOT.LoadMacro('../../Plot.C+')
ROOT.gROOT.LoadMacro('../../PlotToPy.C+')
ROOT.gROOT.LoadMacro('../../Datacard.C+')
ROOT.gROOT.LoadMacro('../../PDFunc.C+')

ROOT.gROOT.LoadMacro('./temp/{var}_/'.format(var = varName) + varName + '.C+')
print '> Succesfully loaded binning information from temp/' + varName + '.C', "\n"


def getCardsNominal(task):
    binDn, binUp, indx, asimov = task

    p = ROOT.PlotToPy(ROOT.TString('theBDt_bin%d( TBDT )'%indx), ROOT.TString('(TIsSS == 0 && TNJets == 1  && TNBtags == 1 && %s >= %4.2f  && %s < %4.2f )'%(varList[varName]['var'], binDn, varList[varName]['var'], binUp)), ROOT.TString('ElMu'), nBinsInBDT, ROOT.Double(0.5), ROOT.Double(nBinsInBDT + 0.5), ROOT.TString(varName + '_%d'%indx), ROOT.TString('BDT disc. (bin %s)'%(str(indx))))
    p.SetPath(pathToTree); p.SetTreeName(NameOfTree);
    p.SetLimitFolder('./temp/{var}_/'.format(var = varName));
    p.SetPathSignal(pathToTree);
    p.SetTitleY("Events")
    
    p.AddSample("TW",                           "tW_%d"%indx,           ROOT.itBkg, ROOT.TColor.GetColor("#ffcc33"), systlist)
    p.AddSample("TbarW",                        "tW_%d"%indx,           ROOT.itBkg, ROOT.TColor.GetColor("#ffcc33"), systlist);
    
    p.AddSample("TTbar_PowhegSemi",             "Non-W|Z_%d"%indx,      ROOT.itBkg, 413, systlist)
    p.AddSample("WJetsToLNu_MLM",               "Non-W|Z_%d"%indx,      ROOT.itBkg, 413, systlist)
    
    p.AddSample("WZ",                           "VV+t#bar{{t}}V_{ind}".format(ind = indx), ROOT.itBkg, 390, systlist);
    p.AddSample("WW",                           "VV+t#bar{{t}}V_{ind}".format(ind = indx), ROOT.itBkg, 390, systlist);
    p.AddSample("ZZ",                           "VV+t#bar{{t}}V_{ind}".format(ind = indx), ROOT.itBkg, 390, systlist);
    p.AddSample("TTWToLNu",                     "VV+t#bar{{t}}V_{ind}".format(ind = indx), ROOT.itBkg, 390, systlist);
    p.AddSample("TTWToQQ" ,                     "VV+t#bar{{t}}V_{ind}".format(ind = indx), ROOT.itBkg, 390, systlist);
    p.AddSample("TTZToQQ" ,                     "VV+t#bar{{t}}V_{ind}".format(ind = indx), ROOT.itBkg, 390, systlist);
    p.AddSample("TTZToLLNuNu",                  "VV+t#bar{{t}}V_{ind}".format(ind = indx), ROOT.itBkg, 390, systlist);

    p.AddSample("DYJetsToLL_M10to50_aMCatNLO",  "DY_%d"%indx,           ROOT.itBkg, 852, systlist)
    p.AddSample("DYJetsToLL_M50_aMCatNLO",      "DY_%d"%indx,           ROOT.itBkg, 852, systlist);
    
    p.AddSample("TTbar_Powheg",                 "t#bar{{t}}_{ind}".format(ind = indx),     ROOT.itBkg, 633, systlist)
    
    p.AddSample("TW",                           "tW_%d"%indx,           ROOT.itSys, 1, "JERUp");
    p.AddSample("TbarW",                        "tW_%d"%indx,           ROOT.itSys, 1, "JERUp");
    p.AddSample("TTbar_Powheg",                 "t#bar{{t}}_{ind}".format(ind = indx),     ROOT.itSys, 1, "JERUp");
    p.AddSymmetricHisto("t#bar{{t}}_{ind}".format(ind = indx),  "JERUp");
    p.AddSymmetricHisto("tW_%d"%indx,  "JERUp");

    #p.AddSystematic(systlist)

    if not asimov:
        p.AddSample("MuonEG",                       "Data",             ROOT.itData);
        p.AddSample("SingleMuon",                   "Data",             ROOT.itData);
        p.AddSample("SingleElec",                   "Data",             ROOT.itData);
    else:
        hData=ROOT.Histo(p.GetHisto('tW_%d'%indx).Clone("Data"))
        for proc in ['t#bar{{t}}_{ind}'.format(ind = indx),'VV+t#bar{{t}}V_{ind}'.format(ind = indx), "DY_%d"%indx, "Non-W|Z_%d"%indx]:
            hData.Add( p.GetHisto(proc) )
        hData.SetProcess("Data")
        hData.SetTag("Data")
        hData.SetType(ROOT.itData)
        hData.SetColor(ROOT.kBlack)
        p.AddToHistos(hData)
    
    p.doUncInLegend = True;
    p.SetRatioMin( 0.6 );
    p.SetRatioMax( 1.4 );
    
    p.SetCMSlabel("CMS");
    p.SetCMSmodeLabel("Preliminary");
    p.SetLegendPosition(0.7, 0.45, 0.93, 0.92);
    p.SetPlotFolder("results/Cardplots/");
    p.doYieldsInLeg = False;
    p.doSetLogy     = False;
    #p.doData        = False;
    p.doSignal      = False;
    p.SetTitleY(ROOT.TString(varList[varName]['yaxis']))
    
    
    #for i in range(1, nBinsInBDT + 1):
        #if (p.GetHisto("DY_%d"%indx).GetBinContent(i) < 0):
            #p.GetHisto("DY_%d"%indx).SetBinContent(i, 1e-4)
        #for sys in (systlist + ',JER').split(','):
            #if (p.GetHisto("DY_%d"%indx, sys + 'Up').GetBinContent(i) < 0):
                #p.GetHisto("DY_%d"%indx, sys + 'Up').SetBinContent(i, 1e-4)
            #if (p.GetHisto("DY_%d"%indx, sys + 'Down').GetBinContent(i) < 0):
                #p.GetHisto("DY_%d"%indx, sys + 'Down').SetBinContent(i, 1e-4)
    
    #p.GetHisto("DY_%d"%indx).ReCalcValues()
    #for sys in (systlist + ',JER').split(','):
        #p.GetHisto("DY_%d"%indx, sys + 'Up').ReCalcValues()
        #p.GetHisto("DY_%d"%indx, sys + 'Down').ReCalcValues()
        #p.GetHisto("DY_%d"%indx).ReCalcValues()
    
    p.NoShowVarName = True;
    p.SetOutputName("forCards_" + varName + '_%d'%indx);
    p.DrawStack();
    p.SetOutputName("forCards_" + varName + '_%d'%indx);
    p.SaveHistograms();
    del p
    
    card = ROOT.Datacard("tW_%d"%indx, "t#bar{{t}}_{idx},DY_{idx},VV+t#bar{{t}}V_{idx},Non-W|Z_{idx}".format(idx=indx), systlist + ', JER', "ElMu_%d"%indx)
    card.SetRootFileName('./temp/{var}_/forCards_'.format(var = varName) + varName + '_%d'%indx)
    card.GetParamsFormFile()
    card.SetNormUnc("Non-W|Z_%d"%indx, 1.50)
    card.SetNormUnc("DY_%d"%indx   , 1.50)
    card.SetNormUnc('VV+t#bar{{t}}V_{ind}'.format(ind = indx), 1.50);
    card.SetNormUnc('t#bar{{t}}_{ind}'.format(ind = indx), 1.06);
    card.SetLumiUnc(1.025)
    card.PrintDatacard("temp/{var}_/datacard_".format(var = varName) + varName + '_%d'%indx);
    del card

    # All this crap so i dont have to tamper with the DataCard.C
    out = ''
    datacarta = open('temp/{var}_/datacard_'.format(var = varName) + varName + '_%d.txt'%indx,'r')
    for lin in datacarta.readlines():
        nuLine = lin
        if 'process' in nuLine: nuLine = nuLine.replace('-1', '-%d'%indx)
        if 'rate' in nuLine and '-' in nuLine: nuLine = nuLine.replace('-', '0')
        out = out + nuLine
    datacarta.close()
    outCarta = open('temp/{var}_/datacard_'.format(var = varName) + varName + '_%d.txt'%indx,'w')
    outCarta.write(out)


def getCardsSyst(task):
    binDn, binUp, indx, asimov, syst = task
    if not os.path.isdir('temp/{var}_{sys}'.format(var = varName, sys = syst)):
        os.system('mkdir -p temp/{var}_{sys}'.format(var = varName, sys = syst))
    
    p = ROOT.PlotToPy(ROOT.TString('theBDt_bin%d( TBDT )'%indx), ROOT.TString('(TIsSS == 0 && TNJets == 1  && TNBtags == 1 && %s >= %4.2f  && %s < %4.2f )'%(varList[varName]['var'], binDn, varList[varName]['var'], binUp)), ROOT.TString('ElMu'), nBinsInBDT, ROOT.Double(0.5), ROOT.Double(nBinsInBDT+0.5), ROOT.TString(varName + '_%d'%indx), ROOT.TString(''))
    p.SetPath(pathToTree); p.SetTreeName(NameOfTree);
    p.SetLimitFolder("temp/{var}_{sys}/".format(var = varName, sys = syst));
    p.SetPathSignal(pathToTree);
    p.SetTitleY("Events")
    
    p.AddSample(systMap[syst]["TW"],           "tW_%d"%indx,           ROOT.itBkg, ROOT.TColor.GetColor("#ffcc33"), systlist)
    p.AddSample(systMap[syst]["TbarW"],        "tW_%d"%indx,           ROOT.itBkg, ROOT.TColor.GetColor("#ffcc33"), systlist)
    
    p.AddSample("TTbar_PowhegSemi",            "Non-W|Z_%d"%indx,      ROOT.itBkg, 413, systlist)
    p.AddSample("WJetsToLNu_MLM",              "Non-W|Z_%d"%indx,      ROOT.itBkg, 413, systlist)
    
    p.AddSample("WZ",                          'VV+t#bar{{t}}V_{ind}'.format(ind = indx), ROOT.itBkg, 390, systlist);
    p.AddSample("WW",                          'VV+t#bar{{t}}V_{ind}'.format(ind = indx), ROOT.itBkg, 390, systlist);
    p.AddSample("ZZ",                          'VV+t#bar{{t}}V_{ind}'.format(ind = indx), ROOT.itBkg, 390, systlist);
    p.AddSample("TTWToLNu",                    'VV+t#bar{{t}}V_{ind}'.format(ind = indx), ROOT.itBkg, 390, systlist);
    p.AddSample("TTWToQQ" ,                    'VV+t#bar{{t}}V_{ind}'.format(ind = indx), ROOT.itBkg, 390, systlist);
    p.AddSample("TTZToQQ" ,                    'VV+t#bar{{t}}V_{ind}'.format(ind = indx), ROOT.itBkg, 390, systlist);
    p.AddSample("TTZToLLNuNu",                 'VV+t#bar{{t}}V_{ind}'.format(ind = indx), ROOT.itBkg, 390, systlist);

    p.AddSample("DYJetsToLL_M10to50_aMCatNLO", "DY_%d"%indx,           ROOT.itBkg, 852, systlist)
    p.AddSample("DYJetsToLL_M50_aMCatNLO",     "DY_%d"%indx,           ROOT.itBkg, 852, systlist);
    
    if 'UEUp' in syst:
        specialweight = nUEUp_ttbar/sigma_ttbar/(nUEUp_ttbar/sigma_ttbar + nUEUp_dilep/sigma_dilep)
        p.SetWeight('TWeight*' + str(specialweight))
        p.AddSample(systMap[syst]["TTbar_Powheg"], 't#bar{{t}}_{ind}'.format(ind = indx), ROOT.itBkg, 633, systlist)
        p.AddSample(systMap[syst]["TTbar_Powheg"], 't#bar{{t}}_{ind}'.format(ind = indx), ROOT.itSys, 1, "JERUp");
        
        specialweight = nUEUp_dilep/sigma_dilep/(nUEUp_ttbar/sigma_ttbar + nUEUp_dilep/sigma_dilep)
        p.SetWeight('TWeight*' + str(specialweight))
        p.AddSample('TTbar2L_Powheg_ueUp',                 't#bar{{t}}_{ind}'.format(ind = indx), ROOT.itBkg, 633, systlist)
        p.AddSample('TTbar2L_Powheg_ueUp',                 't#bar{{t}}_{ind}'.format(ind = indx), ROOT.itSys, 1, "JERUp")
        p.AddSymmetricHisto('t#bar{{t}}_{ind}'.format(ind = indx),  "JERUp");
        p.SetWeight('TWeight')
    elif 'UEDown' in syst:
        specialweight = nUEDown_ttbar/sigma_ttbar/(nUEDown_ttbar/sigma_ttbar + nUEDown_dilep/sigma_dilep)
        p.SetWeight('TWeight*' + str(specialweight))
        p.AddSample(systMap[syst]["TTbar_Powheg"], 't#bar{{t}}_{ind}'.format(ind = indx), ROOT.itBkg, 633, systlist)
        p.AddSample(systMap[syst]["TTbar_Powheg"], 't#bar{{t}}_{ind}'.format(ind = indx), ROOT.itSys, 1, "JERUp")
        
        specialweight = nUEDown_dilep/sigma_dilep/(nUEDown_ttbar/sigma_ttbar + nUEDown_dilep/sigma_dilep)
        p.SetWeight('TWeight*' + str(specialweight))
        p.AddSample('TTbar2L_Powheg_ueDown',               't#bar{{t}}_{ind}'.format(ind = indx), ROOT.itBkg, 633, systlist)
        p.AddSample('TTbar2L_Powheg_ueDown',               't#bar{{t}}_{ind}'.format(ind = indx), ROOT.itSys, 1, "JERUp")
        p.AddSymmetricHisto('t#bar{{t}}_{ind}'.format(ind = indx),  "JERUp");
        p.SetWeight('TWeight')
    elif 'hDampUp' in syst:
        specialweight = nhDampUp_ttbar/sigma_ttbar/(nhDampUp_ttbar/sigma_ttbar + nhDampUp_dilep/sigma_dilep)
        p.SetWeight('TWeight*' + str(specialweight))
        p.AddSample(systMap[syst]["TTbar_Powheg"], 't#bar{{t}}_{ind}'.format(ind = indx), ROOT.itBkg, 633, systlist)
        p.AddSample(systMap[syst]["TTbar_Powheg"], 't#bar{{t}}_{ind}'.format(ind = indx), ROOT.itSys, 1, "JERUp")
        
        specialweight = nhDampUp_dilep/sigma_dilep/(nhDampUp_ttbar/sigma_ttbar + nhDampUp_dilep/sigma_dilep)
        p.SetWeight('TWeight*' + str(specialweight))
        p.AddSample('TTbar2L_Powheg_hdampUp',              't#bar{{t}}_{ind}'.format(ind = indx), ROOT.itBkg, 633, systlist)
        p.AddSample('TTbar2L_Powheg_hdampUp',              't#bar{{t}}_{ind}'.format(ind = indx), ROOT.itSys, 1, "JERUp")
        p.AddSymmetricHisto('t#bar{{t}}_{ind}'.format(ind = indx),  "JERUp");
        p.SetWeight('TWeight')
    elif 'hDampDown' in syst:
        specialweight = nhDampDown_ttbar/sigma_ttbar/(nhDampDown_ttbar/sigma_ttbar + nhDampDown_dilep/sigma_dilep)
        p.SetWeight('TWeight*' + str(specialweight))
        p.AddSample(systMap[syst]["TTbar_Powheg"], 't#bar{{t}}_{ind}'.format(ind = indx), ROOT.itBkg, 633, systlist)
        p.AddSample(systMap[syst]["TTbar_Powheg"], 't#bar{{t}}_{ind}'.format(ind = indx), ROOT.itSys, 1, "JERUp")
        
        specialweight = nhDampDown_dilep/sigma_dilep/(nhDampDown_ttbar/sigma_ttbar + nhDampDown_dilep/sigma_dilep)
        p.SetWeight('TWeight*' + str(specialweight))
        p.AddSample('TTbar2L_Powheg_hdampDown',            't#bar{{t}}_{ind}'.format(ind = indx), ROOT.itBkg, 633, systlist)
        p.AddSample('TTbar2L_Powheg_hdampDown',            't#bar{{t}}_{ind}'.format(ind = indx), ROOT.itSys, 1, "JERUp")
        p.AddSymmetricHisto('t#bar{{t}}_{ind}'.format(ind = indx),  "JERUp");
        p.SetWeight('TWeight')
    else:
        p.AddSample(systMap[syst]["TTbar_Powheg"], 't#bar{{t}}_{ind}'.format(ind = indx), ROOT.itBkg, 633, systlist)
        p.AddSample(systMap[syst]["TTbar_Powheg"], 't#bar{{t}}_{ind}'.format(ind = indx), ROOT.itSys, 1, "JERUp")
        p.AddSymmetricHisto('t#bar{{t}}_{ind}'.format(ind = indx),  "JERUp");


    p.AddSample(systMap[syst]["TW"],           "tW_%d"%indx,    ROOT.itSys, 1, "JERUp");
    p.AddSample(systMap[syst]["TbarW"],        "tW_%d"%indx,    ROOT.itSys, 1, "JERUp");
    p.AddSymmetricHisto("tW_%d"%indx,  "JERUp");
    
    #p.AddSystematic(systlist)

    if not asimov:
        p.AddSample("MuonEG",                       "Data",  ROOT.itData);
        p.AddSample("SingleMuon",                   "Data",  ROOT.itData);
        p.AddSample("SingleElec",                   "Data",  ROOT.itData);
    else: 
        # get asimov from the nominal one"
        tfile = ROOT.TFile.Open("temp/{var}_/forCards_".format(var = varName) + varName + '_%d.root'%indx)
        if not tfile:
            raise RuntimeError('Nominal card rootfile for variable {var} has not been found while considering syst. {sys}'.format(var = varName, sys = syst))
        hData = ROOT.Histo( tfile.Get('data_obs') )
        hData.SetProcess("Data")
        hData.SetTag("Data")
        hData.SetType(ROOT.itData)
        hData.SetColor(ROOT.kBlack)
        p.AddToHistos(hData)

    p.doUncInLegend = True;
    p.SetRatioMin( 0.6 );
    p.SetRatioMax( 1.4 );
    
    p.SetCMSlabel("CMS");
    p.SetCMSmodeLabel("Preliminary");
    p.SetLegendPosition(0.7, 0.45, 0.93, 0.92);
    p.SetPlotFolder("results/Cardplots/");
    p.doYieldsInLeg = False;
    p.doSetLogy     = False;
    #p.doData        = False;
    p.doSignal      = False;
    
    #for i in range(1, nBinsInBDT + 1):
        #if (p.GetHisto("DY_%d"%indx).GetBinContent(i) < 0):
            #p.GetHisto("DY_%d"%indx).SetBinContent(i, 1e-4)
        #for sys in (systlist + ',JER').split(','):
            #if (p.GetHisto("DY_%d"%indx, sys + 'Up').GetBinContent(i) < 0):
                #p.GetHisto("DY_%d"%indx, sys + 'Up').SetBinContent(i, 1e-4)
            #if (p.GetHisto("DY_%d"%indx, sys + 'Down').GetBinContent(i) < 0):
                #p.GetHisto("DY_%d"%indx, sys + 'Down').SetBinContent(i, 1e-4)
    
    #p.GetHisto("DY_%d"%indx).ReCalcValues()
    #for sys in (systlist + ',JER').split(','):
        #p.GetHisto("DY_%d"%indx, sys + 'Up').ReCalcValues()
        #p.GetHisto("DY_%d"%indx, sys + 'Down').ReCalcValues()
    
    p.NoShowVarName = True;
    p.SetOutputName("forCards_" + varName + '_' + syst + '_%d'%indx);
    p.DrawStack();
    p.SetOutputName("forCards_" + varName + '_' + syst + '_%d'%indx);
    p.SaveHistograms();
    del p
    
    card = ROOT.Datacard('tW_%d'%indx, 't#bar{{t}}_{idx},DY_{idx},VV+t#bar{{t}}V_{idx},Non-W|Z_{idx}'.format(idx=indx) , systlist + ', JER', "ElMu_%d"%indx)
    card.SetRootFileName("temp/{var}_{sys}/forCards_".format(var = varName, sys = syst) + varName  + '_' + syst  + '_%d'%indx)
    card.GetParamsFormFile()
    card.SetNormUnc("Non-W|Z_%d"%indx, 1.50)
    card.SetNormUnc("DY_%d"%indx   , 1.50)
    card.SetNormUnc('VV+t#bar{{t}}V_{ind}'.format(ind = indx), 1.50);
    card.SetNormUnc('t#bar{{t}}_{ind}'.format(ind = indx), 1.06);
    card.SetLumiUnc(1.025)
    card.PrintDatacard("temp/{var}_{sys}/datacard_".format(var = varName, sys = syst) + varName + '_' + syst + '_%d'%indx);
    del card
    
    # All this crap so i dont have to tamper with the DataCard.C
    out = ''
    datacarta = open('temp/{var}_{sys}/datacard_'.format(var = varName, sys = syst) + varName + '_' + syst +  '_%d.txt'%indx,'r')
    for lin in datacarta.readlines():
        nuLine = lin
        if 'process' in nuLine: nuLine = nuLine.replace('-1', '-%d'%indx)
        if 'rate' in nuLine and '-' in nuLine: nuLine = nuLine.replace('-', '0')
        out = out + nuLine
    datacarta.close()
    outCarta = open('temp/{var}_{sys}/datacard_'.format(var = varName, sys = syst) + varName + '_' + syst + '_%d.txt'%indx,'w')
    outCarta.write(out)


def getCardsPdf(task):
    binDn, binUp, indx, asimov, syst = task
    if not os.path.isdir('temp/{var}_{sys}'.format(var = varName, sys = syst)):
        os.system('mkdir -p temp/{var}_{sys}'.format(var = varName, sys = syst))

    p = ROOT.PlotToPy(ROOT.TString('theBDt_bin%d( TBDT )'%indx), ROOT.TString('(TIsSS == 0 && TNJets == 1  && TNBtags == 1 && %s >= %4.2f  && %s < %4.2f )'%(varList[varName]['var'], binDn, varList[varName]['var'], binUp)), ROOT.TString('ElMu'), nBinsInBDT, ROOT.Double(0.5), ROOT.Double(nBinsInBDT+0.5), ROOT.TString(varName + '_%d'%indx), ROOT.TString(''))
    p.SetPath(pathToTree); p.SetTreeName(NameOfTree);
    p.SetLimitFolder("temp/{var}_{sys}/".format(var = varName, sys = syst));
    p.SetPathSignal(pathToTree);
    p.SetTitleY("Events")
    
    p.AddSample("TW",                          "tW_%d"%indx,           ROOT.itBkg, ROOT.TColor.GetColor("#ffcc33"), systlist)
    p.AddSample("TbarW",                       "tW_%d"%indx,           ROOT.itBkg, ROOT.TColor.GetColor("#ffcc33"), systlist);
    
    p.AddSample("TTbar_PowhegSemi",            "Non-W|Z_%d"%indx,      ROOT.itBkg, 413, systlist)
    p.AddSample("WJetsToLNu_MLM",              "Non-W|Z_%d"%indx,      ROOT.itBkg, 413, systlist)
    
    p.AddSample("WZ",                          'VV+t#bar{{t}}V_{ind}'.format(ind = indx), ROOT.itBkg, 390, systlist);
    p.AddSample("WW",                          'VV+t#bar{{t}}V_{ind}'.format(ind = indx), ROOT.itBkg, 390, systlist);
    p.AddSample("ZZ",                          'VV+t#bar{{t}}V_{ind}'.format(ind = indx), ROOT.itBkg, 390, systlist);
    p.AddSample("TTWToLNu",                    'VV+t#bar{{t}}V_{ind}'.format(ind = indx), ROOT.itBkg, 390, systlist);
    p.AddSample("TTWToQQ" ,                    'VV+t#bar{{t}}V_{ind}'.format(ind = indx), ROOT.itBkg, 390, systlist);
    p.AddSample("TTZToQQ" ,                    'VV+t#bar{{t}}V_{ind}'.format(ind = indx), ROOT.itBkg, 390, systlist);
    p.AddSample("TTZToLLNuNu",                 'VV+t#bar{{t}}V_{ind}'.format(ind = indx), ROOT.itBkg, 390, systlist);

    p.AddSample("DYJetsToLL_M10to50_aMCatNLO", "DY_%d"%indx,           ROOT.itBkg, 852, systlist)
    p.AddSample("DYJetsToLL_M50_aMCatNLO",     "DY_%d"%indx,           ROOT.itBkg, 852, systlist);

    p.AddSample("TW",                          "tW_%d"%indx,           ROOT.itSys, 1, "JERUp");
    p.AddSample("TbarW",                       "tW_%d"%indx,           ROOT.itSys, 1, "JERUp");
    p.AddSymmetricHisto("tW_%d"%indx,  "JERUp");

    #p.AddSystematic(systlist)

    pdf = ROOT.PDFToPy(pathToTree, "TTbar_Powheg", NameOfTree, ROOT.TString('(TIsSS == 0 && TNJets == 1  && TNBtags == 1 && %s >= %4.2f  && %s < %4.2f )'%(varList[varName]['var'], binDn, varList[varName]['var'], binUp)), ROOT.TString('ElMu'), ROOT.TString('theBDt_bin%d( TBDT )'%indx), nBinsInBDT,ROOT.Double(0.5), ROOT.Double(nBinsInBDT+0.5))

    if 'pdfUp' == syst:
        histo = pdf.GetSystHisto("up","pdf").CloneHisto()
    elif 'pdfDown' == syst:
        histo = pdf.GetSystHisto("Down","pdf").CloneHisto()
    elif 'ttbarMEUp' == syst:
        histo = pdf.GetSystHisto("up","ME").CloneHisto()
    elif 'ttbarMEDown' == syst:
        histo = pdf.GetSystHisto("Down","ME").CloneHisto()
    else:
        raise RuntimeError("Systematic %s is not of 'pdf' type"%syst)

    p.PrepareHisto(histo, 'TTbar_Powheg', 't#bar{{t}}_{ind}'.format(ind = indx), ROOT.itBkg,633)

    # now get systematic variations from nominal
    for s in (systlist + ',JER').split(','):
        tfile = ROOT.TFile.Open("temp/{var}_/forCards_".format(var = varName) + varName + '_%d.root'%indx)
        if not tfile: 
            raise RuntimeError('Nominal card rootfile for variable {var} has not been found while considering syst. {sys}'.format(var = varName, sys = syst))
        nom   = tfile.Get('t#bar{{t}}_{ind}'.format(ind = indx))
        nomUp = tfile.Get('t#bar{{t}}_{ind}_{sys}Up'.format(ind = indx, sys = s))
        nomDn = tfile.Get('t#bar{{t}}_{ind}_{sys}Down'.format(ind = indx, sys = s))

        # remove stats just in case
        for i in range(nom.GetNbinsX()):
            nom  .SetBinError(i+1,0.)
            nomUp.SetBinError(i+1,0.)
            nomDn.SetBinError(i+1,0.)

        nomUp.Divide(nom)
        nomDn.Divide(nom)

        histoUp = histo.CloneHisto()
        histoDn = histo.CloneHisto()

        histoUp.Multiply(nomUp)
        histoDn.Multiply(nomDn)

        p.PrepareHisto( histoUp, "TTbar_Powheg", 't#bar{{t}}_{ind}'.format(ind = indx), ROOT.itSys, 0, s+"Up")
        p.PrepareHisto( histoDn, "TTbar_Powheg", 't#bar{{t}}_{ind}'.format(ind = indx), ROOT.itSys, 0, s+"Down")

        p.AddToSystematicLabels(s)

    if not asimov:
        p.AddSample("MuonEG",                       "Data",  ROOT.itData);
        p.AddSample("SingleMuon",                   "Data",  ROOT.itData);
        p.AddSample("SingleElec",                   "Data",  ROOT.itData);
    else: 
        # get asimov from the nominal one
        tfile = ROOT.TFile.Open("temp/{var}_/forCards_".format(var = varName) + varName + '_%d.root'%indx)
        hData = ROOT.Histo( tfile.Get('data_obs') ) 
        hData.SetProcess("Data")
        hData.SetTag("Data")
        hData.SetType(ROOT.itData)
        hData.SetColor(ROOT.kBlack)
        p.AddToHistos(hData)

    p.doUncInLegend = True;
    p.SetRatioMin( 0.6 );
    p.SetRatioMax( 1.4 );
    
    p.SetCMSlabel("CMS");
    p.SetCMSmodeLabel("Preliminary");
    p.SetLegendPosition(0.7, 0.45, 0.93, 0.92);
    p.SetPlotFolder("results/Cardplots/");
    p.doYieldsInLeg = False;
    p.doSetLogy     = False;
    #p.doData        = False;
    p.doSignal      = False;
    
    #for i in range(1, nBinsInBDT + 1):
        #if (p.GetHisto("DY_%d"%indx).GetBinContent(i) < 0):
            #p.GetHisto("DY_%d"%indx).SetBinContent(i, 1e-4)
        #for sys in (systlist + ',JER').split(','):
            #if (p.GetHisto("DY_%d"%indx, sys + 'Up').GetBinContent(i) < 0):
                #p.GetHisto("DY_%d"%indx, sys + 'Up').SetBinContent(i, 1e-4)
            #if (p.GetHisto("DY_%d"%indx, sys + 'Down').GetBinContent(i) < 0):
                #p.GetHisto("DY_%d"%indx, sys + 'Down').SetBinContent(i, 1e-4)
    
    #p.GetHisto("DY_%d"%indx).ReCalcValues()
    #for sys in (systlist + ',JER').split(','):
        #p.GetHisto("DY_%d"%indx, sys + 'Up').ReCalcValues()
        #p.GetHisto("DY_%d"%indx, sys + 'Down').ReCalcValues()
    
    p.NoShowVarName = True;
    p.SetOutputName("forCards_" + varName + '_' + syst + '_%d'%indx);
    p.DrawStack();
    p.SetOutputName("forCards_" + varName + '_' + syst + '_%d'%indx);
    p.SaveHistograms();
    del p

    card = ROOT.Datacard('tW_%d'%indx, 't#bar{{t}}_{idx},DY_{idx},VV+t#bar{{t}}V_{idx},Non-W|Z_{idx}'.format(idx=indx) , systlist + ', JER', "ElMu_%d"%indx)
    card.SetRootFileName('temp/{var}_{sys}/forCards_'.format(var = varName, sys = syst) + varName  + '_' + syst  + '_%d'%indx)
    card.GetParamsFormFile()
    card.SetNormUnc("Non-W|Z_%d"%indx   , 1.50)
    card.SetNormUnc("DY_%d"%indx      , 1.50)
    card.SetNormUnc('VV+t#bar{{t}}V_{ind}'.format(ind = indx), 1.50);
    card.SetNormUnc('t#bar{{t}}_{ind}'.format(ind = indx)    , 1.06);
    card.SetLumiUnc(1.025)
    card.PrintDatacard("temp/{var}_{sys}/datacard_".format(var = varName, sys = syst) + varName + '_' + syst + '_%d'%indx);
    del card

    # All this crap so i dont have to tamper with the DataCard.C
    out = ''
    datacarta = open('temp/{var}_{sys}/datacard_'.format(var = varName, sys = syst) + varName + '_' + syst +  '_%d.txt'%indx,'r')
    for lin in datacarta.readlines():
        nuLine = lin
        if 'process' in nuLine: nuLine = nuLine.replace('-1', '-%d'%indx)
        out = out + nuLine
    datacarta.close()
    outCarta = open('temp/{var}_{sys}/datacard_'.format(var = varName, sys = syst) + varName + '_' + syst + '_%d.txt'%indx,'w')
    outCarta.write(out)


if __name__ == '__main__':
    indx    = 0
    binning = varList[varName]['recobinning']
    print "> Beginning to produce histograms", "\n"
    tasks   = []
    asimov  = False
    print '> Creating nominal rootfiles with histograms and datacards'
    for binDn,binUp in zip(binning, binning[1:]):
        indx = indx+1
        tasks.append( (binDn, binUp, indx, asimov) )

    pool    = Pool(nCores)
    pool.map(getCardsNominal, tasks)
    pool.close()
    pool.join()
    del pool
    
    print '> Creating rootfiles with histograms and datacards for all systematics'
    tasksSyst = []
    indx    = 0
    for binDn,binUp in zip(binning, binning[1:]):
        indx = indx+1
        for syst in systMap:
            tasksSyst.append( (binDn, binUp, indx, asimov, syst) )
    
    pool    = Pool(nCores)
    pool.map(getCardsSyst, tasksSyst)
    pool.close()
    pool.join()
    
    tasksPdf = []
    indx = 0
    for binDn,binUp in zip(binning, binning[1:]):
        indx = indx+1
        tasksPdf.append( (binDn, binUp, indx, asimov, 'pdfUp') )
        tasksPdf.append( (binDn, binUp, indx, asimov, 'ttbarMEUp') )
        tasksPdf.append( (binDn, binUp, indx, asimov, 'pdfDown') )
        tasksPdf.append( (binDn, binUp, indx, asimov, 'ttbarMEDown') )

    pool    = Pool(nCores)
    pool.map(getCardsPdf, tasksPdf)
    pool.close()
    pool.join()


    print "> Done!", "\n"
