import sqlite3 #biblioteca para banco de dados
import PySimpleGUI as sg #biblioteca para interface (GUI)
##################################################

# conectando...
conn = sqlite3.connect('clientes.db')
# definindo um cursor
cursor = conn.cursor()

# criando a tabela (schema)
cursor.execute("""CREATE TABLE IF NOT EXISTS clientes (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	nome TEXT NOT NULL,
	idade INTEGER,
	cpf	VARCHAR(11) NOT NULL,
	email TEXT NOT NULL,
	fone TEXT,
	cidade TEXT,
	uf VARCHAR(2) NOT NULL);""")

##################################################

# criando a janela (GUI)
sg.theme('Tan Blue')   # Definindo um tema para a janela
# Desingn da janela.
layout = [  [sg.Text('Nome:', size=(6, 1)), sg.InputText(size=(30,1), key='-NOME-')],
            [sg.Text('Idade:', size=(6, 1)), sg.InputText(size=(30,1), key='-IDADE-')],
            [sg.Text('CPF:', size=(6, 1)), sg.InputText(size=(30,1), key='-CPF-')],
            [sg.Text('e-mail:', size=(6, 1)), sg.InputText(size=(30,1), key='-EMAIL-')],
            [sg.Text('Fone:', size=(6, 1)), sg.InputText(size=(30,1), key='-FONE-')],
            [sg.Text('Cidade:', size=(6, 1)), sg.InputText(size=(30,1), key='-CIDADE-')],
            [sg.Text('UF:', size=(6, 1)), sg.InputText(size=(30,1), key='-UF-')],
            [ sg.Button('Cadastrar', button_color = 'black on orange', font = ['Comics', 12]), 
            sg.Button('Sair', button_color = 'black on red', font = ['Comics', 12]),
            sg.Button('Ver Registros', button_color = 'black on green', font = ['Comics', 12]) ] ]

# Criando a janela
window1 = sg.Window('Cadastro de Clientes', layout)
window2_active = False

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event1, values1 = window1.read()
    # if user closes window or clicks exit
    if event1 == sg.WIN_CLOSED or event1 == 'Sair':
        break
    if event1 == 'Cadastrar':
        try:
            # inserindo dados na tabela
            cursor.execute("""INSERT INTO clientes (nome, idade, cpf, email, fone, cidade, uf)
            VALUES (?,?,?,?,?,?,?)""", (values1['-NOME-'], values1['-IDADE-'], values1['-CPF-'], 
            values1['-EMAIL-'], values1['-FONE-'], values1['-CIDADE-'], values1['-UF-']))
            conn.commit() #NUNCA ESQUECER ESSE COMANDO
            sg.popup('Cliente cadastrado com sucesso!')
            window1['-NOME-'].update('')
            window1['-IDADE-'].update('')
            window1['-CPF-'].update('')
            window1['-EMAIL-'].update('')
            window1['-FONE-'].update('')
            window1['-CIDADE-'].update('')
            window1['-UF-'].update('')
        except E:
            print(E)
    if event1 == 'Ver Registros' and not window2_active:
        window2_active = True
        window1.Hide()
        
        # SEMPRE CRIAR LAYOUT NOVO, NUNCA REUTILIZAR
        layout2 = [ [sg.Text('TIPO DE FILTRO', font=('Helvetica', 14), justification='left')],
                    [sg.Radio('Nome', 'loss', default=True, size=(5, 1)), 
                    sg.Radio('CPF', 'loss', size=(5, 1))],
                    [sg.Text('Busca:', size=(6, 1)), sg.InputText(size=(40,1), key='-BUSCA-', enable_events=True)],
                    [sg.MLine(key='-ML1-'+sg.WRITE_ONLY_KEY, size=(80,15), font='Any 13')],
                    [sg.Button('Sair', button_color = 'black on red', font = ['Comics', 12])] ]
                    
        window2 = sg.Window('Ver/Filtrar Registros', layout2, finalize=True)
        
        #Preenchendo na primeira execução
        window2['-ML1-'+sg.WRITE_ONLY_KEY].print('\nOS DADOS SALVOS NO BANCO DE DADOS SÃO:\n', text_color='yellow', background_color='black')
        cursor.execute("""SELECT * FROM clientes;""")
        for i, linha in enumerate(cursor.fetchall()):
            if i % 2 == 0:
                window2['-ML1-'+sg.WRITE_ONLY_KEY].print(linha, text_color='black', background_color='light yellow')
            else:
                window2['-ML1-'+sg.WRITE_ONLY_KEY].print(linha, text_color='black', background_color='light blue')
        
        #Laço da segunda janela    
        while True:
            event2, values2 = window2.read()
            if event2 == sg.WIN_CLOSED or event2 == 'Sair':
                window2.Close()
                window2_active = False
                window1.UnHide()
                break
            if values2['-BUSCA-']:    # if something is highlighted in the list
                #window2.FindElement('-ML1-').Update('')
                cursor.execute(f"""SELECT * FROM clientes WHERE nome LIKE '{values2['-BUSCA-']}%';""")
                for i, linha in enumerate(cursor.fetchall()):
                    if i % 2 == 0:
                        window2['-ML1-'+sg.WRITE_ONLY_KEY].print(linha, text_color='black', background_color='light yellow')
                    else:
                        window2['-ML1-'+sg.WRITE_ONLY_KEY].print(linha, text_color='black', background_color='light blue')
conn.close() # desconectando do banco de dados...
window1.close()
##################################################
