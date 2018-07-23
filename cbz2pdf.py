#!/usr/bin/python
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

logging.basicConfig(level=logging.ERROR)

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
    import ipdb; ipdb.set_trace()
    os.system(cmd)

def main(args=None):
	for source_file in args.source_files:
		extract_folder = tempfile.mkdtemp(prefix='cbz2pdf')
		output_filename = os.path.splitext(source_file)[0] + ".pdf"
	
		logging.info('extracting "%s"' % source_file)
		with zipfile.ZipFile(source_file, 'r') as z:
			z.extractall(extract_folder)
			z.close()
		
		print 'Creating "%s"...' % output_filename
		#run_command('convert %s/*.jpg "%s"' % (extract_folder, output_filename))
        run_command('convert %s "%s"' % (walker(extract_folder), output_filename))

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
