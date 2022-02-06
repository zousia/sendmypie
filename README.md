# SENDMYPIE #

    Module to send html templated emails fulfilled with variables using Python script  

---

## How to use this Python 3 module ##

### Basic use ###

You may feel free to use the __.make_email_body_with_img(*args, **kwargs)__ method in a for loop if you have several dest to whom you want to send an email, or several emails to send to the same dest(s).  

All the html files passed to the method will be stored in a list which you will be able to pass as a parameter to the class method __.open_send_close(*args, **kwargs)__.  

### 1. Call the class method from whithin your images' directory to make the email body with the html template and other parameters ###  

```python
from sendmypie.core_module import *

sendmypie = SendMyPie()
sendmypie.make_email_body_with_img(
                            exp="DISPLAYED NAME FOR YOUR EXP",  
                            emails_addresses=["dest_firstname.dest_lastname@domain.com",],  
                            subject="Subject title for the email",  
                            file_template_path="/the/path/to/our/template_email.html",  
                            images_data=['name_img1.png', 'name_img2.png', ]  
                            )  
```

### 2. Assigne the all list of prepared emails in a local variable to use it as a parameter with the next class method ###  

```python
list_to_send = sendmypie.get_messages_to_send()
```

### 3. Open connection with your mailbox, send your email(s) and close connection: ###  

The default __EMAIL_HOST__ is set to Gmail, and the default __EMAIL_PORT__ set to 587.  
You can change it to fit your needs by passing these parameters to the class method.

In your Google Account > Security > Activate Less secure app access and in your Gmail Parameters > Transfert and POP/IMAP > Activate IMAP

```python
sendmypie.open_send_close(EMAIL_HOST_USER="sender_name@domain.com",  
                                         EMAIL_HOST_PASSWORD="sender_password",  
                                         list_messages=list_to_send)
```

---  

### For a little more advanced use ###

### A. If your images are stored in another directory on the same host ###  

Add a __imgs_directory__ parameter when you call the class method.  

ex: imgs_directory="/the/path/to/our/images/directory"

```python
sendmypie.make_email_body_with_img(
                            exp="DISPLAYED NAME FOR YOUR EXP",  
                            emails_addresses=["dest_firstname.dest_lastname@domain.com",],  
                            subject="Subject title for the email",  
                            file_template_path="/the/path/to/our/template_email.html",  
                            imgs_directory='/the/path/to/our/images/directory',  
                            images_data=['name_img1.png', 'name_img2.png', ]  
                            ) 
```


### B. To add a "+" string in the dest email address in order to make filtering easier in the dest mailbox ###  

Add a __email_plus_addr__ parameter when you call the class method.  

ex: email_plus_addr="personalstuff" will be transformed into "dest_firstname.dest_lastname+personalstuff@domain.com"

```python
sendmypie.make_email_body_with_img(
                            exp="DISPLAYED NAME FOR YOUR EXP",  
                            emails_addresses=["dest_firstname.dest_lastname@domain.com",],  
                            subject="Subject title for the email",  
                            file_template_path="/the/path/to/our/template_email.html",  
                            email_plus_addr="personalstuff", 
                            imgs_directory='/the/path/to/our/images/directory',  
                            images_data=['name_img1.png', 'name_img2.png', ]  
                            ) 
```

### C. If you want to send an email with variables in the html part ###  
    * Make sure that the variables has been written in literal string format in the html file *  
    * And prefix images src by "cid:" *

```html
<html>
    <head></head>
    <body>
        <div>${key_variable1}</div>
        <img src="cid:name_img1.jpg" alt="name_img1">
        <div>${key_variable2}</div>
        <img src="cid:name_img2.jpg" alt="name_img2">
    </body>
</html>
```

Append the html_variable dict to parameters when calling the class method:

```python
sendmypie.make_email_body_with_img(
                            exp="DISPLAYED NAME FOR YOUR EXP",  
                            emails_addresses=["dest_firstname.dest_lastname@domain.com",],  
                            subject="Subject title for the email",  
                            file_template_path="/the/path/to/our/template_email.html",  
                            email_plus_addr="personalstuff",  
                            html_variables = {
                                "key_variable1": "value_variable1", 
                                "key_variable2": "value_variable2", 
                            },
                            imgs_directory='/the/path/to/our/images/directory',  
                            images_data=['name_img1.png', 'name_img2.png', ]  
                            ) 
```