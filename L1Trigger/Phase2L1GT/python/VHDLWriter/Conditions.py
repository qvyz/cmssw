from L1Trigger.Phase2L1GT.l1GTScales import l1GTScales

class Condition:
    _ObjectNameConversions = {
        "GTT Prompt Jets" : "GTT_PROMPT_JETS_SLOT",
        "GTT Displaced Jets" : "GTT_DISPLACED_JETS_SLOT",
        "GTT Ht Miss Prompt" : "GTT_HT_MISS_PROMPT_SLOT",
        "GTT Ht Miss Displaced" : "GTT_HT_MISS_DISPLACED_SLOT",
        "GTT Et Miss" : "GTT_ET_MISS_SLOT",
        "GTT Taus" : "GTT_TAUS_SLOT",
        "GTT Phi Candidates" : "GTT_PHI_CANDIDATE_SLOT",
        "GTT Rho Candidates" : "GTT_RHO_CANDIDATE_SLOT",
        "GTT Bs Candidates" : "GTT_BS_CANDIDATE_SLOT",
        "GTT Prim Vert" : "GTT_PRIM_VERT_SLOT",
        "CL2 Jets" : "CL2_JET_SLOT",
        "CL2 Ht Miss" : "CL2_HT_MISS_SLOT",
        "CL2 Et Miss" : "CL2_ET_MISS_SLOT",
        "CL2 Taus" : "CL2_TAU_SLOT",
        "CL2 Electrons" : "CL2_ELECTRON_SLOT",
        "CL2 Photons" : "CL2_PHOTON_SLOT",
        "GCT Non Iso Eg" : "GCT_NON_ISO_EG_SLOT",
        "GCT Iso Eg" : "GCT_ISO_EG_SLOT",
        "GCT Jets" : "GCT_JETS_SLOT",
        "GCT Taus" : "GCT_TAUS_SLOT",
        "GCT Ht Miss" : "GCT_HT_MISS_SLOT",
        "GCT Et Miss" : "GCT_ET_MISS_SLOT",
        "GMT Sa Prompt" : "GMT_SA_PROMPT_SLOT", 
        "GMT Sa Displaced" : "GMT_SA_DISPLACED_SLOT", 
        "GMT Tk Muon" : "GMT_TK_MUON_SLOT", 
        "GMT Topo" : "GMT_TOPO_SLOT"
        }


    def __init__(self):
        self._PossibleCuts = []
        self.Cuts = {}
        self.InputObjects = {}
        self._HWConversionFunctions ={}

    def _setInputObject(self,condition,value):
        self.InputObjects[condition] = self._ObjectNameConversions.get(value)
    def _setPosibleCuts(self, cuts):
        self._PossibleCuts = cuts

    def setCuts(self, **cutsdict):
        for key , value in cutsdict.items():
            if key in self._PossibleCuts:
                if key in self._HWConversionFunctions:
                    self.Cuts[key] = self._HWConversionFunctions[key](value)
                else:
                    self.Cuts[key] = value
    def setCut(self,key,value):
                if key in self._HWConversionFunctions:
                    self.Cuts[key] = self._HWConversionFunctions[key](value)
                else:
                    self.Cuts[key] = value        

    def setName(self,name):
        self.Name = name


    def _setInputTags(self, tags):
        self._InputTags = tags

    def setInputObjects(self, **inobjs):
        for name, value in inobjs.items():
            if name in self._InputTags:
                self.InputObjects[name] = value
    def _setHWConversionFunctions(self,indict):
           self._HWConversionFunctions = indict

    def getPossibleCuts(self):
        return self._PossibleCuts

class DoubleObjCond(Condition):
    Label = "L1GTDoubleObjectCond"
    Template = "double.template"
    def __init__(self):
        Condition.__init__(self)
        self._setPosibleCuts(
            [
            "pt1_cut",
            "pt2_cut",
            "minEta1_cut",
            "maxEta1_cut",
            "minEta2_cut",
            "maxEta2_cut",
            "minPhi1_cut",
            "maxPhi1_cut",
            "minPhi2_cut",
            "maxPhi2_cut",
            "minDz1_cut",
            "maxDz1_cut",
            "minDz2_cut",
            "maxDz2_cut",
            "qual1_cut",
            "qual2_cut",
            "iso1_cut",
            "iso2_cut",
            "dEtaMin_cut",
            "dPhiMin_cut",
            "dRSquaredMin_cut",
            "invMassDiv2Min_cut",
            "invMassDiv2Max_cut",
            "os_cut",
            "ss_cut"
            ]
        )
        self._setHWConversionFunctions(
        {
        "pt1_cut": l1GTScales.to_hw_pT,
        "pt2_cut": l1GTScales.to_hw_pT,
        "minEta1_cut": l1GTScales.to_hw_eta,
        "maxEta1_cut": l1GTScales.to_hw_eta,
        "minEta2_cut": l1GTScales.to_hw_eta,
        "maxEta2_cut": l1GTScales.to_hw_eta,
        "minPhi1_cut": l1GTScales.to_hw_phi,
        "maxPhi1_cut": l1GTScales.to_hw_phi,
        "minPhi2_cut": l1GTScales.to_hw_phi,
        "maxPhi2_cut": l1GTScales.to_hw_phi,
        "minDz1_cut": l1GTScales.to_hw_dZ,
        "maxDz1_cut": l1GTScales.to_hw_dZ,
        "minDz2_cut": l1GTScales.to_hw_dZ,
        "maxDz2_cut": l1GTScales.to_hw_dZ,
        "dEtaMin_cut": l1GTScales.to_hw_eta,
        "dPhiMin_cut": l1GTScales.to_hw_phi,
        "dRSquaredMin_cut": l1GTScales.to_hw_RSquared,
        "invMassDiv2Min_cut": l1GTScales.to_hw_InvMass,
        "invMassDiv2Max_cut": l1GTScales.to_hw_InvMass
        }
        )


        self._setInputTags(
            ["col1Tag",
             "col2Tag"]
        )
class SingleObjCond(Condition):
    Label = "L1GTSingleObjectCond"
    Template = "single.template"
    def __init__(self):
        Condition.__init__(self)
        self._setPosibleCuts(
            ["pt_cut",
             "minEta_cut",
             "maxEta_cut",
             "minPhi_cut",
             "maxPhi_cut",
             "minDz_cut",
             "maxDz_cut",
             "qual_cut"]
        )
        self._setHWConversionFunctions(
        {
        "pt_cut": l1GTScales.to_hw_pT,
        "minEta_cut": l1GTScales.to_hw_eta,
        "maxEta_cut": l1GTScales.to_hw_eta,
        "minPhi_cut": l1GTScales.to_hw_phi,
        "maxPhi_cut": l1GTScales.to_hw_phi,
        "minDz_cut": l1GTScales.to_hw_dZ,
        "maxDz_cut": l1GTScales.to_hw_dZ,
        }
        )
        self._setInputTags(
            ["colTag"]
        )


class DefineAlgoBits:
    def __init__(self):
        self.Assignment = {}
    def SetBit(self,Name,Algobit):
        self.Assignment[Name] = Algobit


    

