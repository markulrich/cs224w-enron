""" This file is for reading in the graph and creating additional attributes.
"""
import snap
import os
import re
from dateutil import parser

FROM_REGEX = re.compile(r'From:?\s[^@]+@[^@]+\.[^@]+\n')
TO_REGEX = re.compile(r'To:?\s[^@]+@[^@]+\.[^@]+\n')
DATE_REGEX = re.compile(r'Date: \w\w\w, [0-9]+ \w\w\w [0-9]{4} \d\d:\d\d:\d\d [-+]?\d\d\d\d \([A-Z]{3}\)')
DATE_FORMAT = '%a, %e %b %Y %H:%M:%S %z (%Z)'

rootdir = './enron_mail_20110402/maildir'

def load_data():
    emailToNid = {}
    id = 1
    f_emails = open('email.txt','w')
    f_edges = open('edges.txt', 'w')

    for subdir, dirs, files in os.walk(rootdir):
        for dir in dirs:
            user_dir = os.path.join(subdir, dir + '/sent')
            if os.path.isdir(user_dir):
                for email in os.listdir(user_dir):
                    dir_entry_path = os.path.join(user_dir, email)
                    if os.path.isfile(dir_entry_path):
                        with open(dir_entry_path, 'r') as email_file:
                            from_email = None
                            to_email = None
                            date_email = None
                            for email_line in email_file:
                                if from_email and to_email and date_email:
                                    break

                                # Handle from_field
                                from_field = re.match(FROM_REGEX, email_line)
                                if from_field:
                                    from_field = from_field.group(0).strip().split('From: ')[-1]
                                    from_field = from_field.split()[-1]
                                    from_field = from_field.translate(None, '<>')
                                    from_email = from_field
                                    if from_field not in emailToNid:
                                        emailToNid[from_field] = id
                                        id += 1
                                        f_emails.write('%d %s\n' % (id, from_field))

                                # Handle to_field
                                to_field = re.match(TO_REGEX, email_line)
                                if to_field:
                                    to_field = to_field.group(0).strip().split('To: ')[-1]
                                    to_field = to_field.split()[-1]
                                    to_field = to_field.translate(None, '<>')
                                    to_email = to_field
                                    if to_field not in emailToNid:
                                        emailToNid[to_field] = id
                                        id += 1
                                        f_emails.write('%d,%s\n' % (id, to_field))

                                # Handle date_email
                                date_email = re.match(DATE_REGEX, email_line)
                                if date_email:
                                    email_string = date_email.group(0).split('Date:')[-1].lstrip()
                                    date_obj = parser.parse(email_string)



                            if from_email and to_email and date_obj:
                                to_id = emailToNid[to_email]
                                from_id = emailToNid[from_email]
                                date_string = date_obj.strftime('%Y-%m-%d %H:%M:%S')

                                #############################################
                                # Format: date, to_id, from_id), email_path #
                                #############################################
                                to_write = '%s,%d,%d,%s\n' % (date_string, to_id, from_id, dir_entry_path)
                                f_edges.write(to_write)
                                print to_write

    f_edges.close()
    f_emails.close()
