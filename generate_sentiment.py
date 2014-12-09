""" This file is for generating sentiment labeling as well as basic features
    like word count.
"""
import os
import re
from textblob import TextBlob

BODY_START_TOKEN = 'X-FileName' # Copy only after a line containing this

rootdir = './enron_mail_20110402/maildir'

def load_data():
    f_features = open('nlp_features.out','w') # filename,sentiment_score,line_count

    for subdir, dirs, files in os.walk(rootdir):
        for dir in dirs:
            user_dir = os.path.join(subdir, dir + '/sent')
            if os.path.isdir(user_dir):
                for email in os.listdir(user_dir):
                    dir_entry_path = os.path.join(user_dir, email)
                    if os.path.isfile(dir_entry_path):
                        with open(dir_entry_path, 'r') as email_file:
                            print 'Processing', dir_entry_path
                            lines = []
                            start = False
                            for line in email_file:
                                if start:
                                    lines.append(line)
                                if BODY_START_TOKEN in line:
                                    start = True


                            num_lines = len(lines)
                            msg = '\n'.join(lines)
                            blob = TextBlob(msg)
                            sentiment_score = blob.sentiment.polarity


                            ###############################################
                            # Format: filename,sentiment_score,line_count #
                            ###############################################
                            to_write = '%s,%f,%d\n' % (dir_entry_path, sentiment_score, num_lines)
                            f_features.write(to_write)
                            print 'Done processing', dir_entry_path

    f_features.close()

if __name__ == '__main__':
    load_data()
