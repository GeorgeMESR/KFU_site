import os
import urllib.request
import time
import socket
import kpfudatabase


#Параметры, которые надо поменять
Shifr='03.03.03'
NameCom='Радиофизика'
Name='Квантовая и СВЧ электроника'
NameShort='КиСВЧэ'
Kvalif='бакалавр'
year='2022'
nsem=8
namefileOP='plan.csv'


socket.setdefaulttimeout(15)
def DownloadUrl(url, namefile):
	try:
		os.remove(namefile)
	except:
		pass
	for i in range(10):
		try:
			urllib.request.urlretrieve(url, namefile)
			return
		except:
			time.sleep(2)
	print('cannot download URL %s in file %s' %(url, namefile))


RPD=kpfudatabase.GetPlan(namefileOP,nsem)
kpfudatabase.GetAuthors('authors.txt',RPD)

getwebpar1=['p1','p_menu','p2','p_study_plan','p_h','p_content']


for irpd in range(len(RPD)):
	if(RPD[irpd]['shifr'][0:2]=='Б2' or RPD[irpd]['shifr'][0:2]=='Б3'):
		continue
	if(RPD[irpd]['rpdstateIndx']==''):
		continue
	print('get ' + RPD[irpd]['name'])
	mainurl="https://shelly.kpfu.ru/pls/student/discipline_programs.program_form?"+RPD[irpd]['rpdstateIndx']
	name="tmp/tmp.html"
	name1 = "tmp/tmp1.html"
	# Скачиваем первую страничку
	DownloadUrl(mainurl, name)
	with (open(name, 'r', encoding='cp1251') as ftmp):
		l=ftmp.read()
		ftmp.close()
		sathstr='<select name="p_author" size="3" multiple style="width:500px">'
		i=l.find(sathstr)
		if(i!=-1):
			sa1=l[i+len(sathstr):len(l)].strip()
			k=sa1.find("</select>")
			if(k!=-1):
				sa1=sa1[0:k]
				for iath in range(5):
					js=sa1.find("<option value=")
					jf=sa1.find("</option>")
					if(js!=-1 and jf!=-1):
						sa2=sa1[js+len("<option value="):jf]
						sa1=sa1[jf+len("</option>"):len(sa1)]
						j = sa2.find(">")
						if(j!=-1):
							FIO=sa2[j+1:k]
							title=''
							placeofwork=''
							if 'author' in RPD[irpd]:
								RPD[irpd]['author'].append({'FIO': FIO, 'title': title, 'placeofwork': placeofwork})
							else:
								RPD[irpd]['author'] = [{'FIO': FIO, 'title': title, 'placeofwork': placeofwork}]
					else:
						break
			i=l.find('<a href="#tabs-13"')
			if(i!=-1):
				sp=l[i+len('<a href="#tabs-13" onclick="self.location=\''):len(l)]
				j=sp.find('\'"')
				if(j!=-1):
					mainurl1='https://shelly.kpfu.ru/pls/student/'+sp[0:j].strip()
					# Скачиваем страничку 6.3
					DownloadUrl(mainurl1, name1)
			i=l.find('<a  download=')
			if(i!=-1):
				sa1=l[i+len('<a  download='):len(l)].strip()
				k=sa1.find('href="')
				if(k!=-1):
					sa1=sa1[k+len('href="'):len(l)]
					j=sa1.find('">')
					if(j!=-1):
						sa1 = sa1[0:j]
						# скачиваем файл doc
						s="https://shelly.kpfu.ru/pls/student/"+sa1
						namefile='step3/'+kpfudatabase.makeRPDfilename( RPD[irpd]['shifr'],RPD[irpd]['name'],Shifr, NameShort, year)
						DownloadUrl(s, namefile + ".html")
						s="https://html2pdf.kpfu.ru/convert.php?url=https://shelly.kpfu.ru/pls/student/"+sa1.replace("&",'%26')+"%26p_pdf=1"
						DownloadUrl(s, namefile + ".pdf")
		#открываем страницу с 6.3 и ищем там ФОС
		with open(name1, 'r', encoding='cp1251') as ftmp:
			l=ftmp.read()
			ftmp.close()
			i=l.find('<a target="_blank"')
			if(i!=-1):
				sp=l[i+len('<a target="_blank" style="color: #00599B;" href="'):len(l)]
				j=sp.find('"')
				if(j!=-1):
					mainurl2=sp[0:j].strip()
					namefile = 'step3/' + kpfudatabase.makeRPDfilename(RPD[irpd]['shifr'], RPD[irpd]['name'], Shifr, NameShort, year)+'_ФОС.pdf'
					#скачиваем ФОС
					DownloadUrl(mainurl2, namefile)

#сохраняем информацию об авторах
with open('authors.txt', 'w', encoding='utf-8') as f2:
	for irpd in range(len(RPD)):
		if (('author' in RPD[irpd])):
			s=''
			for a in RPD[irpd]['author']:
				s+=a['FIO']+'#'+a['title']+'#'+a['placeofwork']+';'
			f2.write(RPD[irpd]['shifr']+'\t'+s+'\n')
		else:
			f2.write(RPD[irpd]['shifr'] +'\t'+ 'None'+'\t'+ 'None'+'\t'+ 'None' + '\n')
	f2.close()

