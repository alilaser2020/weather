import PySimpleGUI as sg
import requests
from bs4 import BeautifulSoup as bs


def get_weather_date(city):
    """
    A method for getting data about each city that it's requested
    :param city:
    :return:
    """
    url = f"https://www.google.com/search?q={city.replace(' ', '')}+weather"
    USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36")
    session = requests.Session()
    session.headers["user-agent"] = USER_AGENT
    response = session.get(url)

    # Create a soup:
    soup = bs(response.text, "html.parser")
    time = soup.find("div", attrs={'id': 'wob_dts'}).text
    weather = soup.find("span", attrs={'id': 'wob_dc'}).text
    temp = soup.find("span", attrs={'id': 'wob_tm'}).text
    return time, weather, temp


def create_theme(theme):
    """
    A method for create a theme for window
    :param theme:
    :return:
    """
    sg.theme(theme)
    sg.set_options(font="Calibre 15")
    img_col = sg.Column([[sg.Image(key="-IMAGE-", pad=(70, 4))]])
    info_col = sg.Column([
        [sg.Text("location", key="-LOCATION-", font="Calibre 35", text_color="#FF0000", background_color="#FFFFFF",
                 pad=(2, 5), visible=False)],
        [sg.Text("time", key="-TIME-", font="Calibre 25", text_color="#000000", background_color="#FFFFFF",
                 pad=(2, 5), visible=False)],
        [sg.Text("temp", key="-TEMP-", font="Calibre 25", text_color="#000000", background_color="#FFFFFF",
                 pad=(2, 5), visible=False)]
    ])
    layout = [
        [sg.Input(key="-INPUT-", right_click_menu=theme_menu), sg.Button("Enter", key="-ENTER-",
                right_click_menu=theme_menu, expand_x=True)],
        [img_col, info_col],
    ]
    return sg.Window("Converter", layout)


theme_menu = ["menu", ["Black", "BlueMono", "Dark", "random"]]
window = create_theme("graygraygray")

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event in theme_menu[1]:
        window.close()
        window = create_theme(event)
    if event == "-ENTER-":
        time, weather, temp = get_weather_date(values["-INPUT-"])
        window["-LOCATION-"].update(values["-INPUT-"].title(), visible=True)
        window["-TIME-"].update(time, visible=True)
        window["-TEMP-"].update(f"{temp} \u2103 ({weather})", visible=True)
        if weather in ('cloud', 'cloudy', 'grey', 'gloomy', 'dismal', 'murky', 'overcast'):
            window["-IMAGE-"].update("symbols/cloud.png")
        elif weather in ('Mist', 'Dust', 'Fog', 'Smoke', 'Haze', 'Flurries'):
            window["-IMAGE-"].update("symbols/fog.png")
        elif weather in ('Partly Sunny', 'Mostly Sunny', 'Partly cloudy', 'Mostly cloudy', 'Cloudy', 'Overcast'):
            window["-IMAGE-"].update("symbols/part sun.png")
        elif weather in ('Rain', 'Chance of Rain', 'Light Rain', 'Showers', 'Scattered Showers', 'Rain and Snow', 'Hail'):
            window["-IMAGE-"].update("symbols/rain.png")
        elif weather in ('Freezing Drizzle', 'Chance of Snow', 'Sleet', 'Snow', 'Icy', 'Snow Showers'):
            window["-IMAGE-"].update("symbols/snow.png")
        elif weather in ('Sun', 'Sunny', 'Clear', 'Clear with periodic clouds', 'Mostly sunny'):
            window["-IMAGE-"].update("symbols/sun.png")
        elif weather in ('Scattered Thunderstorms', 'Chance of Storm', 'Storm', 'Thunderstorm', 'Chance of TStorm'):
            window["-IMAGE-"].update("symbols/thunder.png")

window.close()
