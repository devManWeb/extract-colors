from PIL import Image
from datetime import datetime
from tkinter import filedialog
import tkinter as tk
from threading import Thread
from os import path

def RGBtoHEX(color):
    #RGB to HEX conversion (no transparency)
    return '#%02x%02x%02x' % (color)

def imagePixels(image):
    #returns a list with individual pixels and colors
    selectedImage = Image.open(image)
    imageRGB = selectedImage.convert("RGB")
    width, height = imageRGB.size

    colorList = []
    for x in range(0,width):
        for y in range(0,height):
            colorList.append(
                RGBtoHEX(
                    imageRGB.getpixel((x, y))
                )
            )

    return colorList


def countNumber(list):
    #returns a set with each color and number of times it appears
    uniqueColors = set(list)
    finalList = []
    NumPixels = len(list)

    for item in uniqueColors:
        finalList.append([
            item,
            round(
                list.count(item) / NumPixels * 100,
                3
            )
        ])

    return sorted(finalList)

def createHTML(data,image,timeStamp):
    #used to create the HTML to be inserted on the page
    
    HTML = f'''
        <!DOCTYPE html>
            <head></head>
            <body>
                <h1>Image analysis results</h1>
                <p>Image: {image}</h1>
                <p>Analized: {timeStamp}</h1>
        '''

    for element in data:
        HTML = HTML + f'''
                <div style='float:left;margin:10px;width:130px;align-content:center;'>
                    <div style='background-color:{element[0]};width:100px;height:100px;border:3px solid black'>
                    </div> {element[0]} {element[1]} %
                </div>
                '''
    
    HTML = HTML + "</body></html>"
    return HTML
    

def createHTMLFile(image):
    #generates the HTML file after reading the image
    dateTimeObj = datetime.now()
    timeStampStr = dateTimeObj.strftime("%d_%m_%Y_%H_%M_%S_%f")
    print(f"Analysis of {image}....")
    colorData = countNumber(imagePixels(image))
   
    file = open(f"{timeStampStr}.html","w")
    file.write(
        createHTML(
            colorData,
            image,
            timeStampStr
        )
    )
    file.close()
    print(f"Ended, see {timeStampStr}.html for {image}")


def processImage():
    #threading to not block the program

    def selectImage():
        #opens the dialog to choose the image
        image = filedialog.askopenfilename(
            initialdir = "/",
            title = "Select file",
            filetypes=[('image files', ('.png', '.jpg'))]
        )
        if len(image) > 0:
            if path.getsize(image) < 20480:
                createHTMLFile(image)
            else:
                print("The chosen image is too big")

    t = Thread(target=selectImage)
    t.start()

def runGUI():
    #main function, loads the GUI
        
    window = tk.Tk()
    window.title("Analyze image's colors")
    window.geometry('500x200')

    frame = tk.Frame(window)
    frame.pack( side = tk.TOP )

    label = tk.Label(frame,text = "Max 20 kB")
    label.pack( side = tk.LEFT )
    button = tk.Button(frame, text="Select image",command=processImage)
    button.pack( side = tk.LEFT )

    textbox = tk.Text(window)
    textbox.pack()

    #intercepts print() and adds the text on the GUI
    def redirector(inputStr):
        textbox.insert(tk.INSERT, inputStr)
    tk.sys.stdout.write = redirector 

    window.mainloop()

try:
    runGUI()
except e:
    print("An error has occurred!")
