import os
import kpfudatabase

#требуется установленные qpdf и inkscape

paths1=os.listdir('step3')

paths=[]
for p in paths1:
	path, ext = os.path.splitext(p)
	if not ext:
		pass
	else:
		if(ext=='.pdf'):
			paths.append(p)

for p in paths:
	kpfudatabase.changeYearOnly('step4/'+p,  'step5/'+p)
