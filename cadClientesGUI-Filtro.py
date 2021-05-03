import sqlite3 #biblio for use DB
import PySimpleGUI as sg #biblio for (GUI)
##################################################

# conecting...
conn = sqlite3.connect('clientes.db')
# def a cursor
cursor = conn.cursor()

# Creating the Table (schema)
cursor.execute("""CREATE TABLE IF NOT EXISTS clientes (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	nome TEXT NOT NULL,
	idade INTEGER,
	cpf	VARCHAR(11) NOT NULL,
	email TEXT,
	fone TEXT,
	cidade TEXT,
	uf VARCHAR(2));""")

##################################################

# Creating the GUI
sg.theme('Tan Blue')   #Choosing a theme
# Desingn of the window1.
layout = [  [sg.Text('Nome:', size=(6, 1)), sg.InputText(size=(32,1), key='-NOME-')],
            [sg.Text('Idade:', size=(6, 1)), sg.InputText(size=(32,1), key='-IDADE-')],
            [sg.Text('CPF:', size=(6, 1)), sg.InputText(size=(32,1), key='-CPF-', enable_events = True)],
            [sg.Text('e-mail:', size=(6, 1)), sg.InputText(size=(32,1), key='-EMAIL-')],
            [sg.Text('Fone:', size=(6, 1)), sg.InputText(size=(32,1), key='-FONE-', enable_events = True)],
            [sg.Text('Cidade:', size=(6, 1)), sg.InputText(size=(32,1), key='-CIDADE-')],
            [sg.Text('UF:', size=(6, 1)), sg.InputText(size=(32,1), key='-UF-')],
            [ sg.Button('Cadastrar', button_color = 'black on orange', font = ['Comics', 12]), 
            sg.Button('Sair', button_color = 'black on red', font = ['Comics', 12]),
            sg.Button('Ver Registros', button_color = 'black on green', font = ['Comics', 12]) ] ]

# Creating the window1
window1 = sg.Window('Cadastro de Clientes', layout, finalize = True)
window2_active = False

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event1, values1 = window1.read()
    # if user closes window or clicks exit
    if event1 == sg.WIN_CLOSED or event1 == 'Sair':
        break

    if event1 == '-CPF-' and values1['-CPF-'] and values1['-CPF-'][-1] not in ('0123456789'):
        window1['-CPF-'].update(values1['-CPF-'][:-1])
        sg.popup('Apenas números são permitidos no campo CPF!')

    if event1 == '-FONE-' and values1['-FONE-'] and values1['-FONE-'][-1] not in ('0123456789()-'):
        window1['-FONE-'].update(values1['-FONE-'][:-1])
        sg.popup('Apenas números são permitidos\n ou o modelo (xx)xxxxx-xxxx')
    
    if event1 == 'Cadastrar':
        nome, cpf = values1['-NOME-'], values1['-CPF-']
        if len(nome) == 0 or len(cpf) == 0:
            sg.popup('Os campos Nome e CPF são obrigatórios!')
        else:
            try:
                #input data in table
                cursor.execute("""INSERT INTO clientes (nome, idade, cpf, email, fone, cidade, uf)
                VALUES (?,?,?,?,?,?,?)""", (values1['-NOME-'], values1['-IDADE-'], values1['-CPF-'], 
                values1['-EMAIL-'], values1['-FONE-'], values1['-CIDADE-'], values1['-UF-']))
                conn.commit() #NEVER FORGET THIS COMAND
                sg.popup('Cliente cadastrado com sucesso!')
                window1['-NOME-'].update('')
                window1['-IDADE-'].update('')
                window1['-CPF-'].update('')
                window1['-EMAIL-'].update('')
                window1['-FONE-'].update('')
                window1['-CIDADE-'].update('')
                window1['-UF-'].update('')
            except E as Argument:
                print(f'Erro ao gravar os dados:\n{E}')

    if event1 == 'Ver Registros' and not window2_active:
        window2_active = True
        window1.Hide()
        
        layout2 = [ [sg.Text('TIPO DE FILTRO', font=('Helvetica', 14), justification='left')],
                    [sg.Radio('Nome', 'loss', default=True, size=(5, 1), font = ['Comics', 14]), 
                    sg.Radio('CPF', 'loss', size=(5, 1), font = ['Comics', 14])],
                    [sg.Text('Busca:', size=(5, 1), font = ['Comics', 13]), sg.InputText(size=(40,1), key='-BUSCA-', font = ['Comics', 13]), sg.Button('Filtrar', button_color = 'black on light blue', font = ['Comics', 12])],
                    [sg.MLine(key='-ML1-'+sg.WRITE_ONLY_KEY, size=(80,15), font='Any 13')],
                    [sg.Button('Sair', button_color = 'black on red', font = ['Comics', 12])] ]
                    
        window2 = sg.Window('Ver/Filtrar Registros', layout2, finalize = True)
        
        #Filling in before showing
        window2['-ML1-'+sg.WRITE_ONLY_KEY].print('\nOS DADOS SALVOS NO BANCO DE DADOS SÃO:\n', text_color='yellow', background_color='black')
        cursor.execute("""SELECT * FROM clientes;""")
        for i, linha in enumerate(cursor.fetchall()):
            if i % 2 == 0:
                window2['-ML1-'+sg.WRITE_ONLY_KEY].print(linha, text_color='black', background_color='light yellow')
            else:
                window2['-ML1-'+sg.WRITE_ONLY_KEY].print(linha, text_color='black', background_color='light blue')
        
        #Loop for window2
        tipoBusca = True
        while True:
            event2, values2 = window2.read()
            if event2 == sg.WIN_CLOSED or event2 == 'Sair':
                window2.Close()
                window2_active = False
                window1.UnHide()
                break

            if event2 == 'Nome':
                tipoBusca = True
            if event2 == 'CPF':
                tipoBusca = False

            if event2 == 'Filtrar' and tipoBusca:    
                #window2.FindElement('-ML1-').Update(value = '') #I can't clear the multiline =(
                cursor.execute(f"""SELECT * FROM clientes WHERE nome LIKE '{values2['-BUSCA-']}%';""")
                for i, linha in enumerate(cursor.fetchall()):
                    if i % 2 == 0:
                        window2['-ML1-'+sg.WRITE_ONLY_KEY].print(linha, text_color='black', background_color='light yellow')
                    else:
                        window2['-ML1-'+sg.WRITE_ONLY_KEY].print(linha, text_color='black', background_color='light blue')
            
            if event2 == 'Filtrar' and not tipoBusca:    
                #window2.FindElement('-ML1-').Update(value = '') #I can't clear the multiline =(
                cursor.execute(f"""SELECT * FROM clientes WHERE cpf LIKE '{values2['-BUSCA-']}%';""")
                for i, linha in enumerate(cursor.fetchall()):
                    if i % 2 == 0:
                        window2['-ML1-'+sg.WRITE_ONLY_KEY].print(linha, text_color='black', background_color='light yellow')
                    else:
                        window2['-ML1-'+sg.WRITE_ONLY_KEY].print(linha, text_color='black', background_color='light blue')
conn.close() # desconecting DB
window1.close()
##################################################

