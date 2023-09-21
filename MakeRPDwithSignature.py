import kpfudatabase
#требуется установленные libreoffice, qpdf


#Параметры, которые надо поменять
Shifr='03.03.03' # шифр направления
NameCom='Радиофизика' # название направления
Name='Квантовая и СВЧ электроника' # профиль
NameShort='КиСВЧэ' # профиль сокращенное название для имен файлов и т.п.
Kvalif='бакалавр' # квалификация выпускников
year='2023' # год поступления
nsem=8 # число учебных семестров (8 бакалавриат, 4 магистратура)
namefileOP='plan.csv' # имя файла с базой данных

RPD=kpfudatabase.GetPlan(namefileOP,nsem)
kpfudatabase.GetAuthors('authors.txt',RPD)




for irpd in range(len(RPD)):
	namerpd = RPD[irpd]['name']
	print(namerpd)
	kpfudatabase.cleantmp()
	namefile = 'step3/' + kpfudatabase.makeRPDfilename(RPD[irpd]['shifr'], RPD[irpd]['name'], Shifr, NameShort,year) + '.pdf'
	namefileout = 'step4/' + kpfudatabase.makeRPDfilename(RPD[irpd]['shifr'], RPD[irpd]['name'], Shifr, NameShort,year) + '.pdf'
	namefileFOS = 'step3/' + kpfudatabase.makeRPDfilename(RPD[irpd]['shifr'], RPD[irpd]['name'], Shifr, NameShort,year) + '_ФОС.pdf'
	namefileoutFOS= 'tmp/foscopy.pdf'
	if(RPD[irpd]['rpdstate']=='document is ready'):
		#Документ готов, надо лишь объединить РПД и ФОС
		# сначала меняем первую страницу ФОС, а то там часто и год не тот и профиль другой
		kpfudatabase.changefirstpageFOS(namefileFOS, RPD[irpd]['name'], RPD[irpd]['shifr'], namefileoutFOS, year,Shifr, NameCom,Name,Kvalif, False)
		#объединяем
		kpfudatabase.InsertFOSOnly(namefile, namefileoutFOS, RPD[irpd]['name'], namefileout)
	if ( RPD[irpd]['rpdstate'] == 'document for approval' or RPD[irpd]['rpdstate'] == 'error in document' or irpd==41):
		#Первая страница документа без печати, но он или на согласовании или вернули с ошибками - главное ФОС есть
		# сначала меняем первую страницу ФОС, а то там часто и год не тот и профиль другой
		kpfudatabase.changefirstpageFOS(namefileFOS, RPD[irpd]['name'], RPD[irpd]['shifr'], namefileoutFOS, year, Shifr, NameCom,Name,Kvalif, False)
		# затем меняем первую страницу в РПД и включаем ФОС в РПД
		kpfudatabase.changefirstpageRPD(namefile, namefileoutFOS, RPD[irpd]['name'], RPD[irpd]['shifr'], namefileout, year,Shifr, NameCom,Name,Kvalif)
	if ( RPD[irpd]['rpdstate'] == 'To write' and irpd!=41):
		#Фоса нет просто подменяем первую страницу
		kpfudatabase.changefirstpageRPD(namefile, '', RPD[irpd]['name'], RPD[irpd]['shifr'], namefileout, year,Shifr, NameCom,Name,Kvalif)

