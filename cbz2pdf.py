#!/bin/env python
# encoding: utf-8
"""
cbz2pdf.py

Created by Charles-Axel Dein on 2011-10-29.
Copyright (c) 2011 Charles-Axel Dein. All rights reserved.
"""

import sys
import os
import argparse
import zipfile
import tempfile
import logging

#logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)

def walker(dir):
    rv=[]
    for root, dirs, files in os.walk(dir):
        for file in files:
          rv.append(os.path.join(root, file))
    rv.sort()
    return '"%s"'%'" "'.join(rv)
                                
def run_command(cmd,nice=-9):
    if nice: cmd="nice -n %d %s"%(nice,cmd)
    logging.info("running %s" % cmd)
    #import ipdb; ipdb.set_trace()
    st=os.system(cmd)
    if st:
        logging.error("Command %s failed with state %d"%(cmd,st))
        return False
    else:
        return True

def filetype(f):
    try:
        # pip install python-magic
        import magic
        m=magic.from_file(f)
        logging.debug(m)
        if m is not None:
            return m.split(' ')[0].upper().strip()
        else :
            return None
    except ImportError as e:
        import subprocess
        import re
        #              grab output              remove LF   second field  but keep only before comma, no blanks
        out=subprocess.check_output(['file',f]).strip('\n').split(':')[1].split(',')[0].strip()
        #someone we know?
        m=re.match('^(ZIP|RAR|PDF)',out,flags=re.I)
        if m is not None:
            return m.group().upper()
        else:
            return None
        
    except IOError as e:
        logging.error("Opening %s:%r"%(f,e))

    return None

def unpack(f,d):
    t=filetype(f)
    logging.debug("Filetype: %s"%t)
    if t == 'ZIP':
        return unzipper(f,d)
    elif t == 'RAR':
        return unrar(f,d)
    else :
        logging.error("Cannot handle filetype %s"%t)
        return False
    
def unrar(f,d):
    return run_command('unrar -inul e "%s" %s' % (f,d))
    
def unzipper(f,d):
    try:
        with zipfile.ZipFile(f, 'r') as z:
            z.extractall(d)
            z.close()
    except zipfile.BadZipfile as e:
        logging.error("Not a zip file: %s"%f)
        return False
    except IOError as e:
        logging.error("Opening %s:%r"%(f,e))
        return False
    return True

def main(args=None):
    for source_file in args.source_files:
        extract_folder = tempfile.mkdtemp(prefix='cbz2pdf')
        output_filename = os.path.splitext(source_file)[0] + ".pdf"
    
        logging.info('extracting "%s" into %s' % (source_file,extract_folder))
        if not unpack(source_file,extract_folder):
            logging.warning("Unpacking FAILED for %s"%source_file)
            continue
        
        logging.info('Creating "%s"...' % output_filename)
        run_command('convert %s "%s"' % (walker(extract_folder), output_filename))

        if not os.path.exists(output_filename):
            logging.error("Conversion FAILED for %s"%source_file)
        else:
            logging.info("OK")
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert a cbz file to a pdf')
    parser.add_argument('source_files', help='cbz files', nargs="*")

    args = parser.parse_args()
    
    sys.exit(main(args))
#
#Local Variables:
#tab-width: 4
#End:
#
