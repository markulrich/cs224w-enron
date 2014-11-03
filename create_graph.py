""" This file is for reading in the graph and creating additional attributes.
"""
import snap
import os
import re

FROM_REGEX = re.compile(r'From:?\s[^@]+@[^@]+\.[^@]+\n')
TO_REGEX = re.compile(r'To:?\s[^@]+@[^@]+\.[^@]+\n')

rootdir = './enron_mail_20110402/maildir'

def load_data():
    emailToNid = {}
    id = 1
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
                            for email_line in email_file:
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

                            if from_email and to_email:
                                to_id = emailToNid[to_email]
                                from_id = emailToNid[from_email]
                                print 'Email from %s (id: %d) to %s (id: %d)' % (from_email, from_id, to_email, to_id)
