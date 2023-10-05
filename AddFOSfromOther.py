import os
import shutil


def GetNameFormFileName(filename):
	ss=filename.split('_')
	for s in ss:
		if(any(map(str.isdigit, s))==False and s!='N' and s!='О' and s!='В' and s!='ДВ'  and s!='ФТД'):
			iss=ss.index(s)
			return ss[iss]
	return filename

def GetRPD_FOS(dirname):
	paths1=os.listdir(dirname)

	paths=[]
	for p in paths1:
		path, ext = os.path.splitext(p)
		if not ext:
			pass
		else:
			if(ext=='.pdf'):
				paths.append(path)
	pathsRPD=[]
	pathsFOS=[]
	for p in paths:
		if(p.find('ФОС')!=-1):
			pathsFOS.append([p,'',GetNameFormFileName(p)])
		else:
			pathsRPD.append([p,'',GetNameFormFileName(p)])

	for ipr in range(len(pathsRPD)):
		if(pathsRPD[ipr][1]==''):
			for ipf in range(len(pathsFOS)):
				if(pathsRPD[ipr][2]==pathsFOS[ipf][2]):
					pathsRPD[ipr][1]=pathsFOS[ipf][0]
					pathsFOS[ipf][1]=pathsRPD[ipr][0]
	return pathsRPD, pathsFOS

maindir='step3' #директория в которой проверяется наличие ФОС
pathsRPD, pathFOS= GetRPD_FOS(maindir)
pathNoFos=[pr for pr in pathsRPD if pr[1]=='']

otheryears=['../../2023/КиСВЧэ/step3']#набор директорий в которой проверяется наличие ФОС с таким же именем для копирования
for otheryear in otheryears:
	pathsRPD1, pathFOS1= GetRPD_FOS(otheryear)
	fullname=True
	if(otheryear.find('2020')!=-1): #в 2020 имена не совпадают и файлы не содержат ФОС
		pathFOS1=[p for p in pathsRPD1] # все файлы этот ФОСы
		fullname=False # нужно для применения нечеткого сравнения строк https://habr.com/ru/articles/733492/
	for infos in range(len(pathNoFos)):
		if(pathNoFos[infos][1]==''):
			for ipf1 in range(len(pathFOS1)):
				if((fullname==True and pathNoFos[infos][2]==pathFOS1[ipf1][2]) or (fullname==False and  pathNoFos[infos][2]==pathFOS1[ipf1][2])):
					# если имена совпали копируем в исходную директорию maindir первая страница с неправильным годом будет подменена при выполнении MakeRPDwithSignature.py
					pathNoFos[infos][1] = pathNoFos[infos][0]+'_ФОС'
					shutil.copyfile(otheryear+'/'+pathFOS1[ipf1][0]+'.pdf',maindir+'/'+pathNoFos[infos][1]+'.pdf')
