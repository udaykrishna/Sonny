#
#   Surya Teja Cheedella
#       BITS Pilani, Hyderabad Campus
#

from tkinter import *
from tkinter import ttk
import requests, json
import random
# import subprocess as sub
# p = sub.Popen('main.py', stdout=sub.PIPE, stderr=sub.PIPE)
# output, errors = p.communicate()

wish_words= ["happy", "hapie", "happie", "bday", "birthday", "returns"]
thank_words= ["Thank you :) ", "Thanks :D ", "Thank you so much for your wishes :) ",
                "Thank you for your warm wishes :) "]

output_file= open("wishes.txt", "w")

def output_to_widget(message):
    text_out.insert(INSERT, message)
    root.update_idletasks()

def get_posts(token):
    parameters = {'access_token': token}
    try:
        r = requests.get('https://graph.facebook.com/me/feed?limit=5', params=parameters)
    except:
        output_to_widget("Unable to get date. Check your internet connection and try again!")
        return "no data"
    if r.status_code== 200:
        result = json.loads(r.text)
        return result['data']
    else:
        output_to_widget("Unable to get data. Check your access_token and make sure if session is still valid.\n")
        return "no data"


def is_birthday(created_date, birthday):
    date= created_date[5:]
    birthday_p_1= birthday[:3]+ str(int(birthday[3:])+ 1)
    if len(birthday_p_1)!= 5:
        birthday_p_1= birthday_p_1[:3]+ "0"+ birthday_p_1[3:]
    birthday_m_1= birthday[:3]+ str(int(birthday[3:])- 1)
    if len(birthday_m_1)!= 5:
        birthday_m_1= birthday_m_1[:3]+ "0"+ birthday_m_1[3:]
    #print(date, birthday, birthday_p_1, birthday_m_1)

    if date== birthday or date== birthday_m_1 or date== birthday_p_1:
        return True

    return False

def is_wish(message):
    message= message.lower()
    for word in wish_words:
        if word in message:
            return True

    return False

def like_post(id, token):
    #print(id)
    id= id.split("_")[1]
    #print(id)

    url= "https://graph.facebook.com/%s/likes" % (id)
    params= {"access_token": token}
    posted= requests.post(url, data= params)
    if posted.status_code== 200:
        return True

    return False

def comment_post(id, token, name):
    #print(id)
    id= id.split("_")[1]
    #print(id)

    my_thank_word= thank_words[random.randint(0, len(thank_words))]
    url= "https://graph.facebook.com/%s/comments" % (id)
    params= {"access_token": token, "message": my_thank_word+ name}
    posted= requests.post(url, data= params)
    if posted.status_code== 200:
        return True

    return False

def save_post(name, message):
    try:
        output_to_widget(name+ ": "+ message+ "\n")
        output_file.write(name+ ": "+ message)
        output_file.write("\n")

        return True
    except:
        return False

def process_data(access_token, birthday, like, comment, save):
    output_to_widget("Starting to request timeline feed from facebook...\n")
    posts_data= get_posts(access_token)
    if posts_data== "no data":
        return
    output_to_widget("Successfully fetched "+ str(len(posts_data))+ " posts from your timeline.\n")
    
    for post in posts_data:
        try:
            #print(json.dumps(post, indent= 2))
            if is_birthday(post["created_time"][:10], birthday):
                # output_to_widget("is birthday\n")
                if is_wish(post["message"]):
                    # output_to_widget("is wish\n")
                    if like:
                        done_like= like_post(post["id"], access_token)
                        if done_like:
                            output_to_widget("Liked wish from "+ post["from"]["name"]+ "\n")
                    if comment:
                        done_comment= comment_post(post["id"], access_token, post["from"]["name"])
                        if done_comment:
                            output_to_widget("Commented on wish from "+ post["from"]["name"]+ "\n")
                    if save:
                        done_save= save_post(post["from"]["name"], post["message"])
                        if done_save:
                            output_to_widget("Saved wish from "+ post["from"]["name"]+ "\n")

        except:
            pass


def validate_values(*args):
    text_out.delete(1.0, INSERT)
    try:
        access_token= str(access_token_value.get())
        #print(access_token)
        if access_token== "":
            output_to_widget("Please enter access token.\n")
            return
    except:
        output_to_widget("Please check the value entered in access token field!\n")
        return

    try:
        birthday= str(date_value.get())
        #print(birthday)
        if birthday== "":
            output_to_widget("Please enter your birthday.\n")
            return
        month, date= birthday.split("-")
        if len(date)!= 2 or len(month)!= 2:
            output_to_widget("Please check the value entered in birthday date field!\n")
            return
        #print(date, month)
    except:
        output_to_widget("Please check the value entered in birthday date field!\n")
        return

    like= like_value.get()
    #print(like)

    comment= comment_value.get()
    #print(comment)

    save= save_value.get()
    #print(save)

    process_data(access_token, birthday, like, comment, save)

root = Tk()
root.title("Sonny- Automatically responds to birthday wishes")


mainframe = ttk.Frame(root, padding="10 10 10 7")
mainframe.grid(column=0, row=0, sticky=(N, W, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

access_token_value = StringVar()
date_value = StringVar()

ttk.Label(mainframe, text="Enter the access token: ").grid(column=1, row=1, sticky=W)
access_token_entry = ttk.Entry(mainframe, width=37, textvariable=access_token_value)
access_token_entry.grid(column=2, row=1, sticky=(W))

ttk.Label(mainframe, text="Enter your birthday (MM-DD): ").grid(column=1, row=2, sticky=W)
date_entry = ttk.Entry(mainframe, width=15, textvariable=date_value)
date_entry.grid(column=2, row=2, sticky=(W))

like_value = IntVar()
comment_value = IntVar()
save_value = IntVar()

ttk.Label(mainframe, text="Like the birthday wish").grid(column=1, row=3, sticky=W)
like_check = ttk.Checkbutton(mainframe, text='', variable=like_value)
like_check.grid(column=2, row=3, sticky=(W))

ttk.Label(mainframe, text="Comment on the birthday wish").grid(column=1, row=4, sticky=W)
comment_check = ttk.Checkbutton(mainframe, text='', variable=comment_value)
comment_check.grid(column=2, row=4, sticky=(W))

ttk.Label(mainframe, text="Save the wishes to a text file").grid(column=1, row=5, sticky=W)
save_check = ttk.Checkbutton(mainframe, text='', variable=save_value)
save_check.grid(column=2, row=5, sticky=(W))

ttk.Button(mainframe, text="Start", command=validate_values).grid(column=2, row=6, sticky=E)

for child in mainframe.winfo_children():
    child.grid_configure(padx=9, pady=5)

smallframe = ttk.Frame(root, padding="10 10 10 7")
smallframe.grid(column=0, row=1, sticky=(N, W, E, S))
smallframe.columnconfigure(0, weight=1)
smallframe.rowconfigure(0, weight=1)

text_out = Text(smallframe, height= 10, width= 70)
text_out.grid(padx= 5, pady= 5)
scrl = Scrollbar(smallframe, command=text_out.yview)
text_out.config(yscrollcommand=scrl.set)
scrl.grid(row=0, column=1, sticky='n s')

# text_out.insert(INSERT, output)

access_token_entry.focus()
root.bind('<Return>', validate_values)

root.mainloop()
