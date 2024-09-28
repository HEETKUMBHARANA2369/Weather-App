from customtkinter import *
import requests
from PIL import Image
import time

# MAIN LOGIC OF THE WEATHER API (BACKEND)
def weather():
    api_key = "61f3c26e9fe60399910326fcfacc322c"
    city = enter_city.get()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        
        # Extracting specific weather details
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        
        temperature_label.configure(text = (f"Temperature\n{temperature}°C").capitalize())
        weather_label.configure(text = (f"Weather in {city}\n{weather}").title())
        feels_like_label.configure(text = (f"Feels like\n{feels_like}°C").title())

        # print(data)
    else:
       city_label.configure(text="")
       err_label.configure(text= f"Error: Unable to fetch data, Status code: {response.status_code}")

# CONFIGURING BASE/MASTER WINDOW OF OUR APPLICATION
base_Window = CTk()
base_Window.geometry("1000x500")
base_Window.title("Weather App")
base_Window.config(background="#0D1117")

# CODE FOR SETTING THE ICON IMAGE FOR THE BASE WINDOW
try:
    img = "Weather_App_Icon.ico"
    base_Window.iconbitmap(True, img)
    findimage = "find.ico"
except Exception as e:
    print(f"Error loading icon as {e}")

# CREATING FONT OBJECT FOR APPLICATION
inner_font = CTkFont(family="Poppins", size=20, weight="normal")
over_font = CTkFont(family="Poppins", size=50, weight="bold")
time_font = CTkFont(family="Poppins Light", size=50)
city_font = CTkFont(family="Ubuntu", size=30)
entry_box_font = CTkFont(family= "Ubuntu",size=20)
weather_font = CTkFont(family = "Lato Black Italic")

# SETTING FRAME FOR MORE MINIMAL LOOK
frame1 = CTkFrame(master=base_Window, height=600, corner_radius=10, fg_color="#161B22",bg_color="#0D1117")
frame1.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

# Make the frame responsive by configuring rows and columns
frame1.rowconfigure(0, weight=1)  # Top space
frame1.rowconfigure(1, weight=0)  # Row for entry box
frame1.rowconfigure(2, weight=0)  # Row for button  
frame1.rowconfigure(3, weight=1)  # Bottom space
frame1.columnconfigure(0, weight=1)  # Left space
frame1.columnconfigure(1, weight=1)  # Middle column for entry and button
frame1.columnconfigure(2, weight=1)  # Right space

# CREATING A LABEL TO SHOW CURRENT TIME
time_label = CTkLabel(master=base_Window, text="", text_color="#58A6FF", bg_color="#0D1117", font=time_font)
time_label.grid(row=0, column=0, padx=20, sticky="w")

# DYNAMIC TIME SHOW
def current_time():
    real_time = time.strftime("%I:%M %p")
    time_label.configure(text=real_time)
    frame1.after(1000, current_time)

current_time()  # To Start The Clock

# CREATING A SUBMIT FUNCTION 
def submit():
    resize()
    if not enter_city.get():
        err_label.configure(text = "City cannot be empty!!")
        print("Enter something")
    else:
        if ((enter_city.get().replace(" ","")).isalpha()):
            city_label.configure(text=enter_city.get().capitalize())
            print("It is alphabet")
            weather()
        elif((enter_city.get().replace(" ","")).isnumeric):
            err_label.configure(text = "Cities don't have Numeric characters")
            print("not an alphabet")
#DEFINING KEY BINDING TO EXIT THE PROGRAM BY PRESSING THE ESCAPE KEY
def exit(key):
    base_Window.destroy()
base_Window.bind("<Escape>",exit)

#BINDING KEYS FOR ENTER AS SEARCH AND DELETE AS DELETE BUTTONS
def enter(key):
    submit()

# DYNAMIC LABEL FOR CITY
city_label = CTkLabel(master=base_Window, font=city_font, text="", text_color="#58A6FF", bg_color="#0D1117")
city_label.grid(row=0, column=0, sticky="e", padx=20)

# CREATING A TITLE FOR THE APPLICATION
title = CTkLabel(master=base_Window, text="Weather App", font=over_font, bg_color="#0D1117", text_color="#58A6FF")
title.grid(row=0, column=0, sticky="s")

# CREATING AN INPUT BOX
enter_city = CTkEntry(master=frame1, placeholder_text="Enter City",height = 50,width=500, border_width=0, font=entry_box_font)
enter_city.grid(row=0, column=1,sticky = "we",padx = 10)

# CREATING A BUTTON
findimage = CTkImage(Image.open("find.ico"))
button = CTkButton(master=frame1, image= findimage,text="",font=entry_box_font, command=submit,height=50,width=50,border_width=0,fg_color="#3D3D3D", hover_color="#5D5D5D",corner_radius=25)
button.grid(row=0, column=2,sticky = "w")
base_Window.bind("<Return>",enter)

#CREATING A BUTTON TO CLEAR THE CITY WITH ITS FUNCTION
def clear():
    city_label.configure(text = "")
    enter_city.delete(0,END)
    err_label.configure(text = "Error Box!")
    temperature_label.configure(text = "")
    weather_label.configure(text = "")
    feels_like_label.configure(text = "")

#CREATING A FUNCTION TO BIND THE DELETE BUTTON WITH CLEAR FUNCTION
def delete(key):
    clear()

del_image = CTkImage(Image.open("Delete_button.ico"))
clrbutton = CTkButton(master = frame1, text = "",image = del_image,command = clear,height=50,width=50,border_width=0,fg_color="#3D3D3D", hover_color="#5D5D5D",corner_radius=25)
clrbutton.grid(row = 0,column = 0,sticky = "e")
base_Window.bind("<Delete>",delete)

#MIDDLE FRAME SIZE
def resize():
    if len(enter_city.get()) > 8:
        print("size more than 8")
        weather_font.configure(size = 15)
    elif len(enter_city.get()) <= 8:
        print("size less than 8 ")
        weather_font.configure(size = 20)

#CREATING A SUB-FRAMES INSIDE FRAME-1,FOR DISPLAYING THE TEMPERATURES
frame2 = CTkFrame(master = frame1, width = 300, height = 300, corner_radius = 20) 
frame2.grid(row = 1,column = 1,sticky = "w",padx = 20, pady = 20)
frame3 = CTkFrame(master = frame1, width = 300, height = 300, corner_radius = 20)
frame3.grid(row = 1,column = 1, sticky = "s",padx = 20, pady = 20)
frame4 = CTkFrame(master = frame1, width = 300, height = 300, corner_radius = 20)
frame4.grid(row = 1,column = 1, sticky = "e",padx = 20, pady = 20)

#CREATING LABELS TO SHOW THE WEATHER 
temperature_label = CTkLabel(master = frame2, text = "",width = 160,height = 160,font=weather_font)
temperature_label.grid(padx = 10,pady = 10)
weather_label = CTkLabel(master = frame3, text = "",width = 160,height = 160,font=weather_font)
weather_label.grid(padx = 10,pady = 10)
feels_like_label = CTkLabel(master = frame4, text = "",width = 160,height = 160,font=weather_font)
feels_like_label.grid(padx = 10,pady = 10)

#CREATING AN ERROR BOX FOR THE MESSAGES TO SHOW
err_box = CTkFrame(master = frame1,height = 30, width=400)
err_box.grid(row = 2,pady = 20,padx = 20,column = 1,sticky = "ns")
err_label = CTkLabel(master = err_box,text = "Error Box!", font=entry_box_font, corner_radius=25)
err_label.grid()

# BASE WINDOW RESPONSIVE-NESS
base_Window.columnconfigure(0, weight=1)
base_Window.rowconfigure(1, weight=1)

# TO EXECUTE THE WINDOW
base_Window.mainloop()