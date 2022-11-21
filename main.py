from sqlite3 import IntegrityError
import PySimpleGUI as sg
from globals import controller


BLANK_SPACE = ''
# ----------- Creamos los elementos que vamos a mostrar en los layouts-----------
yearsNameList = []
controller.yearCombo(yearsNameList)
comboYear = sg.Combo(yearsNameList, default_value=yearsNameList[-1], key='-YEAR-')


treedata = sg.TreeData()
controller.loadYearsTree(treedata)


# ------------------ Creamos los layouts que vamos a usar ------------------

layoutMenu = [[sg.Text('Gestion academica')]]


layoutCreate = [[comboYear],
           [sg.Button('Crear Alumno')],
           [sg.Button('Importar desde archivo de texto'),],
           [sg.Text('------------------')],
           [sg.Button('Crear Profesor')],
           [sg.Button('Crear Asignatura')],
           ]


layoutImport = [[sg.Text('Curso'),sg.Combo(values=['############'], key='-IMGRP-')],
                [sg.Input(key="-BROWS-"), sg.FileBrowse(key="-BROWS-")],
                [sg.Button('Importar')]]


layoutStudent = [[sg.Text('Inserte los datos del alumno')],
           [sg.Text('DNI'), sg.Input(key='-DNI-')],
           [sg.Text('Nombre'),sg.Input(key='-NAMES-')],
           [sg.Text('Apellido'),sg.Input(key='-SURNS-')],
           [sg.Text('Direccion'),sg.Input(key='-DIR-')],
           [sg.Text('Telefono'),sg.Input(key='-TELS-')],
           [sg.Text('Curso'),sg.Combo(values=['############'], key='-GRP-')],
           [sg.Button('Guardar Alumno')]]


layoutProf = [[sg.Text('Inserte los datos del profesor')],
           [sg.Text('Nombre'),sg.Input(key='-NAMEP-')],
           [sg.Text('Apellido'),sg.Input(key='-SURNP-')],
           [sg.Text('Telefono'),sg.Input(key='-TELP-')],
           [sg.Button('Guardar Profesor')]]


layoutCourse = [[sg.Text('Inserte asignatura')],
           [sg.Text('Nombre'),sg.Input(key='-COUR-')],
           [sg.Button('Guardar Asignatura')]]


layoutSearch = [[sg.Tree(treedata, ['Identificador', 'Nombre', 'Apellido', 'Direccion', 'Telefono'], 
                num_rows=15, col_widths=150, key=('-TREE-'))],
                [sg.Button('Refrescar')],]


# ----------- Creamos el layout principal usando Column
layout = [[sg.Column(layoutMenu, key='-COL1-'),
           sg.Column(layoutCreate, visible=False, key='-COL2-'),
           sg.Column(layoutSearch, visible=False, key='-COL3-'),
           sg.Column(layoutStudent, visible=False, key='-COL4-'),
           sg.Column(layoutProf, visible=False, key='-COL5-'),
           sg.Column(layoutCourse, visible=False, key='-COL6-'),
           sg.Column(layoutImport, visible=False, key='-COL7-')
          ],
          [sg.Button('Insertar'), sg.Button('Buscar'), sg.Button('Volver al menú'), 
          sg.Text('Operación realizada con éxito', key='-RES-', visible=False)]]

window = sg.Window('Swapping the contents of a window', layout)

layout = 1  # El layout visible al comienzo
while True:
    event, values = window.read()
    print(event, values)
    window['-RES-'].update(visible=False)
    if event in (None, 'Exit'):
        break
    if event == 'Insertar':
        window[f'-COL{layout}-'].update(visible=False)
        layout = 2
        window[f'-COL{layout}-'].update(visible=True)
    elif event == 'Buscar':
        window[f'-COL{layout}-'].update(visible=False)
        layout = 3
        window[f'-COL{layout}-'].update(visible=True)
    elif event == 'Crear Alumno':
        if values['-YEAR-'] not in controller.getYears().yearsDict.keys():
            sg.popup('Asegúrese de seleccionar un curso académico')
        else:
            window[f'-COL{layout}-'].update(visible=False)
            layout = 4
            window[f'-COL{layout}-'].update(visible=True)
            auxlist = controller.getGroupsNameForYear(values['-YEAR-'])
            window['-GRP-'].update(values=auxlist)
    elif event == 'Crear Profesor':
        window[f'-COL{layout}-'].update(visible=False)
        layout = 5
        window[f'-COL{layout}-'].update(visible=True)
    elif event == 'Crear Asignatura':
        window[f'-COL{layout}-'].update(visible=False)
        layout = 6
        window[f'-COL{layout}-'].update(visible=True)

    elif event == 'Volver al menú':
        window[f'-COL{layout}-'].update(visible=False)
        layout = 1
        window[f'-COL{layout}-'].update(visible=True)
    elif event == 'Guardar Alumno':
        auxlist = controller.getGroupsNameForYear(values['-YEAR-'])
        if BLANK_SPACE not in (values['-GRP-'], values['-DNI-'], values['-NAMES-'],
                               values['-SURNS-'], values['-DIR-'], values['-TELS-']) \
           and values['-GRP-'] in auxlist:
            try:
                controller.saveStudent(values['-YEAR-'],
                values['-GRP-'],
                values['-DNI-'],
                values['-NAMES-'],
                values['-SURNS-'],
                values['-DIR-'],
                values['-TELS-'],)
                window['-RES-'].update(visible=True)
            except IntegrityError:
                sg.popup('Error de integridad, revise los DNI')    
        else:
            sg.popup('Asegúrese de rellenar todos los campos correctamente')
    elif event == 'Guardar Profesor':
        if BLANK_SPACE not in (values['-NAMEP-'], values['-SURNP-'], values['-TELP-']):
            controller.saveProfessor(
            values['-NAMEP-'],
            values['-SURNP-'],
            values['-TELP-'],)
            window['-RES-'].update(visible=True)
        else:
            sg.popup('Asegúrese de rellenar todos los campos')
    elif event == 'Guardar Asignatura':
        if BLANK_SPACE not in (values['-COUR-']):
            controller.saveCourse(values['-COUR-'],)
            window['-RES-'].update(visible=True)
        else:
            print(values['-COUR-'])
            sg.popup('Asegúrese de rellenar todos los campos')
    elif event == 'Refrescar':
        treedata = sg.TreeData()
        treedata = controller.loadYearsTree(treedata)
        window['-TREE-'].update(treedata)
    elif event == 'Importar desde archivo de texto':
        if values['-YEAR-'] not in controller.getYears().yearsDict.keys():
            sg.popup('Asegúrese de seleccionar un curso académico')
        else:
            window[f'-COL{layout}-'].update(visible=False)
            layout = 7
            window[f'-COL{layout}-'].update(visible=True)
            auxlist = controller.getGroupsNameForYear(values['-YEAR-'])
            window['-IMGRP-'].update(values=auxlist)
    elif event == 'Importar':        
        auxlist = controller.getGroupsNameForYear(values['-YEAR-'])
        if  values['-IMGRP-'] not in auxlist or \
            BLANK_SPACE == values['-BROWS-']:
            sg.popup('Rellen los datos apropiadamente')
        else:
            try:
                controller.importStudentsFromFile(values['-BROWS-'],values['-IMGRP-'], values['-YEAR-'] )
                window['-RES-'].update(visible=True)
            except FileNotFoundError:
                sg.popup('Archivo no encontrado')
            except IntegrityError:
                sg.popup('Alumnos ya registrados en este año')
window.close()
