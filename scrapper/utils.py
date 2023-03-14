from time import sleep
from pyautogui import screenshot,click,moveTo,dragTo,write,press,hotkey
import platform
from sys import argv
import psutil
import os
import shutil
import json
from pyperclip import copy

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchWindowException,ElementClickInterceptedException,NoSuchElementException
from selenium.webdriver.support.ui import Select

import chromedriver_autoinstaller

def waitElement(by:By,element:str,driver:webdriver.Chrome):
    """A partir de un driver definido espera hasta 120 segundos que aparezca el objeto en cuestión.

    Args:
        by (By): Es el tipo de elemento que se buscará
        element (str): es el elemento a buscar
        driver (webdriver.Chrome): Es el chromedriver que se está utilizando para navegar
    """
    for i in range(120):
        try:
            driver.find_element(by,element)
            return
        except Exception as e:
            print(e)
            sleep(1)
            continue
    raise(TimeoutError)

def waitPixel(x:int,y:int,pixel:tuple=(255,255,255)):
    """This function wait a specific pixel turn on white (default) or an specific color

    Args:
        x (int): horizontal pixel
        y (int): vertical pixel
        pixel (tuple, optional): color of the pixel to wait. Defaults to (255,255,255).

    Returns:
        bool: return True when the pixel is right
        
    Example:
    >>> waitPixel(400,300,(222,106,99))
    True
    >>> 
    """
    im = screenshot()
    while im.getpixel((x,y)) != pixel:
        sleep(1)
        im = screenshot()
    return True

def pixel(x:int,y:int,pixel:tuple=(255,255,255)):
    im = screenshot()
    p = im.getpixel((x,y))
    if p == pixel:
        copy('coincide')
    else:
        copy('nocoincide')

def run(path:str):
    """execute a program from the specific path.
    Windows:
        Open the execute window with the hotkey Ctrl+R and turn on the program.
    Linux:
        Open the terminal with the hotkey Ctrl+Alt+T and execute a program with bash.

    Args:
        path (str): path from the executable file.
    """
    so = platform.system()
    if so == 'Linux':
        hotkey('ctrl','alt','t')
        write(f'bash {path}')
        press('enter')
        
    elif so == 'Windows':
        hotkey('windows','r')
        hotkey('ctrl','a')
        write(path,interval=.1)
        press('enter')
        
def processExists(program:str):
    for x in psutil.process_iter():
        if x.name() == program: return True
    return False

def processClose(program:str):
    [x.kill() for x in psutil.process_iter() if x.name() == program]
    

def initChrome(width:int=1400,height:int=600) ->webdriver.Chrome:
    """Instala la versión más nueva del chromedriver y luego inicializa el chrome con las opciones
    predeterminadas.
    - No GPU
    - No sandbox
    - Tamaño de la ventana 1400x600 px
    
    Args:
        width (int, optional): Defaults to 1400.
        height (int, optional): Defaults to 600.

    Returns:
        webdriver.Chrome: es el driver con el que se controla el navegador.
    """
    chromedriver_autoinstaller.install()
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument(f"window-size={width},{height}")
    return webdriver.Chrome(options=options)

def stringToList(string:str) -> list:
    """Recibe un string y retorna una lista con cada caracter como elemento de esta

    Args:
        string (str): es el texto que se quiere convertir en lista

    Returns:
        list: la lista de los caracteres de la palabra
    """
    list1 = []
    list1[:0] = string
    return list1

def valid_move_download(download_folder:str,filepath:str,startwith:str,endwith:str):
    """verifica que el archivo se ha descargado y mueve a otra ubicación.

    Args:
        download_folder (str): path de la carpeta de descarga
        filepath (str): path del archivo y el lugar en donde se va a mover
        startwith (str): subcadena de inicio del nombre del archivo
        endwith (str): subcadena que generalmente se utiliza como la extensión del archivo
    """
    while True:
        nm=''
        ls =  os.listdir(download_folder)
        for name in ls:
            if name.startswith(startwith) and name.endswith(endwith):
                if name+'.crdownload' in ls: continue
                nm = name
                shutil.copyfile(download_folder+name,filepath)
                print(download_folder+name + ' -> ' + filepath)
                os.remove(download_folder+name)
                break
        if name.startswith(startwith) and name.endswith(endwith): break
        sleep(2)
    