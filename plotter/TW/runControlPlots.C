#define DEBUGFLAG 
R__LOAD_LIBRARY(Histo.C+)
R__LOAD_LIBRARY(Looper.C+)
R__LOAD_LIBRARY(Plot.C+)
R__LOAD_LIBRARY(TW/AdditionalStuff.C+)
#include "Histo.h"
#include "Looper.h"
#include "Plot.h"
#include "TW/AdditionalStuff.C"

void DrawPlot(TString var, TString cut, TString chan, Int_t nbins, Float_t bin0, Float_t binN, TString Xtitle, TString varname="",bool setLegendLeft=false );
TString pathToTree = "/pool/cienciasrw/userstorage/sscruz/TW/jul25/";
TString NameOfTree = "Mini";


void runControlPlots(){

  DrawPlot("TLeadingLepPt ", "(TIsSS == 0)", "ElMu", 36, 20., 200., "Leading lepton p_{T} (GeV)","");
  DrawPlot("TMath::Abs(TLeadingLepEta )", "(TIsSS == 0)", "ElMu", 25, 0., 2.5, "Leading lepton |#eta|","TLeadingLepEta");
  DrawPlot("TSubLeadingLepPt ", "(TIsSS == 0)", "ElMu", 36, 20., 200., "Sub-leading lepton p_{T} (GeV)","");
  DrawPlot("TMath::Abs(TSubLeadingLepEta )", "(TIsSS == 0)", "ElMu", 25, 0., 2.5, "Sub-leading lepton |#eta|","TSubLeadingLepEta");
  DrawPlot("TMll ", "(TIsSS == 0)", "ElMu", 25, 0., 300, "M_{l^{+}l^{-}} (GeV)","");
  DrawPlot("TDilepPt ", "(TIsSS == 0)", "ElMu", 25, 0., 300, "Dilepton p_{T} (GeV)","");
  return; 

  
}

void DrawPlot(TString var, TString cut, TString chan, Int_t nbins, Float_t bin0, Float_t binN, TString Xtitle, TString varname="", bool setLegendLeft = false){
  Plot* p = new Plot(var, cut, chan, nbins, bin0, binN, "Title", Xtitle);
  p->SetPath(pathToTree); p->SetTreeName(NameOfTree);
  p->SetPathSignal(pathToTree + "");
  p->verbose = false;
  if (varname != "") p->SetVarName(varname);


  p->AddSample("TTWToLNu", "Other", itBkg, kOrange-3);
  p->AddSample("TTWToQQ", "Other", itBkg);
  p->AddSample("TTZToQQ", "Other", itBkg);
  p->AddSample("TTZToLLNuNu", "Other", itBkg);
  p->AddSample("WZ", "Other", itBkg);
  p->AddSample("WW", "Other", itBkg);
  p->AddSample("ZZ", "Other", itBkg);


  p->AddSample("DYJetsToLL_M10to50_aMCatNLO", " Z/#gamma* #rightarrow e^{#pm}#mu^{#mp}", itBkg, TColor::GetColor("#3b0160")); // kRed);
  p->AddSample("DYJetsToLL_M50_aMCatNLO",     " Z/#gamma* #rightarrow e^{#pm}#mu^{#mp}", itBkg);
  p->AddSample("TTbar_Powheg", "t#bar{t}", itBkg, TColor::GetColor("#669966")); // TColor::GetColor("#8ADCFF"));
  p->AddSample("TW", "tW", itBkg, TColor::GetColor("#ff4800")); // TColor::GetColor("#ffc878"));
  p->AddSample("TbarW", "tW", itBkg);
  p->AddSample("TTbar_PowhegSemi","Non W/Z", itBkg, kGray);
  p->AddSample("WJetsToLNu_MLM","Non W/Z", itBkg, kGray);


  p->AddSample("MuonEG", "Data", itData);
  p->AddSample("SingleMuon", "Data", itData);
  p->AddSample("SingleElec", "Data", itData);

  p->AddSample("TTbar_Powheg_hdampUp", "t#bar{t}", itSys, 1,  "hdampUp"); 
  p->AddSample("TTbar_Powheg_hdampDown", "t#bar{t}", itSys, 1,  "hdampDown"); 




  p->AddSample("TTbar_Powheg_ueUp", "t#bar{t}", itSys, 1,  "ueUp"); 
  p->AddSample("TTbar_Powheg_ueDown", "t#bar{t}", itSys, 1,  "ueDown"); 
  p->AddSample("TTbar_Powheg_isrUp", "t#bar{t}", itSys, 1,  "isrUp"); 
  p->AddSample("TTbar_Powheg_isrDown", "t#bar{t}", itSys, 1,  "isrDown"); 
  p->AddSample("TTbar_Powheg_fsrUp", "t#bar{t}", itSys, 1,  "fsrUp"); 
  p->AddSample("TTbar_Powheg_fsrDown", "t#bar{t}", itSys, 1,  "fsrDown"); 

  p->AddSample("TW_noFullyHadr_isrUp","tW", itSys, 1,  "isrUp");
  p->AddSample("TW_noFullyHadr_isrDown","tW", itSys, 1,  "isrDown");
  p->AddSample("TW_noFullyHadr_fsrUp","tW", itSys, 1,  "fsrUp");
  p->AddSample("TW_noFullyHadr_fsrDown","tW", itSys, 1,  "fsrDown");

  p->AddSample("TW_noFullyHadr_MEscaleUp","tW", itSys, 1,  "tWMe_s_caleUp");
  p->AddSample("TW_noFullyHadr_MEscaleDown","tW", itSys, 1,  "tWMe_s_caleDown");

  p->AddSample("TbarW_noFullyHadr_isrUp","tW", itSys, 1,  "isrUp");
  p->AddSample("TbarW_noFullyHadr_isrDown","tW", itSys, 1,  "isrDown");
  p->AddSample("TbarW_noFullyHadr_fsrUp","tW", itSys, 1,  "fsrUp");
  p->AddSample("TbarW_noFullyHadr_fsrDown","tW", itSys, 1,  "fsrDown");
  p->AddSample("TbarW_noFullyHadr_MEscaleUp","tW", itSys, 1,  "tWMe_s_caleUp");
  p->AddSample("TbarW_noFullyHadr_MEscaleDown","tW", itSys, 1,  "tWMe_s_caleDown");

  p->AddSample("TTbar_Powheg", "t#bar{t}", itSys, 1, "ScaleUp"); 
  p->AddSample("TTbar_Powheg", "t#bar{t}", itSys, 1, "ScaleDown"); 
  p->AddSample("TTbar_Powheg", "t#bar{t}", itSys, 1, "pdfUp"); 
  p->AddSample("TTbar_Powheg", "t#bar{t}", itSys, 1, "pdfDown"); 


  
  p->SetPlotFolder("Control/");
  
  p->AddSystematic("stat,JES,Btag,Mistag,PU,ElecEff,MuonEff,Trig"); //,LepEff


  p->doYieldsInLeg=false;

  p->SetRatioMin( 0.6 );
  p->SetRatioMax( 1.4 );

  p->doSetLogy = false;
  p->doData = true;
  if (setLegendLeft) p->SetLegendPosition("UL");
  p->DrawStack("ElMu_0_log", 1);


  delete p;

}


void runLooper(){
  Looper* p = new Looper(pathToTree, NameOfTree, "TMET", "TMET > 0", "ElMu", 30, 0, 300);
  Histo* h = p->GetHisto("TW");
  h->SetLineColor(kRed);
  cout << "nEntries = " << h->GetEntries() << endl;
  cout << "Yield = " << h->Integral()*35900 << endl;
  h->Draw();
}
