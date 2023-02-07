from tkinter import *
from tkinter import messagebox
import random
import pyperclip
from cryptography.fernet import Fernet
import json

# --------------------------- ENCRYPTION ------------------------------- #

# key generation
key = Fernet.generate_key()

def encrypt():
  key = Fernet.generate_key()
  # string the key in a file
  with open('filekey.key', 'wb') as filekey:
    filekey.write(key)


  # opening the key
  with open('filekey.key', 'rb') as filekey:
      key = filekey.read()
  
  # using the generated key
  fernet = Fernet(key)
  
  # opening the original file to encrypt
  with open('data.json', 'rb') as file:
      original = file.read()
      
  # encrypting the file
  encrypted = fernet.encrypt(original)
  
  # opening the file in write mode and
  # writing the encrypted data
  with open('Encrypted.txt', 'wb') as encrypted_file:
      encrypted_file.write(encrypted)


# using the key
def decrypt():
  with open('filekey.key', 'rb') as f:
     key = f.read()
  fernet = Fernet(key)
  
  # opening the encrypted file
  with open('Encrypted.txt', 'rb') as enc_file:
      encrypted = enc_file.read()
  
  # decrypting the file
  decrypted = fernet.decrypt(encrypted)
  
  # opening the file in write mode and
  # writing the decrypted data
  with open('Decrypted.txt', 'wb') as dec_file:
      dec_file.write(decrypted)


# --------------------------- PASSWORD GENERATOR ------------------------------- #
#Password Generator Project

def generate_password():
  letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
  numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
  symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

  nr_letters = random.randint(8, 10)
  nr_symbols = random.randint(2, 4)
  nr_numbers = random.randint(2, 4)

  password_letters = [random.choice(letters) for _ in range(nr_letters)]
  password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
  password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

  password_list = password_letters + password_numbers + password_symbols

  random.shuffle(password_list)

  password = "".join(password_list)

  Password_Entry.insert(0,password)
  pyperclip.copy(password)

# ---------------------------- SEARCH PASSWORD DATABASE ------------------------------- #

def find_password():
    web=Website_Entry.get()
    try:
        with open("data.json") as datafile:
            data = json.load(datafile)
    except FileNotFoundError:
        messagebox.showinfo(title="Error",message = "No data File Found")
    else:
        if web in data:
            email = data[web]["email"]
            password = data[web]["password"]
            messagebox.showinfo(title=web, message = f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title=web, message = f"{web} Credentials not found") 



# ---------------------------- SAVE PASSWORD ------------------------------- #

def add(): 

    website = Website_Entry.get()
    email = Email_Entry.get()
    password = Password_Entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                #Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            #Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                #Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            Website_Entry.delete(0, END)
            Password_Entry.delete(0, END)



# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx = 20, pady = 20)

canvas = Canvas(width=200, height = 200)
logo_img = PhotoImage(file= "logo.png")
canvas.create_image(100, 100, image = logo_img)
canvas.grid(row = 0,column = 2)


#Labels
Website_Label = Label(text = "Website:")
Email_Label = Label(text = "E-mail/Username")
Password_Label = Label(text = "Password")

Password_Label.grid(row = 3, column = 0)
Email_Label.grid(row = 2, column = 0)
Website_Label.grid(row = 1, column = 0)

#Entries
Website_Entry = Entry(width = 35)
Email_Entry = Entry(width = 35)
Password_Entry = Entry(width = 35)
Email_Entry.insert(0,"Dummy@email.com")

Website_Entry.focus()

Email_Entry.grid(row = 2, column = 1, columnspan = 2)
Website_Entry.grid(row = 1, column = 1, columnspan = 2)
Password_Entry.grid(row = 3, column = 1, columnspan = 2)

#Buttons
Password_Button = Button(text = "Generate Password", command = generate_password)
Add_Button = Button(text = "Add", width = 36, command = add)
Decrypt_Button = Button(text = "Decrypt", command = decrypt)
Encrypt_Button = Button(text = "Encrypt", command = encrypt)
search_button = Button(text="Search",width = 13, command=find_password)

search_button.grid(row=1, column=3)
Decrypt_Button.grid(row = 5, column = 1)
Encrypt_Button.grid(row = 5, column = 2)
Password_Button.grid(row = 3, column = 3)
Add_Button.grid(row = 4, column = 1, columnspan = 2)

window.mainloop()