import os
import time
import smtplib
import email
import re
from sty import fg, bg, rs # for colors in print
from email.policy import default
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from string import Template

import logging
from sendmypie.settings import logging_config
logger = logging.getLogger(__name__)


class SendMyPie:
    # list of messages to pass to method open_send_close
    messages_to_send = []
    
    def __init__(self, name='instance'):  
        self.name = name
        
    def get_messages_to_send(self):
        #print(f"Total : {len(self.messages_to_send)}")
        logger.info(f"Total : {len(self.messages_to_send)}")
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
        logger.info(f"prepare mail to dest : {my_dest}")
        logger.info(f"template path : {file_template_path}")
        logger.info(f"html_variables : {html_variables}")
        logger.info(f"images dir : {imgs_directory}")
        

        # get html template for the body of the email
        file_template = open(file_template_path, "r")

        if html_variables:
            html_message = Template(file_template.read()).substitute(html_variables)
        else:
            html_message = str(file_template.read())

        # create multiparts mixed as a global container
        msg = MIMEMultipart('mixed')
        msg['From'] = str(exp)
        # visible email adress will be the first in the list (you can set it to the email exp)
        msg['To'] = my_dest[0]
        # invisible email adresses
        msg['Bcc'] = ', '.join(my_dest)
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
        #print(f"changing directory to : {os.getcwd()}")

        for image_fulname in images_data:
            # print(f"image fulname : {image_fulname}")
            logger.info(f"image fulname : {image_fulname}")

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
        # print(f"changing directory to : {os.getcwd()}")
        # print(f"msg : {msg}")
        logger.debug(f"msg : {msg}")
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
            #print(f"smtp socked {smtp.sock}")
            logger.debug(f"smtp socked {smtp.sock}")
            # get authenticated
            my_response = smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            print(f"smtp login response {my_response}")
            logger.info(f"smtp login response {my_response}")

            if len(list_messages) >= 1:
                k = len(list_messages)
                for msg in list_messages:
                    my_response = smtp.send_message(msg)
                    k -= 1
                    print(f"sended 1 msg ; remaining msg to send {k}")
                    logger.debug(f"sended 1 msg ; remaining msg to send {k}")
            else:
                print(f"list messages empty {list_messages}")
                logger.debug(f"list messages empty {list_messages}")

            # close connection
            smtp.quit()
            print(f"closed smtp connection")
            logger.debug(f"closed smtp connection")
            time.sleep(5)

        except smtplib.SMTPException as e:
            logger.error(f"ERROR SMTP CONNECTION RESPONSE :{e}")

        finally:
            return "DONE"


def update_add_more():
    try:
        updated_add_more = int(input(f"{bg.black} {fg.li_red}Add another (0 to quit)? {fg.rs} {bg.rs}\n"))
        return updated_add_more
    except Exception as e:
        return e


def enter_email(addr="", add_more=True):
    add_more = add_more
    addr = addr
    emails_addresses = []
    # regex to validate email format
    consensus_email_reg = '(?i)(\w*(\w*|[\-|\.|_])(\w*|[\-|\.|_])\w)*@(\w*(\w*|[\-|\.|_])(\w*|[\-|\.|_])\w)*\.\w{2,3}$'

    # if addr is in params (for tests)
    if addr != "":
        # if there is a list of several addresses
        if type(addr) == list:
            for single_ad in addr:
                if re.match(consensus_email_reg, single_ad):
                    emails_addresses.append(single_ad)
        # if there is one single email address
        elif type(addr) == str and re.match(consensus_email_reg, addr):
            emails_addresses.append(addr)
    else:
        # ask for input to the user
        k = 0
        while add_more or not re.match(consensus_email_reg, addr):
            addr = input(f"{bg.black} {fg.li_blue}Enter dest email address {k+1}: {fg.rs} {bg.rs}\n")
            if addr and re.match(consensus_email_reg, addr):
                emails_addresses.append(addr)
                k += 1
            else:
                addr = input(f"{bg.black} {fg.li_blue}Enter dest VALID email address {k+1}: {fg.rs} {bg.rs}\n")
                if re.match(consensus_email_reg, addr):
                    emails_addresses.append(addr)
                    k += 1
            # ask to the user if he wants to add more addresses
            add_more = update_add_more()

    print(f"{bg.black} {fg.li_yellow}Recipients emails_addresses {emails_addresses}{fg.rs} {bg.rs}\n")
    logger.info(f"Recipients emails_addresses {emails_addresses}")
    return emails_addresses



def command_line_inputs():
    sendmypie = SendMyPie()
    exp = input(f"{bg.black} {fg.li_blue}Enter your exp name: {fg.rs} {bg.rs}\n")

    emails_addresses = enter_email()

    subject = input(f"{bg.black} {fg.li_blue}Enter your subject title: {fg.rs} {bg.rs}\n")
    file_template_path = input(f"{bg.black} {fg.li_blue}Enter path for your html template file: {fg.rs} {bg.rs}\n")

    html_variables = {}

    j = 0
    try:
        add_more = int(input(f"{bg.black} {fg.li_blue}Add variable key for html template rendering (0 to quit)? {fg.rs} {bg.rs}\n"))
    except Exception as e:
        add_more = 1

    while add_more:
        key = input(f"{bg.black} {fg.li_blue}Enter key for variable n°{j+1}: {fg.rs} {bg.rs}\n")
        value = input(f"{bg.black} {fg.li_blue}Enter value for variable n°{j+1}: {fg.rs} {bg.rs}\n")

        add_more = update_add_more()
        html_variables[key] = value
        j += 1

    imgs_directory = input(f"{bg.black} {fg.li_blue}Enter path for your images directory: {fg.rs} {bg.rs}\n")

    # add images
    try:
        add_more = int(input(f"{bg.black} {fg.li_blue}Add image (0 to quit)? {fg.rs} {bg.rs}\n"))
    except Exception as e:
        add_more = 1

    images_data = []
    i = 0
    while add_more:
        image = input(f"{bg.black} {fg.li_blue}Enter filename for your image n°{i+1}: {fg.rs} {bg.rs}\n")
        add_more = update_add_more()
        images_data.append(image)
        i += 1

    EMAIL_HOST_USER = input(f"{bg.black} {fg.li_blue}Enter your exp email address: {fg.rs} {bg.rs}\n")
    EMAIL_HOST_PASSWORD = input(f"{bg.black} {fg.li_blue}Enter your exp password: {fg.rs} {bg.rs}\n")

    # make body
    sendmypie.make_email_body_with_img(exp=exp, emails_addresses=emails_addresses, 
        subject=subject, file_template_path=file_template_path, 
        html_variables=html_variables, 
        imgs_directory=imgs_directory, 
        images_data=images_data)

    # get the list
    list_to_send = sendmypie.get_messages_to_send()

    # send the email
    sendmypie.open_send_close(EMAIL_HOST_USER=EMAIL_HOST_USER, EMAIL_HOST_PASSWORD=EMAIL_HOST_PASSWORD, list_messages=list_to_send)

    # clear the list
    list_to_send.clear()


if __name__ == "__main__":
    command_line_inputs()