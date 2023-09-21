import os
import csv
import subprocess
import shutil
import imageio
from PIL import Image
import numpy as np
from pdf2image import convert_from_path

colname=[
	'exam',
	'assessment',
	'assessment_with_score',
	'course work',
	'Common',
	'classroom_Common',
	'classroom_lecture',
	'classroom_practice',
	'classroom_laboratory',
	'classroom_lecture_elec',
	'classroom_practice_elec',
	'classroom_laboratory_elec',
	'independent_work',
	'course_project',
	'1sem_lecture',
	'1sem_practice',
	'1sem_laboratory',
	'1sem_lecture_elec',
	'1sem_practice_elec',
	'1sem_laboratory_elec',
	'1sem_individual_sessions',
	'1sem_individual_project',
	'2sem_lecture',
	'2sem_practice',
	'2sem_laboratory',
	'2sem_lecture_elec',
	'2sem_practice_elec',
	'2sem_laboratory_elec',
	'2sem_individual_sessions',
	'2sem_individual_project',
	'3sem_lecture',
	'3sem_practice',
	'3sem_laboratory',
	'3sem_lecture_elec',
	'3sem_practice_elec',
	'3sem_laboratory_elec',
	'3sem_individual_sessions',
	'3sem_individual_project',
	'4sem_lecture',
	'4sem_practice',
	'4sem_laboratory',
	'4sem_lecture_elec',
	'4sem_practice_elec',
	'4sem_laboratory_elec',
	'4sem_individual_sessions',
	'4sem_individual_project',
	'5sem_lecture',
	'5sem_practice',
	'5sem_laboratory',
	'5sem_lecture_elec',
	'5sem_practice_elec',
	'5sem_laboratory_elec',
	'5sem_individual_sessions',
	'5sem_individual_project',
	'6sem_lecture',
	'6sem_practice',
	'6sem_laboratory',
	'6sem_lecture_elec',
	'6sem_practice_elec',
	'6sem_laboratory_elec',
	'6sem_individual_sessions',
	'6sem_individual_project',
	'7sem_lecture',
	'7sem_practice',
	'7sem_laboratory',
	'7sem_lecture_elec',
	'7sem_practice_elec',
	'7sem_laboratory_elec',
	'7sem_individual_sessions',
	'7sem_individual_project',
	'8sem_lecture',
	'8sem_practice',
	'8sem_laboratory',
	'8sem_lecture_elec',
	'8sem_practice_elec',
	'8sem_laboratory_elec',
	'8sem_individual_sessions',
	'8sem_individual_project'
	]

def GetAuthors(filename, RPD):
	if(os.path.isfile('authors.txt')):
		with open('authors.txt', 'r', encoding='utf-8') as f:
			ls = csv.reader(f, dialect='excel', delimiter='\t')
			for l in ls:
				for irpd in range(len(RPD)):
					if(l[0]==RPD[irpd]['shifr']):
						FIO=l[1]
						if(len(l)>2):
							title=l[2]
						if(len(l)>3):
							placeofwork=l[3]
						RPD[irpd]['author']={'FIO':FIO, 'title':title, 'placeofwork':placeofwork}

def GetPPS():
	pps=[]
	if(os.path.isfile('pps/Сведения по всем ППС КФУ.csv')):
		with open('pps/Сведения по всем ППС КФУ.csv', 'r', encoding='utf-8') as f:
			ls = csv.reader(f, dialect='excel', delimiter='\t')
			for l in ls:
				if(l[0].find('№')!=-1 or l[0].find('п/п')!=-1):
					continue
				pps.append(l[1:len(l)])
	return pps
	
	
def GetPlan(filename, nsem):
	rpd = []
	with open(filename, 'r', encoding='utf-8') as f:
		ls = csv.reader(f, dialect='excel')
		FindstartLine=0
		for row in ls:
			if(FindstartLine==0):
				FindstartLine=1
			if(FindstartLine==1 and row[0].find('Б1')!=-1):
				FindstartLine=2
			if(FindstartLine==2):
				if(row[0].find('&nbsp')==-1 and row[1].find('Дисциплины по выбору')==-1):
					indname=1
					if(row[1].find('&nbsp')!=-1):
						indname=2
					rpdstate='empty'
					rpdstateIndx = ''
					if(row[3].find("next_small.png")!=-1):
						rpdstate = 'To write'
						if(row[3].find("Places-folder-txt-icon")!=-1):
							rpdstate = 'document for approval'
						if(row[3].find("folder_plus")!=-1):
							rpdstate = 'document is ready'
						if (row[3].find("folder_minus") != -1):
							rpdstate = 'error in document'
						i=row[3].find("discipline_programs.program_form?")
						il=len("discipline_programs.program_form?")
						j=row[3].find("')")
						if(i!=-1 and j!=-1):
							rpdstateIndx=row[3][i+il:j].replace('&amp;','&')
					rpdElecstate='empty'
					if(row[4].find("next_small.png")!=-1):
						rpdElecstate = 'Have electronic doc'
						if(row[4].find("monitor--pencil")!=-1):
							rpdElecstate = 'Electronic doc attached'
					name=row[indname].replace("&nbsp;","").strip()
					rpd.append({'shifr': row[0], 'name': name, 'C': [],'rpdstate':rpdstate, 'rpdstateIndx':rpdstateIndx, 'rpdElecstate':rpdElecstate })
					if(indname==2):
						indname=1
					b={}
					for k in range(len(colname)):
						if(indname+4+k >= len(row)):
							break
						s=row[indname+4+k].replace('&nbsp;','').strip()
						if(k<3):
							h=[]
							for si in range(len(s)):
								a = s[si]
								if (a.isdecimal()):
									ai = int(a)
									h.append(ai)
							b[colname[k]] = h
						else:
							h=-1
							if(s!=''):
								try:
									h=int(s)
								except:
									h=-1
							b[colname[k]]=h
					rpd[-1]['Hours']=b

					sem=[False for mm in range(nsem)]
					for m in range(len(colname)):
						for s in range(len(sem)):
							if(colname[m].find(str(s+1)+'sem')!=-1 and rpd[-1]['Hours'][colname[m]]!=-1):
								sem[s]=True
					sem1=[ mm+1 for mm in range(nsem) if sem[mm]]
					sems=rpd[-1]['Hours']['exam']+rpd[-1]['Hours']['assessment']+rpd[-1]['Hours']['assessment_with_score']
					for sa in sems:
						if(not (sa in sem1)):
								sem1.append(sa)
					if(len(sem1)==0):
						print('error in ' + rpd[-1]['name'])
					rpd[-1]['semestr']=sem1
					rpd[-1]['HoursLec'] ={}
					rpd[-1]['HoursLec']['Lecture'] = rpd[-1]['Hours']['classroom_lecture']
					rpd[-1]['HoursLec']['LectureEl'] = rpd[-1]['Hours']['classroom_lecture_elec']
					rpd[-1]['HoursLec']['Practice'] = rpd[-1]['Hours']['classroom_practice']
					rpd[-1]['HoursLec']['PracticeEl'] = rpd[-1]['Hours']['classroom_practice_elec']
					rpd[-1]['HoursLec']['Self'] = rpd[-1]['Hours']['independent_work']
					rpd[-1]['HoursLec']['lab'] = rpd[-1]['Hours']['classroom_laboratory']
					rpd[-1]['HoursLec']['KSR'] = 0
					rpd[-1]['HoursLec']['Zach'] = rpd[-1]['Hours']['Common']/36.0
					rpd[-1]['Ze'] = rpd[-1]['HoursLec']['Zach']
					rpd[-1]['HoursLec']['Common'] = rpd[-1]['Hours']['Common']
					rpd[-1]['HoursLec']['EkzSem'] = rpd[-1]['Hours']['exam']
					rpd[-1]['HoursLec']['ZachSem'] = rpd[-1]['Hours']['assessment']
					rpd[-1]['HoursLec']['ZachSemOch'] = rpd[-1]['Hours']['assessment_with_score']

					parts=-1
					if(rpd[-1]['shifr'].find('Б1.О')!=-1):
						parts=0
					if(rpd[-1]['shifr'].find('Б1.В')!=-1):
						parts=1
						if(rpd[-1]['shifr'].find('ДВ')!=-1):
							parts=2
					if(rpd[-1]['shifr'].find('Б2.')!=-1):
						parts=3
					if(rpd[-1]['shifr'].find('Б3.')!=-1):
						parts=4
					if(rpd[-1]['shifr'].find('ФТД.')!=-1):
						parts=5
					rpd[-1]['parts']=parts
		return rpd

def shortnameRPD(name):
	name=name.replace(',','_').replace(':','')
	if (len(name) > 80):
		ls=name.split(' ')
		rstr=''
		for l in ls:
			rstr+=l + ' '
			if(len(rstr)>80):
				return rstr.strip()
	return name

def makeRPDfilename(shifrRPD,nameRPD,Shifr,NameShort,year):
	nameRPD1=shortnameRPD(nameRPD)
	return shifrRPD.replace(".", "_") + '_' + nameRPD1 + '_' + Shifr.replace(".", "") + '_' + NameShort + '_' + year

def copyfileWithCheck(oldname, newname, name):
	if(os.path.isfile(oldname)):
		shutil.copy(oldname, newname)
		return True
	else:
		print('%s файл для %s не существует' % (oldname , name))
		return False

def ChYear(name, ChangeYear):
	namef, ext=os.path.splitext(name)
	if (len(ChangeYear) > 0):
		proc = subprocess.Popen("inkscape --export-filename=tmp/pages/%s.svg tmp/pages/%s.pdf" % (namef, namef),shell=True)
		proc.wait()
		with open("tmp/pages/%s.svg" % (namef), 'rb') as fin:
			buf = fin.read()
			buf = buf.replace(b'2022', b'2021')
			fin.close()
			with open("tmp/pages/%s.svg" % (namef), 'wb') as fout:
				fout.write(buf)
				fout.close()
		proc = subprocess.Popen("inkscape --export-filename=tmp/pages/%s.pdf tmp/pages/%s.svg" % (namef, namef),shell=True)
		proc.wait()

def AddSignature(namef, Signature, scale, place):
	pages = convert_from_path(namef+'.pdf', 500)
	pages[0].save(namef+'.png', 'PNG')
	# proc = subprocess.Popen("inkscape --export-filename=tmp/pages/%s.png tmp/pages/%s.svg" % (namef, namef),shell=True)
	# proc.wait()
	img1 = Image.open(namef+'.png')
	img2 = Image.open(Signature)
	img3=img2.resize((int(img2.width/scale),int(img2.height/scale)))
	img1.paste(img3, place)
	img1.save(namef+'.pdf')


def changeYearOnly(namefile, fileout):
	if(os.path.isfile(namefile)):
		#открываем шаблон
		#копируем РПД
		copyfileWithCheck(namefile,'tmp/rpd1.pdf',namefile)
		#чистим директорию pages
		proc = subprocess.Popen("rm tmp/pages/*", shell=True)
		proc.wait()
		#разбиваем файл с РПД на страницы
		proc = subprocess.Popen("qpdf tmp/rpd1.pdf tmp/pages/out.pdf --split-pages", shell=True)
		proc.wait()
		#получаем список файлов содержащик одну страницу
		paths1 = os.listdir('tmp/pages')
		paths1.sort()
		# меняем год на первой и двух последних страницах
		ChYear(paths1[0], '2021')
		ChYear(paths1[-2], '2021')
		ChYear(paths1[-1], '2021')
		#составляем файл обратно
		s = "qpdf --empty --pages tmp/rpd.pdf"
		for i in range(1, len(paths1)):
			s += ' "tmp/pages/' + paths1[i] + '"'
		s += ' -- "' + fileout + '"'
		proc = subprocess.Popen(s,shell=True)
		proc.wait()
	else:
		print('нет файла '+namefile)



def changefirstpageRPD(namefile, namefileFOS, rpdname, rpdshifr, fileout, year, Shifr, NameCom, Name, Kvalif):
	if(os.path.isfile(namefile)):
		#открываем шаблон
		with open('src/rpd.html', 'r', encoding='cp1251') as fin:
			fileinf=fin.read()
			fin.close()
			# меняем в шаблоне параметры
			fileinf=fileinf.replace('$year$',year)
			fileinf=fileinf.replace('$name$', rpdname)
			fileinf=fileinf.replace('$shifr$', rpdshifr)
			fileinf=fileinf.replace('$shifrdir$', Shifr)
			fileinf=fileinf.replace('$dir$', NameCom)
			fileinf=fileinf.replace('$profile$', Name)
			fileinf=fileinf.replace('$cvalification$', Kvalif)
			# сохраняем первую страницу как doc
			with open('tmp/rpd.doc', 'w', encoding='cp1251') as fout:
				fout.write(fileinf)
				fout.close()
				# конвертируем первую страницу в pdf с помощью libreoffice (libreoffice желательно держать открытым)
				proc=subprocess.Popen("libreoffice --headless --convert-to pdf:writer_pdf_Export tmp/rpd.doc --outdir tmp/", shell=True)
				proc.wait()
			#копируем РПД
			copyfileWithCheck(namefile,'tmp/rpd1.pdf',rpdname)
			#чистим директорию pages
			proc = subprocess.Popen("rm tmp/pages/*", shell=True)
			proc.wait()
			#разбиваем файл с РПД на страницы
			proc = subprocess.Popen("qpdf tmp/rpd1.pdf tmp/pages/out.pdf --split-pages", shell=True)
			proc.wait()
			#получаем список файлов содержащик одну страницу
			paths1 = os.listdir('tmp/pages')
			paths1.sort()
			if(year=='2021'):
				# меняем год на двух последних страницах
				ChYear(paths1[-2], '2021')
				ChYear(paths1[-1], '2021')
			#составляем файл из новой первой страницы, последующих страниц, фос, две последних
			s = "qpdf --empty --pages tmp/rpd.pdf"
			for i in range(1, len(paths1) - 2):
				s += ' "tmp/pages/' + paths1[i] + '"'
			if(namefileFOS!=''):
				s+=' "'+namefileFOS+'"'
			s += ' "tmp/pages/' + paths1[-2] + '"'
			s += ' "tmp/pages/' + paths1[-1] + '"'
			s += ' -- "' + fileout + '"'
			proc = subprocess.Popen(s,shell=True)
			proc.wait()
	else:
		print('нет файла '+namefile+' для ' + rpdname)

def InsertFOSOnly(namefile, namefileFOS, rpdname, fileout):
	if(os.path.isfile(namefile)):
		#копируем РПД
		copyfileWithCheck(namefile,'tmp/rpd1.pdf',rpdname,)
		#чистим директорию pages
		proc = subprocess.Popen("rm tmp/pages/*", shell=True)
		proc.wait()
		#разбиваем файл с РПД на страницы
		proc = subprocess.Popen("qpdf tmp/rpd1.pdf tmp/pages/out.pdf --split-pages", shell=True)
		proc.wait()
		#получаем список файлов содержащик одну страницу
		paths1 = os.listdir('tmp/pages')
		paths1.sort()
		#составляем файл из старой первой страницы, последующих страниц, фос, две последних
		s = "qpdf --empty --pages"
		for i in range(0, len(paths1) - 2):
			s += ' "tmp/pages/' + paths1[i] + '"'
		if(namefileFOS!=''):
			s+=' "'+namefileFOS+'"'
		s += ' "tmp/pages/' + paths1[-2] + '"'
		s += ' "tmp/pages/' + paths1[-1] + '"'
		s += ' -- "' + fileout + '"'
		proc = subprocess.Popen(s,shell=True)
		proc.wait()
	else:
		print('нет файла '+namefile+' для ' + rpdname)


def changefirstpageFOS(namefile,  rpdname, rpdshifr, fileout, year,Shifr, NameCom,Name,Kvalif, nofirstpage = False):
	if(os.path.isfile(namefile)):
		with open('src/fos.html', 'r', encoding='cp1251') as fin:
			fileinf=fin.read()
			fin.close()
			fileinf=fileinf.replace('$year$',year)
			fileinf=fileinf.replace('$name$', rpdname)
			fileinf=fileinf.replace('$shifrdir$', Shifr)
			fileinf=fileinf.replace('$shifr$', rpdshifr)
			fileinf=fileinf.replace('$dir$', NameCom)
			fileinf=fileinf.replace('$profile$', Name)
			fileinf=fileinf.replace('$cvalification$', Kvalif)
			#сохраняем как doc
			with open('tmp/fos.doc', 'w', encoding='cp1251') as fout:
				fout.write(fileinf)
				fout.close()
				#конвертируем в pdf с помощью libreoffice (libreoffice желательно держать открытым)
				proc=subprocess.Popen("libreoffice --headless --convert-to pdf:writer_pdf_Export tmp/fos.doc --outdir tmp/", shell=True)
				proc.wait()
			#копируем файл с ФОС
			copyfileWithCheck(namefile,'tmp/fos1.pdf', rpdname)
			if(nofirstpage):
				#если первой страницы нет, то надо просто объединить
				proc = subprocess.Popen("qpdf --empty --pages tmp/fos.pdf tmp/fos1.pdf -- \""+fileout+'"',shell=True)
				proc.wait()
			else:
				# если первая страница есть, то надо просто выделить все страницы без нее
				proc = subprocess.Popen("qpdf tmp/fos1.pdf --pages . 2-z -- tmp/fos2.pdf",shell=True)
				proc.wait()
				#и объеденить файлы
				proc = subprocess.Popen("qpdf --empty --pages tmp/fos.pdf tmp/fos2.pdf -- \""+fileout+'"',shell=True)
				proc.wait()
	else:
		print('нет файла для ' + rpdname)

def cleantmp():
	proc = subprocess.Popen("rm tmp/*.pdf", shell=True)
	proc.wait()
	proc = subprocess.Popen("rm tmp/*.doc", shell=True)
	proc.wait()
