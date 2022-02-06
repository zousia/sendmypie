# author: Isabelle MARECHE
# date: 2022-02-06
# purpose: re-usable class to send email messages 
#          with variables and images in html body

import os
import smtplib
import email
from email.policy import default
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from string import Template

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SendMyPie:
    # list of messages to pass to method open_send_close
    messages_to_send = []
    
    def __init__(self, name='instance'):  
        self.name = name
        
    def get_messages_to_send(self):
        print(f"Total : {len(self.messages_to_send)}")
        return self.messages_to_send

    def make_email_body_with_img(self, exp, emails_addresses, 
                                 subject, file_template_path, 
                                 email_plus_addr=None, 
                                 html_variables={}, 
                                 imgs_directory=None, 
                                 images_data=[]):
        """
        Method to construct the email message with encoded 64 images in html body

        Parameters:
        exp_name (str): Name to present the expeditor
        emails_addresses (list(str)): Original emails addresses
        email_plus_addr (str): Additional arg for email further fitering 
                                ex: if emails_addresses = firstname.lastname@domain.com
                                and email_plus_addr = hobby
                                the resulting email address will be firstname.lastname+hobby@domain.com
        subject (str): The title for the email
        file_template_path (path): The path of the file with the html template 
        html_variables (dict): Variables to feel html template with the corresponding keys with coresponfing string literal in html ${name_key_variable}
        imgs_directory (path): The directory where are images
        images_data (list(path)): List of the relative paths of the images to include in the html body


        Returns:
        email.email.message: The email data to send with send_message() function from smtplib

        """

        if imgs_directory == None:
            imgs_directory=os.getcwd()
        my_subject = subject
        my_dest = [] # list to store formatted emails_addresses after traitement

        for email_address in emails_addresses:                   
            # if an additional part for the eamil address is supplied
            # split address to insert it at the right place
            if email_plus_addr != None:
                email_localpart, email_domain = email_address.split("@")
                format_adrr = f'{email_localpart}+{email_plus_addr}@{email_domain}'
            else:
                format_adrr = email_address
            # add this email address to the list of desired receivers
            my_dest.append(format_adrr) #= [f"{format_adrr}", ] 
        
        print(f"prepare mail to dest : {my_dest}")

        # get html template for the body of the email
        file_template = open(file_template_path, "r")

        if html_variables:
            html_message = Template(file_template.read()).substitute(html_variables)
        else:
            html_message = str(file_template.read())
            
       
        # create multiparts mixed as a global container
        msg = MIMEMultipart('mixed')
        msg['From'] = str(exp)
        msg['To'] = my_dest[0]
        msg['Subject'] = my_subject

        # create multipart alternatives container for text and/or html parts
        alternatives = MIMEMultipart(_subtype='alternative', _subparts=[])
        # link it to the global container
        msg.attach(alternatives)

        # create html part
        html_part = MIMEMultipart(_subtype='related', _subparts=[])
        # link it to the multipart alternatives container
        alternatives.attach(html_part)

        # create body utf8
        body_html = MIMEText(html_message, _subtype="html")
        body_html.set_charset("UTF-8")
        # link it to the html_part related container
        html_part.attach(body_html)

        # save current dir to be able to get back in after getting images
        save_current_dir = os.getcwd()
        # change dir to be in the right place to work with images files

        os.chdir(imgs_directory)
        print(f"changing directory to : {os.getcwd()}")

        for image_fulname in images_data:
            print(f"image fulname : {image_fulname}")
            # get images and put them in variables
            image_data = open(image_fulname, 'rb').read()

            fn, extension = image_fulname.split('.')
            # create mime type for the images
            new_img = MIMEImage(_imagedata=image_data, _subtype=extension, name=os.path.basename(image_fulname))

            # link the images to the html_part related container
            html_part.attach(new_img)

            # add headers for each image
            new_img.add_header(_name='Content-Disposition', _value='inline', filename=os.path.join(image_fulname))
            new_img.add_header('Content-ID', f'<{image_fulname}>')       

        # get back to where you have to be to continue the job
        os.chdir(save_current_dir)
        print(f"changing directory to : {os.getcwd()}")
        print(f"msg : {msg}")
        self.messages_to_send.append(msg)

        return self.messages_to_send


    def open_send_close(self, EMAIL_HOST_USER=None, 
                                         EMAIL_HOST_PASSWORD=None,EMAIL_HOST='smtp.gmail.com', 
                                         EMAIL_PORT=587, list_messages=[]):
        """
        Method to open an smtp connection, send emails from a list and close connection when it is done

        Parameters (): 
        EMAIL_HOST (smtp server): default to 'smtp.gmail.com'
        EMAIL_PORT (int): 587
        EMAIL_HOST_USER (str): Email address from witch to connect 
        EMAIL_HOST_PASSWORD (str): Password for authentication to this account
        list_messages (list(email.email.message)): List of the emails to send

        Returns:
        Logged in connection to smtp server, ready to use to send email
        """

        # connect to actual host on actual port
        smtp = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        # smtp.set_debuglevel(1)
        smtp.starttls()

        # check if socket is open
        try:
            smtp.sock
            print(f"smtp socked {smtp.sock}")
            # get authenticated
            my_response = smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            print(f"smtp login response {my_response}")
            
            
            if list_messages:
                k = len(list_messages)
                for msg in list_messages:
                    my_response = smtp.send_message(msg)
                    k -= 1
                    print(f"sended 1 msg ; remaining msg to send {k}")
                    self.messages_to_send.remove(msg)
            else:
                print(f"list messages empty {list_messages}")

            self.get_messages_to_send()

            # close connection
            smtp.quit()
            print(f"closed smtp connection")

        except smtplib.SMTPException as e:
            logger.error(f"ERROR SMTP CONNECTION RESPONSE :{e}")


