import urllib.request
import re
import codecs
import string
import sys

arg_valide=True

if len(sys.argv)!=3:
	print("Veuillez donner le domaine d'extraction et le port du serveur en arguments")
	arg_valide=False

else:	
	if (not re.match("[A-Za-z]-[A-Za-z]",sys.argv[1])) or (sys.argv[1][2].upper()< sys.argv[1][0].upper()):
		print("Le format du premier argument est faux")
		arg_valide=False
	
	if re.search(r"\D",sys.argv[2]):
		print("Le format du port est incorrect")
		arg_valide=False

if arg_valide:
	
	Dinfo={}
	s=0
	
	dic=open("subst.dic",'w',encoding='utf-16-le')
	dic.write('\ufeff')
	
	alpha=string.ascii_uppercase
	
	for j in range(alpha.index(sys.argv[1].upper()[0]),alpha.index(sys.argv[1].upper()[2])+1):
		
		url= urllib.request.urlopen('http://localhost:'+sys.argv[2]+'/vidal/vidal-Sommaires-Substances-'+alpha[j]+'.htm')
		html=url.read().decode('utf8')
		
		medoc=re.findall("(<a href=\"Substance.+?>)(.+?)(</a>)",html)
		Dinfo[alpha[j]]=len(medoc)
		s=s+len(medoc)
		
		for i in medoc:
			dic.write(i[1]+",.N+subst\n")
		
		
	dic.close()
		
	infos1=open("infos1.txt",'w')
	
	for i in Dinfo:
		infos1.write(i+": "+str(Dinfo.get(i))+"\n")
	infos1.write("\nTotal: "+str(s))