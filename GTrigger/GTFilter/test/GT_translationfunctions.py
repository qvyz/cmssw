import FWCore.ParameterSet.Config as cms
import json
import GT_vhdl_template as vhdl







#Currently it just takes a float and converts it to an integer:
#Example from float of config input to HW:
def pt_to_HW(ptfloat):
	return cms.int32(int(ptfloat))


def phi_to_HW(phifloat):
	return cms.int32(int(phifloat))

def eta_to_HW(etafloat):
	return cms.int32(int(etafloat * 14 + 3))















class GlobalTrigger():
	###this is janky###
	"""
	translate_genmap = {
	'MinPtfirst' : 'pT1_cut => to_unsigned(', 
	'MinPtsecond': 'pT2_cut => to_unsigned(',  
	'MinEtafirst':'minEta1_cut => to_signed(', 
	'MinEtasecond': 'minEta2_cut => to_signed(', 
	'MaxEtafirst': 'maxEta1_cut => to_signed(' ,
	'MaxEtasecond': 'maxEta2_cut => to_signed('
	}
	### this is even jankier ###
	translate_width = {
	'MinPtfirst' : '14',
	'MinPtsecond': '14',
	'MinEtafirst':'12',
	'MinEtasecond': '12',
	'MaxEtafirst': '12' ,
	'MaxEtasecond': '12'
	}

	
	translate_portmap = {
	'"L1TkElectronsEllipticMatchCrystal","EG"' : 'ELECTRON_SLOT',
	'"L1TkMuons"' : 'MU_SLOT',
	'inputTag1' : 'object1',
	'inputTag2' : 'object2'
	}	

	translate_algoname = {
	'P2GTDoubleObjFilterMuEle' : 'p2gt_doubleObjCond'

	}
	condlist = [
	'P2GTDoubleObjFilterMuEle'
	]

	
	metalist = [
	'TriggerResultsFilter'
	]
	"""



	def __init__(self,name):
		self.name = name 
		self.algorithms = [] #a list for the names of the algopaths (could be skipped and added to algoobjs instantatniously# 
		self.algoobjs = [] #list of objs of type GTAlgoobj
		self.knownmetaobjs = {} #Metafilters like triggerresultsfilter where a conversion is known taken from json
		self.knownalgoobjs = {} #EDFilters that are a condition 


	#### This has to be changed: ####
	#because it will take any input and wont check if it makes sense: # 
	def addAlgo(self, algo): 
		try:
	
			self.algorithms.append(algo.label())
		except:
			self.algorithms.append(algo)
	

	
	##read the json
	def importjson(self,jsonfile):
		with open(jsonfile) as fl:
			jsondict = json.load(fl)
			self.knownalgoobjs = jsondict["Conditions"]	
			self.knownmetaobjs = jsondict["Metafilters"] 
	### returns the list of names in algos, currently not used
	def getAlgos(self):
		return(self.algorithms)


	### class for storing the actual paths:
	class _GTAlgoobj():
		def __init__(self,key,value):	#read the fi
			self.algoname = key 		#pathname used in vhdl as signal to write output of entity	
			self.algovalues = value 	#list of modules in the path (currently only works for single module paths)
			self.algobit = int		#number of bit in the vhdl output
			self.filtdict = {}		#dict of all filters 
			self.metadict = {}		#dict of metafilters
			self.conddict = {}		#dict of condition filters
			self.isalgo = True		# does the object get an algobit


			#### set the algobit
		def setAlgobit(self,a):
			self.algobit = a
	
			####read filterobjects from names of filters and add them to a dict
		def setfilters(self,process):
			self.filtdict = dict((k,process.filters[k]) for k in self.algovalues if k in process.filters)
	


			
			####method to distinguish between conditions and currently triggerresultsfilter
		def settype(self,conditions,metalist):
			for filt in self.filtdict:
				if self.filtdict[filt].type_() in conditions:
					self.conddict[filt] = self.filtdict[filt]
				if self.filtdict[filt].type_() in metalist:
					self.metadict[filt] = self.filtdict[filt]





		




			#### debug:
		def printtypes(self):
			print("filters")
			for filt in self.filtdict:
				print(self.filtdict[filt].type_())
			print("condidtions")
			
			for filt in self.conddict:
				print(self.conddict[filt].type_())

			print("metafilters")
			
			for filt in self.metadict:
				print(self.metadict[filt].type_())





			#### debug
	def debugPrintalgos(self):
		for algo in self.algoobjs:
			algo.printtypes()







	def getParameters(self,process):
		propathdict = process.paths
		profiltdict = process.filters
		pathdict_filtered = dict((k,propathdict[k]) for k in self.algorithms if k in propathdict)
		algolist = []
		
		for path in pathdict_filtered:
			self.algoobjs.append(self._GTAlgoobj(path,list(pathdict_filtered[path].moduleNames())))	

		### deduct filter and type from name
		for algo in self.algoobjs: 
			algo.setfilters(process) 
			algo.settype(list(self.knownalgoobjs.keys()),self.knownmetaobjs["names"])	
		###rewrite algoobjs should be a dict not a list otherwise, this happens: ###
		inalgolist = []
		for algo in self.algoobjs:
			inalgolist.append(algo.algoname)
		for algo in self.algoobjs:
			if algo.metadict:
				for entry in algo.metadict:
					metalist = self.gettrfpaths(algo.metadict[entry])
					for metapart in metalist:
						for meta in metapart:
							if meta not in inalgolist:	
								if meta in process.paths:
									x =self._GTAlgoobj(meta,list(process.paths[meta].moduleNames()))
									x.setfilters(process)
									x.settype(self.condlist,self.metalist)
									x.isalgo = False
									self.algoobjs.append(x)


	####print vhdl
	def printvhdl(self):	
		vhdl.writeVHDLintro()
		for algo in self.algoobjs: 
			self.writeVHDLsignals(algo)

		
		vhdl.writeVHDLintermediatefirst()


		for algo in self.algoobjs:
			self.writeVHDLcond(algo)




		vhdl.writeVHDLintermediatesecond()


		iterator = 0
		for algo in self.algoobjs:
			if algo.isalgo:
				self.writeAlgobits(algo,iterator)
				iterator = iterator + 1		
		vhdl.WriteVHDLend()
		

		### This parses the triggerresultsfilter
		### has to be rewritten: ###
	def gettrfpaths(key,value):
		tclist = []
		triggercond = value.triggerConditions.value()
	
		for trig in triggercond: 
			tclist.append(trig.split())
			return(tclist)



					




	#### print function for vhdl conditions a bit messy, dont know a better way
	def writeVHDLcond(self,a):
		for cond in a.conddict:
			jsondb =  self.knownalgoobjs[a.conddict[cond].type_()]
			print(a.conddict[cond].label() + " : entity work." + jsondb["vhdl_name"])
			print("generic map (")
			jsongeneric = jsondb["Generic_map"]	
			jsonport = jsondb["Port_map"]
			if jsonport["inputTag1"] == jsonport["inputTag2"]:
				 
				print("different_objects => false,") ###This is wrong have to structure inputTag in json  better				
			else:
				print("different_objects => true,")
			
			for params in a.conddict[cond].parameterNames_():
				if params in jsongeneric:
					jsonpara = jsongeneric[params]
					print(jsonpara["vhdl_name"] + "=> to_{}({},{}),".format(jsonpara["sign"],a.conddict[cond].getParameter(params).pythonValue(),jsonpara["width"]))

			print("ss_cut => true \n)")	
			vhdl.portdefaults()
			for params in a.conddict[cond].parameterNames_():
				if params in jsonport:
					print(jsonport[params] + "=>delayed_objects(BX_ZERO)("+jsonport[a.conddict[cond].getParameter(params).pythonValue()]+"),")


			print("algo_bit_out =>"+a.algoname)
			print("      );")
			print("""


""")

			


	#### signals used in vhdl
	def writeVHDLsignals(self,a):
		print("signal "+ a.algoname +" : std_logic;")



	#### I have to rewrite this does not work if metadict has more than one entry ####
	def writeAlgobits(self,a,algobit):
		if a.metadict:

			for meta in a.metadict:
				#### This is the problematic line: ####
				print("	algo_bits_int2({}) <= ".format(algobit)+str(a.metadict[meta].triggerConditions.value()[0])+" ;")
		else:
			print("	algo_bits_int2({}) <= ".format(algobit)+a.algoname +" ;")







