from tkinter import *               # importing tkinter
from tkinter import font            # importing fonts
from PIL import ImageTk, Image      # importing the ImageTk and Image from PIL (python image library) to process images
import requests                     # importing the requests library for making HTTP requests to APIs
from io import BytesIO              # importing BytesIO for handling binary data in memory
import random                       # importing random to generate random choices and data
import pygame                       # importing pygame to add a background music to the gui

# function to automatically play background  music
def play_music():
    # Initialize Pygame Mixer
    pygame.mixer.init()
    # Load your music file
    pygame.mixer.music.load(r'Images and Audio\Harry Potter Main Theme Slowed Down (Extended 1H).mp3')
    # Play the music, -1 for looping indefinitely
    pygame.mixer.music.play(-1)

# calling the function to start playing the background music
play_music()

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

# creating a raise frame function to raise specific frames
def raise_frame(frame):
    frame.tkraise()

# Creating a start button click function to raise the appframe, navigation frame and the instruction frame
def start_button_click():
    raise_frame(app_frame)
    raise_frame(navigation_frame)
    raise_frame(instruction_frame)

# creating a function to raise instruction frame when instruction button is clicked
def instruction_button_click():
    raise_frame(instruction_frame)
    # Reset the style of other navigation buttons
    character_button.config(fg=yellow_color, bg=blue2_color)
    books_button.config(fg=yellow_color, bg=blue2_color)
    movies_button.config(fg=yellow_color, bg=blue2_color)
    potions_button.config(fg=yellow_color, bg=blue2_color)

# creating a function to raise character frame when character button is clicked
def character_click():
    raise_frame(character_frame)

    # Change the style of the character button to indicate it's the active page
    character_button.config(fg=blue_color, bg=yellow2_color)

    # Reset the style of other navigation buttons
    books_button.config(fg=yellow_color, bg=blue2_color)
    movies_button.config(fg=yellow_color, bg=blue2_color)
    potions_button.config(fg=yellow_color, bg=blue2_color)

# creating a function to raise books frame when books button is clicked
def books_button_click():
    raise_frame(books_frame)

    # Change the style of the Books button to indicate it's the active page
    books_button.config(fg=blue_color, bg=yellow2_color)

    # Reset the style of other navigation buttons
    character_button.config(fg=yellow_color, bg=blue2_color)
    movies_button.config(fg=yellow_color, bg=blue2_color)
    potions_button.config(fg=yellow_color, bg=blue2_color)

# creating a function to raise movies frame when movies button is clicked
def movies_button_click():
    raise_frame(movies_frame)

    # Change the style of the Books button to indicate it's the active page
    movies_button.config(fg=blue_color, bg=yellow2_color)

    # Reset the style of other navigation buttons
    character_button.config(fg=yellow_color, bg=blue2_color)
    books_button.config(fg=yellow_color, bg=blue2_color)
    potions_button.config(fg=yellow_color, bg=blue2_color)

# creating a function to raise potions frame when potions button is clicked
def potions_button_click():
    raise_frame(potions_frame)

    # Change the style of the Books button to indicate it's the active page
    potions_button.config(fg=blue_color, bg=yellow2_color)

    # Reset the style of other navigation buttons
    character_button.config(fg=yellow_color, bg=blue2_color)
    books_button.config(fg=yellow_color, bg=blue2_color)
    movies_button.config(fg=yellow_color, bg=blue2_color)


# *****************************************************************************************************************
# books data retrieval code

image_references = []

# creating a function to retrieve and display the books data
def display_books():
    # global variables
    global books_display_frame
    global image_references

    # storing the api's url in a variable
    api_url = "https://api.potterdb.com/v1/books"
    try: # getting the data
        response = requests.get(api_url)
        data = response.json()
        books = data['data']
    except Exception as e: # error message if data is not retrieved successfully
        print("Error geting or parsing book data:", e)
        return  

    # destroying all previous widgets
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

    # creating books container
    books_container = Frame(book_canvas, bg=yellow2_color)
    book_canvas.create_window((0, 0), window=books_container, anchor='nw')

    container_height = 0 # setting a specific height
    
    image_references.clear() # clearing the reference image

    title_width = 320  # setting a specific title width
    summary_width = 500  # setting a specific summary width

    # using for loop to print the data
    for i, book_data in enumerate(books):
        try:
            cover_url = book_data['attributes']['cover'] # getting the cover image
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

            # Increasing the width of the title label
            title_lbl = Label(books_container, text=book_data['attributes']['title'], font=text_font4, 
                              fg=blue_color, bg=yellow2_color)
            title_lbl.place(x=90, y=i*180, width=title_width, height=20)

            # Increasing the width of the summary label and adjust wraplength accordingly
            summary_lbl = Label(books_container, text=book_data['attributes']['summary'], font=('New York Times', 8), 
                                fg=blue_color, wraplength=summary_width, justify='left', bg=yellow2_color)
            summary_lbl.place(x=90, y=i*180 + 30, width=summary_width, height=100)


            container_height = i * 180 + 180  # Adjusting the height based on the number of books

            image_references.append(cover_photo)  # Storing a reference
            print(f"Added book {i} to the canvas") # console message while loading
        except Exception as e: 
            print("Error loading book data:", e)

            print(f"Processing book {i}: {book_data['attributes']['title']}")

    # book container and canvas configuration
    books_container.config(width=800, height=container_height)  # Set a fixed width and dynamic height
    books_container.update_idletasks() # updating gui
    book_canvas.config(scrollregion=book_canvas.bbox("all")) # setting scroll region to all

    # console message for debugging
    print("Books container size:", books_container.winfo_width(), books_container.winfo_height())
    print("Canvas scroll region:", book_canvas.cget("scrollregion"))


# ****************************************************************************************************************
# movies data 
image_references = []

# creating a function to retrieve and display the movies data
def display_movies():
    # global variables
    global movies_display_frame
    global image_references

    # storing the api's url in a variable
    api_url = "https://api.potterdb.com/v1/movies"
    try: # getting the data
        response = requests.get(api_url)
        data = response.json()
        movies = data['data']
    except Exception as e: # error message if data retrieval is unsuccessful
        print("Error retrieving or parsing movie data:", e)
        return  

    # destroying previous widgets
    for widget in movies_display_frame.winfo_children():
        widget.destroy()

    # creating canvas
    canvas_frame = Frame(movies_display_frame, bg=blue_color, borderwidth=3, relief="solid")
    canvas_frame.place(x=0, y=0, relwidth=1, relheight=1)
    # styling the canvas
    movie_canvas = Canvas(canvas_frame, bg="white")
    movie_scrollbar = Scrollbar(canvas_frame, orient="vertical", command=movie_canvas.yview)
    movie_scrollbar.place(relx=0.97, rely=0, relwidth=0.03, relheight=1)
    movie_canvas.place(relx=0, rely=0, relwidth=0.97, relheight=1)
    movie_canvas.configure(yscrollcommand=movie_scrollbar.set)

    # creating a movies container frame
    movies_container = Frame(movie_canvas, bg=yellow2_color)
    movie_canvas.create_window((0, 0), window=movies_container, anchor='nw')

    container_height = 0 # setting a height
    image_references = [] # image reference list

    # setting specific widths and heights of the title and summaries
    title_width = 500
    summary_width = 500
    summary_height = 150
    poster_size = (80, 130)
    text_x_position = 100  # Increased to shift text to the right

    # getting and printing the data using for loop
    for i, movie_data in enumerate(movies):
        y_position = i * 250  # Adjusted for additional text
        try:
            # getting the movie poster
            poster_url = movie_data['attributes']['poster']
            poster_response = requests.get(poster_url)
            poster_img = Image.open(BytesIO(poster_response.content))
            poster_img = poster_img.resize(poster_size)

            # CREATING FRAME FOR POSTER
            poster_frame = Frame(movies_container, bg=blue_color, borderwidth=3, relief="solid")
            poster_frame.place(x=10, y=y_position, width=poster_size[0], height=poster_size[1])
            # using photo image to open and place the image
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
            # creating the summary heading label
            summary_heading_lbl = Label(movies_container, text="Summary:", font=text_font4, 
                                        fg=blue_color, bg=yellow2_color, anchor='w')
            summary_heading_lbl.place(x=text_x_position, y=summary_heading_y_position, width=title_width, height=20)

            # creating the Summary label
            summary_lbl_y_position = summary_heading_y_position + 25  # Adjusted Y position for summary text
            summary_lbl = Label(movies_container, text=movie_data['attributes']['summary'], font=('New York Times', 8), 
                                fg=blue_color, wraplength=summary_width, justify='left', bg=yellow2_color)
            summary_lbl.place(x=text_x_position, y=summary_lbl_y_position, width=summary_width, height=summary_height)

            container_height = y_position + 250 # container height adjustments

            print(f"Added movie {i} to the canvas") # console message while loading the data
        except Exception as e: # error message
            print("Error loading movie data:", e)

    # configuring the container
    movies_container.config(width=800, height=container_height)
    movies_container.update_idletasks() # updating the gui
    movie_canvas.config(scrollregion=movie_canvas.bbox("all")) # setting scroll region to all

    # debugging console message
    print("Movies container size:", movies_container.winfo_width(), movies_container.winfo_height())
    print("Canvas scroll region:", movie_canvas.cget("scrollregion"))

# ****************************************************************************************************************
# potions data 
# function to get random potions data
def get_random_potion():
    # configuring dtatus label to notify user about data retrieval while the data loads
    status_label.config(text="Retrieving Data...")
    root.update_idletasks() # updating the gui

    # storing the api url in a variable
    url = "https://api.potterdb.com/v1/potions"
    response = requests.get(url)
    if response.status_code == 200: # getting the data
        data = response.json()
        potions = data['data']

        # message if no potion is available
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

        # getting and setting the potion image
        potion_image_url = random_potion['attributes']['image']
        image_response = requests.get(potion_image_url)
        if image_response.status_code == 200:
            image = Image.open(BytesIO(image_response.content))
            image = image.resize((299, 383))  # Resize as needed
            image = ImageTk.PhotoImage(image)
            potions_image_label.config(image=image)
            potions_image_label.image = image
        status_label.config(text="")
    else: # error message
        status_label.config(text=f"Failed to retrieve data: {response.status_code}")

    # UPDATING THE GUI
    root.update_idletasks()

# ****************************************************************************************************************
# character data 
# function to retrieve and update the character data based on the character the user searches for
def search_character():
    search_name = search.get().lower()  # Retrieve user input and convert to lowercase

    # Storing the API url in a variable
    url = "https://api.potterdb.com/v1/characters?page[number]="

    # Using a for loop to iterate through all character API pages
    for page in range(1, 48):
        url_search = f"{url}{page}"
        response = requests.get(url_search)
        if response.status_code == 200:
            data = response.json()
            characters_list = data.get('data', [])

            # Looking for the required character
            for character in characters_list:
                name = character['attributes'].get('name', '').lower()
                if search_name in name:
                    # If the character is found, update the GUI
                    update_character_info(character)
                    return  # Stop searching after finding the character

        else:
            print(f"Failed to retrieve data from page {page}")

    # If no character is found
    character_name_label.config(text="Character not found")
    character_Gender_label.config(text="")
    character_born_label.config(text="")
    character_image_label.config(image='')  # Clear previous image
    status_label.config(text="")  # Clear the status message

# function to update the character info in the gui
def update_character_info(character):
    # Extract character information
    name = character['attributes'].get('name', '')
    gender = character['attributes'].get('gender', 'Not available')
    born = character['attributes'].get('born', 'Not available')
    image_url = character['attributes'].get('image', '')

    # Updating the labels
    character_name_label.config(text=name)
    character_Gender_label.config(text=gender)
    character_born_label.config(text=born)

    # getting and updating the character's image
    if image_url:
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            image = Image.open(BytesIO(image_response.content))
            image = image.resize((299, 383))
            image = ImageTk.PhotoImage(image)
            character_image_label.config(image=image)
            character_image_label.image = image  # Keep a reference
        else: # error message
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

# creating the landing page frame
landing_page = Frame(root, width=1100, height=700, bg=blue_color)
landing_page.place(x=0, y=0)

# Opening and resizing the image
img = Image.open(r'Images and Audio\landing page.png')
img = img.resize((1100, 700), Image.BOX)  # Resizing the image to fit the window without antialiasing

# Creating PhotoImage object from the resized image
resized_background_image = ImageTk.PhotoImage(img)

# Creating a label for the background image
background_label = Label(landing_page, image=resized_background_image)
background_label.place(relwidth=1, relheight=1)

# Load the image for the "Start" button
start_button_image = Image.open(r"Images and Audio\start-button.jpeg")
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

# adding the logo image to the navigation bar
img = Image.open(r"Images and Audio\main logo.jpeg")
img = img.resize((250, 130))
photo = ImageTk.PhotoImage(img)
label = Label(navigation_frame, image=photo, borderwidth=0, highlightthickness=0)
label.image = photo  
label.place(x=15, y=10)

# character frame button
character_button = Button(navigation_frame, text='Character       ', font=text_font2, fg=yellow_color, bg=blue2_color, 
                    bd=0, padx=70, pady=10, command=character_click)
character_button.place(x=0, y=180)

# books frame button
books_button = Button(navigation_frame, text='Books       ', font=text_font2, fg=yellow_color, bg=blue2_color, 
                    bd=0, padx=90, pady=10, command=books_button_click)
books_button.place(x=0, y=250)

# movies frame button
movies_button = Button(navigation_frame, text='Movies       ', font=text_font2, fg=yellow_color, bg=blue2_color, 
                    bd=0, padx=85, pady=10, command=movies_button_click)
movies_button.place(x=0, y=320)

# potions frame button
potions_button = Button(navigation_frame, text='Potions       ', font=text_font2, fg=yellow_color, bg=blue2_color, 
                    bd=0, padx=80, pady=10, command=potions_button_click)
potions_button.place(x=0, y=390)

# instruction page button
instruction_button_image = Image.open(r"Images and Audio\instructions button.jpeg")
instruction_button_image = instruction_button_image.resize((150, 50))
instruction_button_photo = ImageTk.PhotoImage(instruction_button_image)

instruction_button = Button(navigation_frame, image=instruction_button_photo, borderwidth=0, highlightthickness=0,command=instruction_button_click)
instruction_button.image = instruction_button_photo
instruction_button.place(x=55, y=480)

# Mute music button
mute_button_image = Image.open(r"Images and Audio\mute music button.jpeg")
mute_button_image = mute_button_image.resize((150, 50))
mute_button_photo = ImageTk.PhotoImage(mute_button_image)

# Unmute music button
unmute_button_image = Image.open(r"Images and Audio\unmute music button.jpeg")
unmute_button_image = unmute_button_image.resize((150, 50))  # Correct resizing
unmute_button_photo = ImageTk.PhotoImage(unmute_button_image)

# Mute button
mute_button = Button(navigation_frame, image=mute_button_photo, borderwidth=0, highlightthickness=0, command=toggle_sound)
mute_button.image = mute_button_photo
mute_button.place(x=55, y=540)


# instruction frame
instruction_frame = Frame(app_frame, width=824, height=701, bg=yellow_color)
instruction_frame.place(x=276, y=0)

# instruction frame image
img = Image.open(r"Images and Audio\instructions frame.png")
photo = ImageTk.PhotoImage(img)
label = Label(instruction_frame, image=photo, borderwidth=0, highlightthickness=0)
label.image = photo  
label.place(x=0, y=0)

# PLACING THE CREDITS IMAGE ON NAVBAR
img = Image.open(r"Images and Audio\name credit.png")
original_width, original_height = img.size

# Increase image width and height
new_width = int(original_width * 0.2)
new_height = int(original_height * 0.2)

# Resizing the image
img = img.resize((new_width, new_height))
photo = ImageTk.PhotoImage(img)
label = Label(navigation_frame, image=photo, borderwidth=0, highlightthickness=0)
label.image = photo  
label.place(x=0, y=610)


# ****************************************************************************************************
# Characters Frame
character_frame = Frame(app_frame, width=824, height=701, bg=yellow_color)
character_frame.place(x=276, y=0)

# character frame background image
img = Image.open(r"Images and Audio\characters frame.jpg")
photo = ImageTk.PhotoImage(img)
label = Label(character_frame, image=photo, borderwidth=0, highlightthickness=0)
label.image = photo  
label.place(x=0, y=0)

# search frame for bordered effect
search_border = Frame(character_frame, bg=blue_color)
search_border.place(x=70, y=140, width=500, height=60)

# Entry widget for searching
search = Entry(search_border, bg='white' , fg=blue_color, borderwidth=4,
               relief='flat', font=text_font2, justify=CENTER)
search.place(x=3, y=3, width=494, height=54)

# Button to search for a character
search_button_image = Image.open(r"Images and Audio\search-button.jpeg")
search_button_image = search_button_image.resize((150, 50))
search_button_photo = ImageTk.PhotoImage(search_button_image)

search_button = Button(character_frame, image=search_button_photo, borderwidth=0, highlightthickness=0,command=search_character)
search_button.image = search_button_photo
search_button.place(x=590, y=144)

#image frame
character_image_frame = Frame(character_frame, bg=blue_color)
character_image_frame.place(x=70, y=240, width=299, height=383)

character_image_label = Label(character_image_frame, bg=yellow3_color)
character_image_label.place(x=6, y=6, width=287, height=370)

# image of the character will be placed in the frame above

#character info frame
character_info_border = Frame(character_frame, bg=blue_color)
character_info_border.place(x=400, y=240, width=316, height=366)

character_info_frame = Frame(character_info_border, bg=yellow3_color)
character_info_frame.place(x=7, y=7, width=300, height=350)

# info heading
info_heading = Label(character_info_frame,text="Character Information", bg=yellow3_color, fg=blue_color,
                        font=text_font2, justify=CENTER)
info_heading.place(x=25, y=15)

#name heading
character_name_heading = Label(character_info_frame,text="Character Name:", bg=yellow3_color, fg=blue_color,
                        font=text_font5, justify=LEFT)
character_name_heading.place(x=10, y=60)

#name label
character_name_label = Label(character_info_frame,text="", bg=yellow3_color, fg=blue2_color,
                        font=text_font4, justify=LEFT)
character_name_label.place(x=30, y=90)

# gender heading
character_gender_heading = Label(character_info_frame,text="Gender:", bg=yellow3_color, fg=blue_color,
                        font=text_font5, justify=LEFT)
character_gender_heading.place(x=10, y=140)

# gender label
character_Gender_label = Label(character_info_frame,text="", bg=yellow3_color, fg=blue2_color,
                        font=text_font4, justify=LEFT)
character_Gender_label.place(x=20, y=200)

# born in heading
character_born_heading = Label(character_info_frame,text="Born In:", bg=yellow3_color, fg=blue_color,
                        font=text_font5, justify=LEFT)
character_born_heading.place(x=10, y=240)

# date of birth label
character_born_label = Label(character_info_frame,text="", bg=yellow3_color, fg=blue2_color,
                        font=text_font4, justify=LEFT, wraplength=250)
character_born_label.place(x=20, y=280, width=270)

# Status Label to notify the user that the data is being retrieved
status_label = Label(character_frame, text="", font=text_font4, bg=yellow2_color, fg=blue_color)
status_label.place(x=330, y=205) 


# ****************************************************************************************************
# books Frame
# Calculate the available height for the books_display_frame based on the window height
available_height = 701 - 150  # Subtracting the space for navigation and other elements
books_display_height = min(available_height, 4000)  # Ensure it doesn't exceed the available space

# books frame creation
books_frame = Frame(app_frame, width=824, height=701, bg=yellow_color)
books_frame.place(x=276, y=0)

# books frame background image
img = Image.open(r"Images and Audio\books frame.jpg")
photo = ImageTk.PhotoImage(img)
label = Label(books_frame, image=photo, borderwidth=0, highlightthickness=0)
label.image = photo  
label.place(x=0, y=0)

# Books Display Frame
books_display_frame = Frame(books_frame, bg=yellow2_color, padx=40, pady=20)
books_display_frame.place(x=38, y=150, width=735, height=books_display_height)

# Button to get  books
search_button_image = Image.open(r"Images and Audio\books button.jpeg")
search_button_image = search_button_image.resize((140, 50))
search_button_photo = ImageTk.PhotoImage(search_button_image)

search_button = Button(books_frame, image=search_button_photo, borderwidth=0, highlightthickness=0, command=display_books)
search_button.image = search_button_photo
search_button.place(x=340, y=115)

# ****************************************************************************************************
# movies Frame
available_height = 701 - 150  # Subtracting the space for navigation and other elements
movies_display_height = min(available_height, 4000)  # Ensure it doesn't exceed the available space

# movies frame creation
movies_frame = Frame(app_frame, width=824, height=701, bg=yellow_color)
movies_frame.place(x=276, y=0)

# movies frame background image
img = Image.open(r"Images and Audio\movies frame.jpg")
photo = ImageTk.PhotoImage(img)
label = Label(movies_frame, image=photo, borderwidth=0, highlightthickness=0)
label.image = photo  
label.place(x=0, y=0)

# movies Display Frame
movies_display_frame = Frame(movies_frame, bg=yellow2_color, padx=40, pady=20)
movies_display_frame.place(x=38, y=150, width=735, height=movies_display_height)

# Button to get  movies
search_button_image = Image.open(r"Images and Audio\movies button.jpeg")
search_button_image = search_button_image.resize((140, 50))
search_button_photo = ImageTk.PhotoImage(search_button_image)

search_button = Button(movies_frame, image=search_button_photo, borderwidth=0, highlightthickness=0, command=display_movies)
search_button.image = search_button_photo
search_button.place(x=340, y=115)

# ****************************************************************************************************
# potions Frame
# creating the frame for potions
potions_frame = Frame(app_frame, width=824, height=701, bg=yellow_color)
potions_frame.place(x=276, y=0)

# potions frame background image
img = Image.open(r"Images and Audio\potions frame.jpg")
photo = ImageTk.PhotoImage(img)
label = Label(potions_frame, image=photo, borderwidth=0, highlightthickness=0)
label.image = photo  
label.place(x=0, y=0)

# Button to get  potions
search_button_image = Image.open(r"Images and Audio\potions button.jpeg")
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

# image of the potions will be placed in the frame above

#potions info frame
potions_info_border = Frame(potions_frame, bg=blue_color)
potions_info_border.place(x=400, y=240, width=316, height=366)

# inner frame for bordered effect
potions_info_frame = Frame(potions_info_border, bg=yellow3_color)
potions_info_frame.place(x=7, y=7, width=300, height=350)

# info heading
info_heading = Label(potions_info_frame,text="~ Potions Information ~", bg=yellow3_color, fg=blue_color,
                        font=text_font2, justify=CENTER)
info_heading.place(x=25, y=15)

# potion name heading 
potion_name_heading = Label(potions_info_frame,text="Potion Name:", bg=yellow3_color, fg=blue_color,
                        font=text_font5, justify=LEFT)
potion_name_heading.place(x=10, y=90)

# potion name data label
potion_name_label = Label(potions_info_frame,text="", bg=yellow3_color, fg=blue2_color,
                        font=text_font4, justify=LEFT)
potion_name_label.place(x=30, y=130)

# potion effect heading
potion_effect_heading = Label(potions_info_frame,text="Potion Effect:", bg=yellow3_color, fg=blue_color,
                        font=text_font5, justify=LEFT)
potion_effect_heading.place(x=10, y=180)

# potion effect data label
potion_effect_label = Label(potions_info_frame,text="", bg=yellow3_color, fg=blue2_color,
                        font=text_font4, justify=LEFT, wraplength=250)
potion_effect_label.place(x=20, y=220, width=250)

# Status Label to notify the user that the data is being retrieved
status_label = Label(potions_frame, text="", font=text_font4, bg=yellow2_color, fg=blue_color)
status_label.place(x=330, y=195) 


# Setting  the initial visible frame to the landing frame
raise_frame(landing_page)

# initiating the gui
root.mainloop()