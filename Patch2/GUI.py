import sys
import glob
import serial 
import time
import datetime
import PySimpleGUI as sg
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def empty_window(): #If no proper devices are plugged in opens empty window with option to scan again
    layout = [[sg.Text("No plants available")], [sg.Button("Try again")]]
    window = sg.Window("Doniczujniczka_pusta", layout)
    while True:
        event, values = window.read()
        if event == "Try again":
            window.close()
            search_ports()
        if event == sg.WIN_CLOSED:
            break
    window.close()

def read_and_calc(one_port): #Need for updates of water and sun stats
    arduino = serial.Serial(one_port, 115200, timeout=0.1)
    n = 0
    while not n:
        test = arduino.readline().decode()
        time.sleep(0.1)
        if test:
            n = 1
    phrase, water, sun, = test.split(" ")
    water = float(water) * 100
    sun = float(sun) * 100
    print(f"Water level: {water}%, Sunbathing: {sun}%")
    arduino.write('Jump in!'.encode('utf-8')) #Sends signal to arduino to light up the LED

    return water, sun

def check_if_correct(one_port): #Check if devices plugged in will be working with GUI
    arduino = serial.Serial(one_port, 115200, timeout=0.1)
    n = 0
    while not n:
        test = arduino.readline().decode()
        time.sleep(0.1)
        if test:
            n = 1
    if len(test.split(" ")) == 3: #Water and sun signal should have length equal to 3
        phrase, water, sun, = test.split(" ")
        if phrase == 'water_and_sun':
            water = float(water) * 100
            sun = float(sun) * 100
            return water, sun
        else:
            return []   
    elif len(test.split(" ")) == 2: #Fertilizer signal should have length equal to 2
        phrase, pH_level, = test.split(" ")
        
        if phrase == 'fertilizer':
            pH_level = float(pH_level)
            return [pH_level]
        else:
            return [] #Returns empty list causing refresh option in empty window
    else:
        return [] #Returns empty list causing refresh option in empty window
    
def pH_read_and_calc(pH_port): #Reads pH_reading from separate arduino
    arduino =serial.Serial(pH_port, 115200, timeout=0.1)
    arduino.write('Gimme pH!'.encode('utf-8'))
    n = 0
    while not n:
        test = arduino.readline().decode()
        time.sleep(0.1)
        if test:
            n = 1
    phrase, pH_level, = test.split(" ")
    if phrase == 'fertilizer':
        print(phrase)
        pH_level = float(pH_level)
        return pH_level

def write_data(one_port, water, sun):
    filename_water = 'water_from_' + one_port + '.txt'
    filename_sun = 'sun_from_' + one_port + '.txt'
    file_water = open(filename_water, 'a')
    file_sun = open(filename_sun, 'a')
    date_now = datetime.datetime.now().strftime("%x") + ' ' + datetime.datetime.now().strftime("%H") + ':' + datetime.datetime.now().strftime("%M")
    print(f"Data check!!! {datetime.datetime.now().strftime("%x")} {datetime.datetime.now().strftime("%X")}")
    file_water.write(f"{date_now}\t{water}\n")
    file_sun.write(f"{date_now}\t{sun}\n")
    file_water.close()
    file_sun.close()

def background(graph, figure):
    canvas = FigureCanvasTkAgg(figure, graph.Widget)
    plot_widget = canvas.get_tk_widget()
    plot_widget.pack(side='top', fill='both', expand=1)

def draw(filename, id_data):
    from datetime import datetime
    matplotlib.use("TkAgg")  
    
    fig = plt.figure(id_data)
    ax = plt.gca()

    fig.set_figheight(5)
    fig.set_figwidth(7)
    
    file = open(filename,'r')
    lines = file.readlines()
    x = [line.split("\t")[0] for line in lines]
    y = [float(line.split("\t")[1]) for line in lines]
    x = [datetime.strptime(i,"%m/%d/%y %H:%M") for i in x]

    ax.cla()
    ax.set_title(filename)
    ax.set_xlabel("Dates")
    #ax.set_ylabel("%")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y %H:%M'))
    #plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.plot(x,y)
    plt.gcf().autofmt_xdate()
    fig.canvas.draw()
    #return figure_canvas_agg

def search_ports(): #Searches all ports and sends them for check-up
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    All_ports = []
    List_ports = []
    pH_port = []
    
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            All_ports.append(port)
        except (OSError, serial.SerialException):
            pass
    print(All_ports)
    for i in range (len(All_ports)):
        if len(check_if_correct(All_ports[i])) == 2: #water and sun reading - adds to List_ports
            List_ports.append(All_ports[i])
        if len(check_if_correct(All_ports[i])) == 1: #pH_port reading
            pH_port = All_ports[i]

    if not len(List_ports):
        empty_window()
    if len(List_ports):
        window_creation(List_ports, pH_port)

def window_creation(List_ports, pH_port):
    
    water, sun = read_and_calc(List_ports[0])

    toggle_btn_off = b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAAED0lEQVRYCe1WTWwbRRR+M/vnv9hO7BjHpElMKSlpqBp6gRNHxAFVcKM3qgohQSqoqhQ45YAILUUVDRxAor2VAweohMSBG5ciodJUSVqa/iikaePEP4nj2Ovdnd1l3qqJksZGXscVPaylt7Oe/d6bb9/svO8BeD8vA14GvAx4GXiiM0DqsXv3xBcJU5IO+RXpLQvs5yzTijBmhurh3cyLorBGBVokQG9qVe0HgwiXLowdy9aKsY3g8PA5xYiQEUrsk93JTtjd1x3siIZBkSWQudUK4nZO1w3QuOWXV+HuP/fL85klAJuMCUX7zPj4MW1zvC0Ej4yMp/w++K2rM9b70sHBYCjo34x9bPelsgp/XJksZ7KFuwZjr3732YcL64ttEDw6cq5bVuCvgy/sje7rT0sI8PtkSHSEIRIKgCQKOAUGM6G4VoGlwiqoVd2Za9Vl8u87bGJqpqBqZOj86eEHGNch+M7otwHJNq4NDexJD+59RiCEQG8qzslFgN8ibpvZNsBifgXmFvJg459tiOYmOElzYvr2bbmkD509e1ylGEZk1Y+Ssfan18n1p7vgqVh9cuiDxJPxKPT3dfGXcN4Tp3dsg/27hUQs0qMGpRMYjLz38dcxS7Dm3nztlUAb38p0d4JnLozPGrbFfBFm79c8hA3H2AxcXSvDz7/+XtZE1kMN23hjV7LTRnKBh9/cZnAj94mOCOD32gi2EUw4FIRUMm6LGhyiik86nO5NBdGRpxYH14bbjYfJteN/OKR7UiFZVg5T27QHYu0RBxoONV9W8KQ7QVp0iXdE8fANUGZa0QAvfhhXlkQcmjJZbt631oIBnwKmacYoEJvwiuFgWncWnXAtuVBBEAoVVXWCaQZzxmYuut68b631KmoVBEHMUUrJjQLXRAQVSxUcmrKVHfjWWjC3XOT1FW5QrWpc5IJdQhDKVzOigEqS5dKHMVplnNOqrmsXqUSkn+YzWaHE9RW1FeXL7SKZXBFUrXW6jIV6YTEvMAUu0W/G3kcxPXP5ylQZs4fa6marcWvvZfJu36kuHjlc/nMSuXz+/ejxgqPFpuQ/xVude9eu39Jxu27OLvBGoMjrUN04zrNMbgVmOBZ96iPdPZmYntH5Ls76KuxL9NyoLA/brav7n382emDfHqeooXyhQmARVhSnAwNNMx5bu3V1+habun5nWdXhwJZ2C5mirTesyUR738sv7g88UQ0rEkTDlp+1wwe8Pf0klegUenYlgyg7bby75jUTITs2rhCAXXQ2vwxz84vlB0tZ0wL4NEcLX/04OrrltG1s8aOrHhk51SaK0us+n/K2xexBxljcsm1n6x/Fuv1PCWGiKOaoQCY1Vb9gWPov50+fdEqd21ge3suAlwEvA14G/ucM/AuppqNllLGPKwAAAABJRU5ErkJggg=='
    toggle_btn_on = b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAAD+UlEQVRYCe1XzW8bVRCffbvrtbP+2NhOD7GzLm1VoZaPhvwDnKBUKlVyqAQ3/gAkDlWgPeVQEUCtEOIP4AaHSI0CqBWCQyXOdQuRaEFOk3g3IMWO46+tvZ+PeZs6apq4ipON1MNafrvreTPzfvub92bGAOEnZCBkIGQgZOClZoDrh25y5pdjruleEiX+A+rCaQo05bpuvJ/+IHJCSJtwpAHA/e269g8W5RbuzF6o7OVjF8D3Pr4tSSkyjcqfptPDMDKSleW4DKIggIAD5Yf+Oo4DNg6jbUBlvWLUNutAwZu1GnDjzrcXzGcX2AHw/emFUV6Sfk0pqcKpEydkKSo9q3tkz91uF5aWlo1Gs/mYc+i7tz4//19vsW2AU9O381TiioVCQcnlRsWeQhD3bJyH1/MiFLICyBHiuzQsD1arDvypW7DR9nzZmq47q2W95prm+I9fXfqXCX2AF2d+GhI98Y8xVX0lnxvl2UQQg0csb78ag3NjEeD8lXZ7pRTgftmCu4864OGzrq+5ZU0rCa3m+NzXlzvoAoB3+M+SyWQuaHBTEzKMq/3BMbgM+FuFCDBd9kK5XI5PJBKqLSev+POTV29lKB8rT0yMD0WjUSYLZLxzNgZvIHODOHuATP72Vwc6nQ4Uiw8MUeBU4nHS5HA6TYMEl02wPRcZBJuv+ya+UCZOIBaLwfCwQi1Mc4QXhA+PjWRkXyOgC1uIhW5Qd8yG2TK7kSweLcRGKKVnMNExWWBDTQsH9qVmtmzjiThQDs4Qz/OUSGTwcLwIQTLW58i+yOjpXDLqn1tgmDzXzRCk9eDenjo9yhvBmlizrB3V5dDrNTuY0A7opdndStqmaQLPC1WCGfShYRgHdLe32UrV3ntiH9LliuNrsToNlD4kruN8v75eafnSgC6Luo2+B3fGKskilj5muV6pNhk2Qqg5v7lZ51nBZhNBjGrbxfI1+La5t2JCzfD8RF1HTBGJXyDzs1MblONulEqPDVYXgwDIfNx91IUVbAbY837GMur+/k/XZ75UWmJ77ou5mfM1/0x7vP1ls9XQdF2z9uNsPzosXPNFA5m0/EX72TBSiqsWzN8z/GZB08pWq9VeEZ+0bjKb7RTD2i1P4u6r+bwypo5tZUumEcDAmuC3W8ezIqSGfE6g/sTd1W5p5bKjaWubrmWd29Fu9TD0GlYlmTx+8tTJoZeqYe2BZC1/JEU+wQR5TVEUPptJy3Fs+Vkzgf8lemqHumP1AnYoMZSwsVEz6o26i/G9Lgitb+ZmLu/YZtshfn5FZDPBCcJFQRQ+8ih9DctOFvdLIKHH6uUQnq9yhFu0bec7znZ+xpAGmuqef5/wd8hAyEDIQMjAETHwP7nQl2WnYk4yAAAAAElFTkSuQmCC'

    graphs_into_column = [[sg.Graph((100,150),(0,0),(100,150), key='-graph_water-')], [sg.Graph((100,150),(0,0),(100,150), key='-graph_sun-')],
    [sg.Graph((100,150),(0,0),(100,150), key='-graph_pH-')]]
    
    layout = [[sg.Text("Plant plugged in:")],
    [sg.Combo(List_ports, default_value = List_ports[0], size = (6, 6), readonly = True, key = '-dropdown-'), sg.Button("Refresh")],
    [sg.Text(f"Water level: {water}%", key = '-water-')],
    [sg.Text(f"Sunbathing: {sun}%", key = '-sun-')],
    [sg.Text('Day mode'), sg.Image(toggle_btn_off, key='-nightmode-', enable_events=True, metadata=False), sg.Text('Night mode')],
    [sg.Text("Fertilizer  level:", key = '-fertilizer-'), sg.Button("Check pH")],
    [sg.Column(graphs_into_column, size=(800, 700), scrollable = True, vertical_scroll_only = True)]]

    window = sg.Window("Doniczujniczka", layout, size=(800, 650), resizable=True, finalize=True)

    #write_data(List_ports[0], water, sun)
    
    fig1 = plt.figure(1)
    fig1.set_figheight(5)
    fig1.set_figwidth(7)
    ax1 = plt.subplot(111)
    
    fig2 = plt.figure(2)
    fig2.set_figheight(5)
    fig2.set_figwidth(7)
    ax2 = plt.subplot(111)
    
    fig3 = plt.figure(3)
    fig3.set_figheight(5)
    fig3.set_figwidth(7)
    ax3 = plt.subplot(111)
    
    background(window['-graph_water-'], fig1)
    background(window['-graph_sun-'], fig2)
    background(window['-graph_pH-'], fig3)
    
    draw(str('water_from_' + List_ports[0] + '.txt'), 1)
    draw(str('sun_from_' + List_ports[0] + '.txt'), 2)
    draw(str('fertilizer_from_' + List_ports[0] + '.txt'),3)

    while True:
        
        event, values = window.read(timeout=30000)
        print(f"Event: {event}")
    
        if event == "Refresh": #Refresh button
            water, sun = read_and_calc(values['-dropdown-'])
            if not window['-nightmode-'].metadata:
                write_data(values['-dropdown-'], water, sun)
                draw(str('water_from_' + values['-dropdown-'] + '.txt'),1)
                draw(str('sun_from_' + values['-dropdown-'] + '.txt'), 2)
                
            window['-water-'].update(f"Water level: {water}%")
            window['-sun-'].update(f"Sunbathing: {sun}%")
                
        if event == '__TIMEOUT__': #Auto refesh in timeout
            water, sun = read_and_calc(values['-dropdown-'])
            if not window['-nightmode-'].metadata:
                write_data(values['-dropdown-'], water, sun)
                draw(str('water_from_' + values['-dropdown-'] + '.txt'),1)
                draw(str('sun_from_' + values['-dropdown-'] + '.txt'), 2)
            window['-water-'].update(f"Water level: {water}%")
            window['-sun-'].update(f"Sunbathing: {sun}%")

        if event == '-nightmode-':
            window['-nightmode-'].metadata = not window['-nightmode-'].metadata
            window['-nightmode-'].update(toggle_btn_on if window['-nightmode-'].metadata else toggle_btn_off)

        if event == 'Check pH': #Reads pH stats if the reading device is available
            if len(pH_port):
                pH_level = pH_read_and_calc(pH_port)
                window['-fertilizer-'].update(f"Fertilizer  level: {pH_level}")
                
                filename_fertilizer = 'fertilizer_from_' + values['-dropdown-'] + '.txt'
                file_fertilizer = open(filename_fertilizer, 'a')
                date_now = datetime.datetime.now().strftime("%x") + ' ' + datetime.datetime.now().strftime("%H") + ':' + datetime.datetime.now().strftime("%M")
                file_fertilizer.write(f"{date_now}\t{pH_level}\n")
                file_fertilizer.close()
                draw(str('fertilizer_from_' + values['-dropdown-'] + '.txt'),3)
            else:
                window['-fertilizer-'].update(f"THE DEVICE IS NOT PLUGGED IN!")

        if event == sg.WIN_CLOSED: #Close
            break
    window.close()

if __name__ == '__main__':
    search_ports() #Search for ports one time before opening any window
