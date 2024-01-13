from tkinter import *
from tkinter import font
from PIL import ImageTk, Image
import requests
from io import BytesIO
import json
import random
import pygame

# function to automatically play background  music
def play_music():
    # Initialize Pygame Mixer
    pygame.mixer.init()
    # Load your music file
    pygame.mixer.music.load(r'Images\audios\Harry Potter Main Theme Slowed Down (Extended 1H).mp3')
    # Play the music, -1 for looping indefinitely
    pygame.mixer.music.play(-1)

# Function to mute and unmute the background music
def toggle_sound():
    if pygame.mixer.music.get_volume() > 0:
        pygame.mixer.music.set_volume(0)  # Mute the music
        mute_button.config(image=unmute_button_photo)  # Change to unmute image
        mute_button.image = unmute_button_photo  # Update the button's image reference
    else:
        pygame.mixer.music.set_volume(1)  # Unmute the music
        mute_button.config(image=mute_button_photo)  # Change to mute image
        mute_button.image = mute_button_photo  # Update the button's image reference

def raise_frame(frame):
    frame.tkraise()

def start_button_click():
    raise_frame(app_frame)
    raise_frame(navigation_frame)
    raise_frame(instruction_frame)

def instruction_button_click():
    raise_frame(instruction_frame)
    # Reset the style of other navigation buttons
    character_button.config(fg=yellow_color, bg=blue2_color)
    books_button.config(fg=yellow_color, bg=blue2_color)
    movies_button.config(fg=yellow_color, bg=blue2_color)
    potions_button.config(fg=yellow_color, bg=blue2_color)

def character_click():
    raise_frame(character_frame)

    # Change the style of the Books button to indicate it's the active page
    character_button.config(fg=blue_color, bg=yellow2_color)

    # Reset the style of other navigation buttons
    books_button.config(fg=yellow_color, bg=blue2_color)
    movies_button.config(fg=yellow_color, bg=blue2_color)
    potions_button.config(fg=yellow_color, bg=blue2_color)

def books_button_click():
    raise_frame(books_frame)

    # Change the style of the Books button to indicate it's the active page
    books_button.config(fg=blue_color, bg=yellow2_color)

    # Reset the style of other navigation buttons
    character_button.config(fg=yellow_color, bg=blue2_color)
    movies_button.config(fg=yellow_color, bg=blue2_color)
    potions_button.config(fg=yellow_color, bg=blue2_color)

def movies_button_click():
    raise_frame(movies_frame)

    # Change the style of the Books button to indicate it's the active page
    movies_button.config(fg=blue_color, bg=yellow2_color)

    # Reset the style of other navigation buttons
    character_button.config(fg=yellow_color, bg=blue2_color)
    books_button.config(fg=yellow_color, bg=blue2_color)
    potions_button.config(fg=yellow_color, bg=blue2_color)

def potions_button_click():
    raise_frame(potions_frame)

    # Change the style of the Books button to indicate it's the active page
    potions_button.config(fg=blue_color, bg=yellow2_color)

    # Reset the style of other navigation buttons
    character_button.config(fg=yellow_color, bg=blue2_color)
    books_button.config(fg=yellow_color, bg=blue2_color)
    movies_button.config(fg=yellow_color, bg=blue2_color)

image_references = []

# *****************************************************************************************************************
# books data retrieval code
def display_books():
    global books_display_frame
    global image_references

    api_url = "https://api.potterdb.com/v1/books"
    try:
        response = requests.get(api_url)
        data = response.json()
        books = data['data']
    except Exception as e:
        print("Error geting or parsing book data:", e)
        return  

    for widget in books_display_frame.winfo_children():
        widget.destroy()

    # Create a frame to wrap the canvas with a blue border
    canvas_frame = Frame(books_display_frame, bg=blue_color, borderwidth=3, relief="solid")
    canvas_frame.place(x=0, y=0, relwidth=1, relheight=1)

    # Create the canvas inside the frame
    book_canvas = Canvas(canvas_frame, bg="white")
    book_scrollbar = Scrollbar(canvas_frame, orient="vertical", command=book_canvas.yview)
    book_scrollbar.place(relx=0.97, rely=0, relwidth=0.03, relheight=1)
    book_canvas.place(relx=0, rely=0, relwidth=0.97, relheight=1)
    book_canvas.configure(yscrollcommand=book_scrollbar.set)

    books_container = Frame(book_canvas, bg=yellow2_color)
    book_canvas.create_window((0, 0), window=books_container, anchor='nw')

    container_height = 0
    
    image_references.clear()

    title_width = 300  # Increase the width for the title label if needed
    summary_width = 500  # Increase the width for the summary label if needed

    for i, book_data in enumerate(books):
        try:
            cover_url = book_data['attributes']['cover']
            cover_response = requests.get(cover_url)
            cover_img = Image.open(BytesIO(cover_response.content))
            cover_img = cover_img.resize((70, 120))
            cover_photo = ImageTk.PhotoImage(cover_img)
            cover_lbl = Label(books_container, image=cover_photo)
            cover_lbl.image = cover_photo  # Keep a reference as an attribute.
            image_references.append(cover_photo)  # Add the PhotoImage to the list.
            cover_lbl.place(x=10, y=i*180, width=70, height=120)

            # Keep a reference to each image
            cover_photo = ImageTk.PhotoImage(cover_img)
            cover_lbl = Label(books_container, image=cover_photo)
            cover_lbl.image = cover_photo  # Keep a reference as an attribute.
            image_references.append(cover_photo)  # Add the PhotoImage to the list.
            cover_lbl.place(x=10, y=i*180, width=70, height=120)

            # Increase the width of the title label
            title_lbl = Label(books_container, text=book_data['attributes']['title'], font=text_font4, 
                              fg=blue_color, bg=yellow2_color)
            title_lbl.place(x=90, y=i*180, width=title_width, height=20)

            # Increase the width of the summary label and adjust wraplength accordingly
            summary_lbl = Label(books_container, text=book_data['attributes']['summary'], font=('New York Times', 8), 
                                fg=blue_color, wraplength=summary_width, justify='left', bg=yellow2_color)
            summary_lbl.place(x=90, y=i*180 + 30, width=summary_width, height=100)


            container_height = i * 180 + 180  # Adjust the height based on the number of books

            image_references.append(cover_photo)  # Store reference
            print(f"Added book {i} to the canvas")
        except Exception as e:
            print("Error loading book data:", e)

            print(f"Processing book {i}: {book_data['attributes']['title']}")

    # Simplified content for debugging

    books_container.config(width=800, height=container_height)  # Set a fixed width and dynamic height
    books_container.update_idletasks()
    book_canvas.config(scrollregion=book_canvas.bbox("all"))

    print("Books container size:", books_container.winfo_width(), books_container.winfo_height())
    print("Canvas scroll region:", book_canvas.cget("scrollregion"))

    
    books_container.update_idletasks()
    book_canvas.config(scrollregion=book_canvas.bbox("all"))

# ****************************************************************************************************************
# movies data 
image_references = []

def display_movies():
    global movies_display_frame
    global image_references

    api_url = "https://api.potterdb.com/v1/movies"
    try:
        response = requests.get(api_url)
        data = response.json()
        movies = data['data']
    except Exception as e:
        print("Error retrieving or parsing movie data:", e)
        return  

    for widget in movies_display_frame.winfo_children():
        widget.destroy()

    canvas_frame = Frame(movies_display_frame, bg=blue_color, borderwidth=3, relief="solid")
    canvas_frame.place(x=0, y=0, relwidth=1, relheight=1)

    movie_canvas = Canvas(canvas_frame, bg="white")
    movie_scrollbar = Scrollbar(canvas_frame, orient="vertical", command=movie_canvas.yview)
    movie_scrollbar.place(relx=0.97, rely=0, relwidth=0.03, relheight=1)
    movie_canvas.place(relx=0, rely=0, relwidth=0.97, relheight=1)
    movie_canvas.configure(yscrollcommand=movie_scrollbar.set)

    movies_container = Frame(movie_canvas, bg=yellow2_color)
    movie_canvas.create_window((0, 0), window=movies_container, anchor='nw')

    container_height = 0
    image_references = []

    title_width = 500
    summary_width = 500
    summary_height = 150
    poster_size = (80, 130)
    text_x_position = 100  # Increased to shift text to the right

    for i, movie_data in enumerate(movies):
        y_position = i * 250  # Adjusted for additional text
        try:
            poster_url = movie_data['attributes']['poster']
            poster_response = requests.get(poster_url)
            poster_img = Image.open(BytesIO(poster_response.content))
            poster_img = poster_img.resize(poster_size)

            poster_frame = Frame(movies_container, bg=blue_color, borderwidth=3, relief="solid")
            poster_frame.place(x=10, y=y_position, width=poster_size[0], height=poster_size[1])

            poster_photo = ImageTk.PhotoImage(poster_img)
            poster_lbl = Label(poster_frame, image=poster_photo, bg='white')
            poster_lbl.image = poster_photo
            image_references.append(poster_photo)
            poster_lbl.pack(fill='both', expand='yes')

            # Title label aligned to the left
            title_lbl = Label(movies_container, text="Title: " + movie_data['attributes']['title'], font=text_font4, 
                              fg=blue_color, bg=yellow2_color, anchor='w')  # Added anchor='w' for left alignment
            title_lbl.place(x=text_x_position, y=y_position, width=title_width, height=20)

            # Summary heading moved down closer to the summary text
            summary_heading_y_position = y_position + 45  # Adjusted Y position for summary heading
            summary_heading_lbl = Label(movies_container, text="Summary:", font=text_font4, 
                                        fg=blue_color, bg=yellow2_color, anchor='w')
            summary_heading_lbl.place(x=text_x_position, y=summary_heading_y_position, width=title_width, height=20)

            # Summary label
            summary_lbl_y_position = summary_heading_y_position + 25  # Adjusted Y position for summary text
            summary_lbl = Label(movies_container, text=movie_data['attributes']['summary'], font=('New York Times', 8), 
                                fg=blue_color, wraplength=summary_width, justify='left', bg=yellow2_color)
            summary_lbl.place(x=text_x_position, y=summary_lbl_y_position, width=summary_width, height=summary_height)

            container_height = y_position + 250

            print(f"Added movie {i} to the canvas")
        except Exception as e:
            print("Error loading movie data:", e)

    movies_container.config(width=800, height=container_height)
    movies_container.update_idletasks()
    movie_canvas.config(scrollregion=movie_canvas.bbox("all"))

    print("Movies container size:", movies_container.winfo_width(), movies_container.winfo_height())
    print("Canvas scroll region:", movie_canvas.cget("scrollregion"))

# ****************************************************************************************************************
# potions data 
def get_random_potion():
    status_label.config(text="Retrieving Data...")
    root.update_idletasks()

    url = "https://api.potterdb.com/v1/potions"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        potions = data['data']

        if not potions:
            status_label.config(text="No potions available")
            return

        # Randomly select a potion
        random_potion = random.choice(potions)

        # Update the potion name and effect
        potion_name = random_potion['attributes']['name']
        potion_effect = random_potion['attributes']['effect']
        potion_name_label.config(text=potion_name)
        potion_effect_label.config(text=potion_effect)

        # Fetch and set the potion image
        potion_image_url = random_potion['attributes']['image']
        image_response = requests.get(potion_image_url)
        if image_response.status_code == 200:
            image = Image.open(BytesIO(image_response.content))
            image = image.resize((299, 383))  # Resize as needed
            image = ImageTk.PhotoImage(image)
            potions_image_label.config(image=image)
            potions_image_label.image = image
        status_label.config(text="")
    else:
        status_label.config(text=f"Failed to retrieve data: {response.status_code}")

    root.update_idletasks()

# ****************************************************************************************************************
# character data 
def search_character():
    search_name = search.get().lower()  # Retrieve user input and convert to lowercase
    url = "https://api.potterdb.com/v1/characters?page[number]="

    for page in range(1, 48):  # Iterate through all pages
        url_search = f"{url}{page}"
        response = requests.get(url_search)
        if response.status_code == 200:
            data = response.json()
            characters_list = data.get('data', [])

            for character in characters_list:
                name = character['attributes'].get('name', '').lower()
                if search_name in name:
                    # Found the character, update UI
                    update_character_info(character)
                    return  # Stop searching after finding the character
        else:
            print(f"Failed to retrieve data from page {page}")

    # If no character is found
    character_name_label.config(text="Character not found")
    character_Gender_label.config(text="")
    character_born_label.config(text="")
    character_image_label.config(image='')  # Clear previous image

def update_character_info(character):
    # Extract character information
    name = character['attributes'].get('name', '')
    gender = character['attributes'].get('gender', 'Not available')
    born = character['attributes'].get('born', 'Not available')
    image_url = character['attributes'].get('image', '')

    # Update the labels
    character_name_label.config(text=name)
    character_Gender_label.config(text=gender)
    character_born_label.config(text=born)

    # Fetch and update the image
    if image_url:
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            image = Image.open(BytesIO(image_response.content))
            image = image.resize((299, 383))
            image = ImageTk.PhotoImage(image)
            character_image_label.config(image=image)
            character_image_label.image = image  # Keep a reference
        else:
            character_image_label.config(image='')  # Clear previous image
            print("Failed to retrieve character image")
    else:
        character_image_label.config(image='')  # Clear previous image



# ****************************************************************************************************************
# designing the gui
# creating two variables for the main color used
blue_color = '#06004B'
blue2_color = '#211D53'
yellow_color= '#AB9975'
yellow2_color = '#DCCDAE'
yellow3_color = '#EEE5D2'

play_music()

# Creating the window
root = Tk()
root.title('Wizarding Wonders') # Setting the title
root.geometry('1085x690') #setting width and height
root.resizable(0,0)
root.config(bg=blue_color) # setting a bg

# Defining font styles in variables which will be called later
text_font = font.Font(family="Georgia", size=18, weight=font.BOLD)
text_font2 = font.Font(family="Georgia", size=16, weight=font.BOLD)
text_font3 = font.Font(family="Georgia", size=23, weight=font.BOLD, underline=2)
text_font4 = font.Font(family="Times New Roman", size=13, weight=font.BOLD)
text_font5 = font.Font(family="Times New Roman", size=16, weight=font.BOLD)

landing_page = Frame(root, width=1100, height=700, bg=blue_color)
landing_page.place(x=0, y=0)

# Opening and resizing the image
img = Image.open(r'Images\audios\landing page.png')
img = img.resize((1100, 700), Image.BOX)  # Resizing the image to fit the window without antialiasing

# Creating PhotoImage object from the resized image
resized_background_image = ImageTk.PhotoImage(img)

# Creating a label for the background image
background_label = Label(landing_page, image=resized_background_image)
background_label.place(relwidth=1, relheight=1)

# Load the image for the "Start" button
start_button_image = Image.open(r"Images\audios\start-button.jpeg")
start_button_image = start_button_image.resize((150, 50))  # Adjust size as needed
start_button_photo = ImageTk.PhotoImage(start_button_image)

# Button to start the app with the image
start_button = Button(landing_page, image=start_button_photo, command=start_button_click, borderwidth=0, highlightthickness=0)
start_button.image = start_button_photo
start_button.place(relx=0.5, rely=0.8, anchor=CENTER)

# creating the main app frame
app_frame = Frame(root, width=1100, height=700)
app_frame.place(x=0, y=0)

#nav frame
navigation_frame = Frame(app_frame, width=276, height=700, bg=blue_color)
navigation_frame.place(x=0, y=0)

img = Image.open(r"Images\audios\main logo.jpeg")
img = img.resize((250, 130))
photo = ImageTk.PhotoImage(img)
label = Label(navigation_frame, image=photo, borderwidth=0, highlightthickness=0)
label.image = photo  
label.place(x=15, y=10)

character_button = Button(navigation_frame, text='Character       ', font=text_font2, fg=yellow_color, bg=blue2_color, 
                    bd=0, padx=70, pady=10, command=character_click)
character_button.place(x=0, y=180)

books_button = Button(navigation_frame, text='Books       ', font=text_font2, fg=yellow_color, bg=blue2_color, 
                    bd=0, padx=90, pady=10, command=books_button_click)
books_button.place(x=0, y=250)

movies_button = Button(navigation_frame, text='Movies       ', font=text_font2, fg=yellow_color, bg=blue2_color, 
                    bd=0, padx=85, pady=10, command=movies_button_click)
movies_button.place(x=0, y=320)

potions_button = Button(navigation_frame, text='Potions       ', font=text_font2, fg=yellow_color, bg=blue2_color, 
                    bd=0, padx=80, pady=10, command=potions_button_click)
potions_button.place(x=0, y=390)

# instruction page button
instruction_button_image = Image.open(r"Images\audios\instructions button.jpeg")
instruction_button_image = instruction_button_image.resize((150, 50))
instruction_button_photo = ImageTk.PhotoImage(instruction_button_image)

instruction_button = Button(navigation_frame, image=instruction_button_photo, borderwidth=0, highlightthickness=0,command=instruction_button_click)
instruction_button.image = instruction_button_photo
instruction_button.place(x=55, y=480)

# Mute music button
mute_button_image = Image.open(r"Images\audios\mute music button.jpeg")
mute_button_image = mute_button_image.resize((150, 50))
mute_button_photo = ImageTk.PhotoImage(mute_button_image)

# Unmute music button
unmute_button_image = Image.open(r"Images\audios\unmute music button.jpeg")
unmute_button_image = unmute_button_image.resize((150, 50))  # Correct resizing
unmute_button_photo = ImageTk.PhotoImage(unmute_button_image)

# Mute button
mute_button = Button(navigation_frame, image=mute_button_photo, borderwidth=0, highlightthickness=0, command=toggle_sound)
mute_button.image = mute_button_photo
mute_button.place(x=55, y=540)


# instruction frame
instruction_frame = Frame(app_frame, width=824, height=701, bg=yellow_color)
instruction_frame.place(x=276, y=0)

img = Image.open(r"Images\audios\instructions frame.png")
photo = ImageTk.PhotoImage(img)
label = Label(instruction_frame, image=photo, borderwidth=0, highlightthickness=0)
label.image = photo  
label.place(x=0, y=0)

# PLACING THE CREDITS IMAGE ON NAVBAR
img = Image.open(r"Images\audios\name credit.png")
original_width, original_height = img.size

# Increase by 10%
new_width = int(original_width * 0.2)
new_height = int(original_height * 0.2)

# Resize the image
img = img.resize((new_width, new_height))
photo = ImageTk.PhotoImage(img)
label = Label(navigation_frame, image=photo, borderwidth=0, highlightthickness=0)
label.image = photo  
label.place(x=0, y=610)


# ****************************************************************************************************
# Characters Frame
character_frame = Frame(app_frame, width=824, height=701, bg=yellow_color)
character_frame.place(x=276, y=0)

img = Image.open(r"Images\audios\characters frame.jpg")
photo = ImageTk.PhotoImage(img)
label = Label(character_frame, image=photo, borderwidth=0, highlightthickness=0)
label.image = photo  
label.place(x=0, y=0)

search_border = Frame(character_frame, bg=blue_color)
search_border.place(x=70, y=140, width=500, height=60)

search = Entry(search_border, bg='white' , fg=blue_color, borderwidth=4,
               relief='flat', font=text_font2, justify=CENTER)
search.place(x=3, y=3, width=494, height=54)

# Button to search for a character
search_button_image = Image.open(r"Images\audios\search-button.jpeg")
search_button_image = search_button_image.resize((150, 50))
search_button_photo = ImageTk.PhotoImage(search_button_image)

search_button = Button(character_frame, image=search_button_photo, borderwidth=0, highlightthickness=0,command=search_character)
                    #    command=search_character
search_button.image = search_button_photo
search_button.place(x=590, y=144)

#image frame
character_image_frame = Frame(character_frame, bg=blue_color)
character_image_frame.place(x=70, y=240, width=299, height=383)

character_image_label = Label(character_image_frame, bg=yellow3_color)
character_image_label.place(x=6, y=6, width=287, height=370)

# image of the character will be placed

#character info frame
character_info_border = Frame(character_frame, bg=blue_color)
character_info_border.place(x=400, y=240, width=316, height=366)

character_info_frame = Frame(character_info_border, bg=yellow3_color)
character_info_frame.place(x=7, y=7, width=300, height=350)

info_heading = Label(character_info_frame,text="Character Information", bg=yellow3_color, fg=blue_color,
                        font=text_font2, justify=CENTER)
info_heading.place(x=25, y=15)

character_name_heading = Label(character_info_frame,text="Character Name:", bg=yellow3_color, fg=blue_color,
                        font=text_font5, justify=LEFT)
character_name_heading.place(x=10, y=60)

character_name_label = Label(character_info_frame,text="", bg=yellow3_color, fg=blue2_color,
                        font=text_font4, justify=LEFT)
character_name_label.place(x=30, y=90)

character_gender_heading = Label(character_info_frame,text="Gender:", bg=yellow3_color, fg=blue_color,
                        font=text_font5, justify=LEFT)
character_gender_heading.place(x=10, y=140)

character_Gender_label = Label(character_info_frame,text="", bg=yellow3_color, fg=blue2_color,
                        font=text_font4, justify=LEFT)
character_Gender_label.place(x=20, y=200)

character_born_heading = Label(character_info_frame,text="Born In:", bg=yellow3_color, fg=blue_color,
                        font=text_font5, justify=LEFT)
character_born_heading.place(x=10, y=240)

character_born_label = Label(character_info_frame,text="", bg=yellow3_color, fg=blue2_color,
                        font=text_font4, justify=LEFT, wraplength=250)
character_born_label.place(x=20, y=280, width=270)


# ****************************************************************************************************
# books Frame
# Calculate the available height for the books_display_frame based on the window height
available_height = 701 - 150  # Subtracting the space for navigation and other elements
books_display_height = min(available_height, 4000)  # Ensure it doesn't exceed the available space

books_frame = Frame(app_frame, width=824, height=701, bg=yellow_color)
books_frame.place(x=276, y=0)

img = Image.open(r"Images\audios\books frame.jpg")
photo = ImageTk.PhotoImage(img)
label = Label(books_frame, image=photo, borderwidth=0, highlightthickness=0)
label.image = photo  
label.place(x=0, y=0)

# Books Display Frame
books_display_frame = Frame(books_frame, bg=yellow2_color, padx=40, pady=20)
books_display_frame.place(x=38, y=150, width=735, height=books_display_height)

# Button to get  books
search_button_image = Image.open(r"Images\audios\books button.jpeg")
search_button_image = search_button_image.resize((140, 50))
search_button_photo = ImageTk.PhotoImage(search_button_image)

search_button = Button(books_frame, image=search_button_photo, borderwidth=0, highlightthickness=0, command=display_books)
search_button.image = search_button_photo
search_button.place(x=340, y=115)

# ****************************************************************************************************
# movies Frame
available_height = 701 - 150  # Subtracting the space for navigation and other elements
movies_display_height = min(available_height, 4000)  # Ensure it doesn't exceed the available space

movies_frame = Frame(app_frame, width=824, height=701, bg=yellow_color)
movies_frame.place(x=276, y=0)

img = Image.open(r"Images\audios\movies frame.jpg")
photo = ImageTk.PhotoImage(img)
label = Label(movies_frame, image=photo, borderwidth=0, highlightthickness=0)
label.image = photo  
label.place(x=0, y=0)

# movies Display Frame
movies_display_frame = Frame(movies_frame, bg=yellow2_color, padx=40, pady=20)
movies_display_frame.place(x=38, y=150, width=735, height=movies_display_height)

# Button to get  movies
search_button_image = Image.open(r"Images\audios\movies button.jpeg")
search_button_image = search_button_image.resize((140, 50))
search_button_photo = ImageTk.PhotoImage(search_button_image)

search_button = Button(movies_frame, image=search_button_photo, borderwidth=0, highlightthickness=0, command=display_movies)
search_button.image = search_button_photo
search_button.place(x=340, y=115)

# ****************************************************************************************************
# potions Frame
potions_frame = Frame(app_frame, width=824, height=701, bg=yellow_color)
potions_frame.place(x=276, y=0)

img = Image.open(r"Images\audios\potions frame.jpg")
photo = ImageTk.PhotoImage(img)
label = Label(potions_frame, image=photo, borderwidth=0, highlightthickness=0)
label.image = photo  
label.place(x=0, y=0)

# Button to get  potions
search_button_image = Image.open(r"Images\audios\potions button.jpeg")
search_button_image = search_button_image.resize((170, 70))
search_button_photo = ImageTk.PhotoImage(search_button_image)

search_button = Button(potions_frame, image=search_button_photo, borderwidth=0, highlightthickness=0, command=get_random_potion)
search_button.image = search_button_photo
search_button.place(x=320, y=120)

#image frame
potions_image_frame = Frame(potions_frame, bg=blue_color)
potions_image_frame.place(x=70, y=240, width=299, height=383)

potions_image_label = Label(potions_image_frame, bg=yellow3_color)
potions_image_label.place(x=6, y=6, width=287, height=371)

# image of the potions will be placed

#potions info frame
potions_info_border = Frame(potions_frame, bg=blue_color)
potions_info_border.place(x=400, y=240, width=316, height=366)

potions_info_frame = Frame(potions_info_border, bg=yellow3_color)
potions_info_frame.place(x=7, y=7, width=300, height=350)

info_heading = Label(potions_info_frame,text="~ Potions Information ~", bg=yellow3_color, fg=blue_color,
                        font=text_font2, justify=CENTER)
info_heading.place(x=25, y=15)

potion_name_heading = Label(potions_info_frame,text="Potion Name:", bg=yellow3_color, fg=blue_color,
                        font=text_font5, justify=LEFT)
potion_name_heading.place(x=10, y=90)

potion_name_label = Label(potions_info_frame,text="", bg=yellow3_color, fg=blue2_color,
                        font=text_font4, justify=LEFT)
potion_name_label.place(x=30, y=130)

potion_effect_heading = Label(potions_info_frame,text="Potion Effect:", bg=yellow3_color, fg=blue_color,
                        font=text_font5, justify=LEFT)
potion_effect_heading.place(x=10, y=180)

potion_effect_label = Label(potions_info_frame,text="", bg=yellow3_color, fg=blue2_color,
                        font=text_font4, justify=LEFT, wraplength=250)
potion_effect_label.place(x=20, y=220, width=250)

# Status Label
status_label = Label(potions_frame, text="", font=text_font4, bg=yellow2_color, fg=blue_color)
status_label.place(x=330, y=195)  # Adjust the position as needed


# Set the initial visible frame
raise_frame(landing_page)

root.mainloop()