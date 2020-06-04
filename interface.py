import PySimpleGUI as sg
import init
import event_driven as ed

layout = [[sg.Button('Info')],
          [sg.Button('Pyramid')],
          [sg.Button('Brown')],
          [sg.Button('Diffusion')],
          [sg.Text('Your: '), sg.InputText(key='-FILE-'), sg.FileBrowse()],
          [sg.Button('Start'), sg.Exit()]]

win1 = sg.Window('Prog', layout)

while True:
    start = False
    event1, values = win1.read()
    if event1 is None or event1 == 'Exit':
        break

    elif event1 == 'Info':
        str = ' "Pyramid" - симуляция разбиения бильярдной пирамиды, \n' \
              ' "Brown" - симялиция движения броуновской частицы, \n' \
              ' "Diffusion" - симуляция диффузионного потока газа через отверстие, \n' \
              ' Файловый ввод данных для симуляции через строку напротив "Your" \n' \
              ' или через "Browse". \n' \
              '--Формат даных-- \n' \
              'Первой строкой вводим рзмер окна (разделитель - пробел), далее по строке на шар\n' \
              '/вес/ /диаметр/ /координата х/ /координата у/ /скорсть по х/ /скорость по у/\n' \
              'Все значения - вещественные числа, десятичный разделитель - "."'
        sg.Popup(str)
    elif event1 == 'Start':
        balls, timestep, size = init.user_input(values['-FILE-'])
        start = True
    elif event1 == 'Pyramid':
        balls, timestep, size = init.preset_pyramid()
        start = True
    elif event1 == 'Brown':
        balls, timestep, size = init.preset_brown()
        start = True
    elif event1 == 'Diffusion':
        balls, timestep, size = init.preset_diffusion()
        start = True

    if start and timestep == None:
        sg.Popup('Шары пересекаются друг с другом или выходят за границы области')

    elif start:
        win1.Hide()

        layout2 = [[sg.Graph(size, (0, 0), size, 'black', key='graph')],
                   [sg.Exit()]]
        win2 = sg.Window('Draw', layout2)
        win2.Finalize()

        graph = win2['graph']

        simulation = ed.start_simulation(size, graph, balls)

        while True:
            ev2, val2 = win2.read(timeout=1)
            if ev2 == '__TIMEOUT__':

                ed.simulation_move(simulation, timestep, size, graph, balls)



            elif ev2 is None or ev2 == 'Exit':
                win2.close()
                win2_act = False
                win1.UnHide()
                break


