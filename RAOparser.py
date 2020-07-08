import pandas as pd
def RAOparse(file):
	posi=False
	count=0
	with open(file,"r") as f:
		variable=None
		fo=open("data.tsv","w+")
		for line in f.readlines():
			if not posi and line.startswith("frequencies"):
				variable="fr"
				continue
			elif not posi and line.startswith("headings:"):
				variable="hd"
				continue
			if variable=="fr":
				fline=list(map(float,line.split('\t')))
				variable=None
			elif variable=="hd":
				hdline=line
				hdline=list(map(float,line.split('\t')))
				variable=None
		#RAOS
			if line.startswith("raos:"):
				posi=True
				continue
			elif line.startswith("qtf_data:"):
				posi=False
				break
			if posi:
				fo.write(line)
		fo.close()
	dfleft=pd.DataFrame(columns=["frequency","heading"])
	for head in hdline:
		for freq in fline:
			dfleft=dfleft.append(pd.DataFrame.from_dict({"heading":[head],"frequency":[freq]},dtype=float),ignore_index=True)
	dfright=x=pd.read_csv("data.tsv",sep="\t",names=["SurgeModulo","SurgePhase","SwayModulo","SwayPhase","HeaveModulo","HeavePhase","RollModulo","RollPhase","PitchModulo","PitchPhase","YawModulo","YawPhase",""])
	dfright.dropna(axis=1,how="all",inplace=True)
	result=pd.concat([dfleft,dfright],axis=1,sort=False)
	return result,max(fline),min(fline)
	#result.to_csv("out.csv",index=False)

	
		
if __name__ =="__main__":
	RAOparse("D:\\S6 MCA\\Main_project_siva_and_prasanth\\data\\RAO loaded.dat")