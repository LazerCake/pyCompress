# Program for compressing videos using a tkinter GUI and ffmpeg
from tkinter import *
from tkinter import filedialog
import subprocess
import sys
import os
from moviepy.video.io.VideoFileClip import VideoFileClip #The line that adds 43mb to the exe size >:(

print("Opening GUI...")

if not os.path.exists("output"):
        os.mkdir("output")

#use global variables so that information can be remembered between runs of compression function
outputDest = './output' 
filename = ''

# Function for opening the file explorer window
def browseInput():
    global filename
    filename = filedialog.askopenfilename(initialdir = filename + "/", #open at last place used by browser
                                          title = "Select a File",
                                          filetypes = ((".mp4",
                                                        "*.mp4*"),
                                                       ("all files",
                                                        "*.*")))
    
    # Change label contents
    label_inputPath.configure(text="File opened: " + filename)

def browseOutput():
    global outputDest
    outputDest = filedialog.askdirectory(initialdir = outputDest, #open at last place used by browser
                                          title = "Select an output folder")
    
    # Change label contents
    label_outputPath.configure(text="Output path: " + outputDest)

#Compresses one video without target size
def compressVideo():
    global filename
    global outputDest

    preset = presetVar.get()

    if filename == "":
        print("ERROR - NO INPUT FILE.")
        return

    if not os.path.exists("output"): #check again for output folder in case it was deleted while the program was running
        os.mkdir("output")

    outputName = entry_outputName.get() #set name of output, or set to a default if none given
    if outputName == '':
        outputName = os.path.basename(filename) + "_Compressed"

    subprocess.run(["ffmpeg.exe", "-i", filename, "-c:v", "libx264", "-preset", preset, "-crf", "22", "-c:a", "copy", f"{outputDest}/{outputName}.mp4"], shell=True)

    print("------------------")
    print("Video compressed!")

#Compresses video to target size, potentially losing quality
def resize():
    global filename
    global outputDest

    preset = presetVar.get()

    inputSize = sys.getsizeof(filename) #returns bytes
    outputSize = float(entry_outputSize.get())

    #audioBitrate = 64 if outputSize < 0.15  else 128 #reduces audio bitrate if outputting below certain size
    audioBitrate = 128

    if filename == "":
        print("ERROR - NO INPUT FILE.")
        return

    outputName = entry_outputName.get() #set name of output, or set to a default if none given
    if outputName == '':
        outputName = os.path.basename(filename) + "_Compressed"

    if not os.path.exists("output"): #make 'output' directory if not present
        os.mkdir("output")

    duration = VideoFileClip(filename).duration
    minSize = (audioBitrate * duration) / 8000

    if outputSize < minSize: #check if given size is too small for 
        print(f"Requested size is too small! Minimum size for this file: {minSize} MB")
        return
    
    bitrate = ((outputSize * 8000 / duration) - audioBitrate) #get output video bitrate by converting size given in MB to kilobits, divide by length, and account for audio bitrate

    #First pass
    subprocess.run(["ffmpeg.exe", "-y", "-i", filename, "-max_muxing_queue_size", "9999", "-c:v", "libx264", "-preset", preset, "-b:v", f"{bitrate}k", "-pass", "1", 
                    "-vsync", "cfr", "-f", "null", "/dev/null", "&&", '\''], shell=True)
    #Second pass
    subprocess.run(["ffmpeg.exe", "-i", filename, "-max_muxing_queue_size", "9999", "-c:v", "libx264", "-preset", preset, "-b:v", f"{bitrate}k", "-pass", "2", 
                    "-c:a", "aac", "-b:a", f"{audioBitrate}k", f"{outputDest}/{outputName}.mp4"], shell=True)

    # First pass: ffmpeg -y -i input -max_muxing_queue_size 9999 -c:v libx264 -b:v 2600k -pass 1 -an -f null /dev/null && \
    # Second pass: ffmpeg -i input -max_muxing_queue_size 9999 -c:v libx264 -b:v 2600k -pass 2 -c:a aac -b:a 128k output.mp4

    print("------------------")
    print("Video compressed!")

def execute():
    outputSize = entry_outputSize.get()
    if not outputSize == '' and float(outputSize) > 0:
        resize()
    else: compressVideo()

# Create the root window
window = Tk()
# Set window title
window.title('pyCompress!')
# Set window size
window.geometry("700x500")
#Set window background color
window.config(background = "white")
  
#Title label
label_title = Label(window,
                    text = "Video compressor using ffmpeg and Tkinter",
                    width = 100, height = 4,
                    fg = "blue")
#Input path label
label_inputPath = Label(window,
                        text = "File opened: -",
                        width = 100, height = 1,
                        fg = "blue")
#Output path label
label_outputPath = Label(window,
                        text = "Output path: ./output",
                        width = 100, height = 1,
                        fg = "blue")
#Input browse button
button_inputExplore = Button(window,
                        text = "Browse for input",
                        command = browseInput)
#Label for output name text entry
label_outputName = Label(window, 
                        text = "Output name:")
#Output name text entry
entry_outputName = Entry(window,
                        width = 32,
                        bg = "white",
                        fg = "black")
#Output path browse button
button_outputExplore = Button(window,
                        text = "Browse for output path",
                        command = browseOutput)
#Label for output size
label_outputSize = Label(window, 
                        text = "Desired output size (MB):")
#Desired output size text entry
entry_outputSize = Entry(window,
                        width = 8,
                        bg = "white",
                        fg = "black")
#Label for compression preset dropdown
label_presets = Label(window, 
                        text = "Compression preset:")
#Dropdown menu of compression presets
presetList = ['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow']
presetVar = StringVar()
presetVar.set(presetList[5])
options_presets = OptionMenu(window,
                            presetVar,
                            *presetList)
#Button to run compressing process
button_compress = Button(window,
                        text = "Compress Video",
                        command = execute)
#Button to exit program
button_exit = Button(window,
                     text = "Exit",
                     command = sys.exit)

# Grid method is chosen for placing the widgets at respective positions in a table like structure by specifying rows and columns
label_title.grid(column = 1, row = 1, pady = [0, 3])
label_inputPath.grid(column = 1, row = 2, pady = [3, 3])
label_outputPath.grid(column = 1, row = 3, pady = [3, 3])
button_inputExplore.grid(column = 1, row = 4, pady = [3, 3])
button_outputExplore.grid(column = 1, row = 5, pady = [3, 3])
label_outputName.grid(column = 1, row = 6, pady = [3, 1])
entry_outputName.grid(column = 1, row = 7, pady = [1, 3])
label_outputSize.grid(column = 1, row = 8, pady = [3, 1])
entry_outputSize.grid(column = 1, row = 9, pady = [1, 3])
label_presets.grid(column = 1, row = 10, pady = [1, 3])
options_presets.grid(column = 1, row = 11, pady = [1, 3])
button_compress.grid(column = 1, row = 12, pady = [10, 3])
button_exit.grid(column = 1,row = 13, pady = [10, 3])

# Let the window wait for any events
window.mainloop()