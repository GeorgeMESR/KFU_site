import kpfudatabase
#требуется установленные libreoffice, qpdf и inkscape

#Параметры, которые надо поменять
Shifr='03.03.03'
NameCom='Радиофизика'
Name='Квантовая и СВЧ электроника'
NameShort='КиСВЧэ'
Kvalif='бакалавр'
year='2022' # год за который РПД надо скопировать
nsem=8
namefileOP='plan.csv'

RPD=kpfudatabase.GetPlan(namefileOP,nsem)
kpfudatabase.GetAuthors('authors.txt',RPD)




for irpd in range(len(RPD)):
	namerpd = RPD[irpd]['name']
	print(namerpd)
	kpfudatabase.cleantmp()
	namefile = 'step3/' + kpfudatabase.makeRPDfilename(RPD[irpd]['shifr'], RPD[irpd]['name'], Shifr, NameShort,year) + '.pdf'
	namefileout = 'step5/' + kpfudatabase.makeRPDfilename(RPD[irpd]['shifr'], RPD[irpd]['name'], Shifr, NameShort,'2021') + '.pdf'
	namefileFOS = 'step3/' + kpfudatabase.makeRPDfilename(RPD[irpd]['shifr'], RPD[irpd]['name'], Shifr, NameShort,year) + '_ФОС.pdf'
	namefileoutFOS= 'tmp/foscopy.pdf'
	if(RPD[irpd]['rpdstate']=='document is ready' or RPD[irpd]['rpdstate'] == 'document for approval' or RPD[irpd]['rpdstate'] == 'error in document'):
		#Первая страница документа не с тем годом и печатью, РПД или на согласовании или вернули с ошибками - главное ФОС есть
		# сначала меняем первую страницу ФОС, а то там часто и год не тот и профиль другой
		kpfudatabase.changefirstpageFOS(namefileFOS, RPD[irpd]['name'], RPD[irpd]['shifr'], namefileoutFOS, '2021',Shifr, NameCom,Name,Kvalif, False)
		# затем меняем первую страницу в РПД и включаем ФОС в РПД
		kpfudatabase.changefirstpageRPD(namefile, namefileoutFOS, RPD[irpd]['name'], RPD[irpd]['shifr'], namefileout, '2021',Shifr, NameCom,Name,Kvalif)
	if ( RPD[irpd]['rpdstate'] == 'To write'):
		#Фоса нет просто подменяем первую страницу
		kpfudatabase.changefirstpageRPD(namefile, '', RPD[irpd]['name'], RPD[irpd]['shifr'], namefileout, '2021',Shifr, NameCom,Name,Kvalif)

