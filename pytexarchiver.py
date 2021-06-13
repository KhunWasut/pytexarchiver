#!/usr/bin/env python3

# LAST UPDATED: JANUARY 5, 2017

import argparse
import os,re,sys
import datetime
import subprocess as sp

from latexpython import dirtree,master_generators,process,exceptions


Node = dirtree.Node

# Building directory tree on the fly according to my idea
#    - Initialize the root node first
#    - Traverse the tree. For each node visited, if the children is empty (i.e. leaves), search that node for directories or relevant files
#    - Update the tree
#    - Traverse from scratch again, rinse and repeat
#    - Stop when all leaves contain no relevant directories or files to be added

parser = argparse.ArgumentParser(description='Search a structured LaTeX document root directories for subdirectories, and link them together into a tree based on\
      their relationships, as well as generate master .tex files that govern each level of directories and compile them into a .pdf file, all in a single step! \
      Great for creating and organizing large and complex documents that need constant reviews or edits.')

parser.add_argument('--document-type',action='store',dest='document_type',help='The whole "documentclass" line goes here',default='')
parser.add_argument('-t','--title',action='store',dest='title',help='Your document\'s title',default='')
parser.add_argument('-p','--tex-prefix',action='store',dest='tex_prefix',help='The prefix name for your LaTeX document',default='M-L0')
parser.add_argument('-a','--author',action='store',dest='author',help='The author\'s name',default='Wasut \'Khun\' Pornpatcharapong')
parser.add_argument('-d','--date',action='store',dest='created_date',help='The original created date of the document',default='0')
parser.add_argument('-l','--link',action='store_true',dest='hyperlink',help='Enable hyperlink in the document',default=False)
parser.add_argument('--tp','--title-page',action='store',dest='title_page',help='Parse your own title page.',default='')
parser.add_argument('--bib',action='store_true',dest='with_bib',help='Use this flag to compile the document with bibliography',default=False)
parser.add_argument('--bib-engine',action='store',dest='bib_engine',help='Specify bibliography engine (natbib, bibtex, or biblatex)',default='')
parser.add_argument('--bib-style',action='store',dest='bib_style',help='Enter bib style (biblatex format)',default='')
parser.add_argument('--bib-fullpath',action='store',dest='bib_path',help='This must be specified if the --bib flag is toggled on.',default='')
parser.add_argument('--bib-additional-options',action='store',dest='bib_additional_options',help='This must be specified if the --bib flag is toggled on.',default='')
parser.add_argument('--english',action='store_true',dest='is_english',help='Use pdflatex as a compiler with English language documents',default=True)
parser.add_argument('--preamble',action='store',dest='preamble',help='Use this flag to add document-specific preambles via a text file',default='')
parser.add_argument('--thai',action='store_false',dest='is_english',help='Use xelatex as a compiler with Thai language documents',default=True)
args = parser.parse_args()

# Collecting variables
author = args.author
doc_type = args.document_type
tex_prefix = args.tex_prefix
is_english = args.is_english
with_bib = args.with_bib
preamble = args.preamble
title_page = args.title_page
# For now only concern documents with one bib file, but I already have a scheme for documents with more than one bib file - 
# the --bib-fullpath field should have the format "path1,path2" and the code shall split the paths at commas into the list and count them.
# Just to make the scheme works first, let's KISS (Keep It Simple and Stupid)!!
bib_path = args.bib_path
bib_style = args.bib_style
bib_engine = args.bib_engine
bib_additional_options = args.bib_additional_options
title = args.title
date = args.created_date
hyperlink = args.hyperlink

# If no -m and -t tags are specified, prompt the user. The reason I do this is sometimes I need to compile quickly but don't want to pause when typing commands with flags.
# Because assigning document title take a little time, I would rather separate this process to the user prompt instead.

if title == '' and title_page == '':
   print('What\'s your document title? Typing in any unicode characters is fine.')
   title = input()

# If the bib flag is toggled on and there are no inputs to the --bib-style field or the --bib-fullpath entry, prompt the user!!
# This design choice is made because in the situation where we work with multiple machines, paths can be different and users have to specify them explicitly.
# In the future, as documents are highly schemed and structured, the main TeX directories shall be represented by one env variable on UNIX systems
# (I'm doing this on OSX and LNX with the $KTEXDIR UNIX variable)
# Future edition will include reading system env variable and simply add the root paths

if with_bib and ((bib_style == '') or (bib_path == '') or (bib_additional_options == '')):
   if bib_engine == 'biblatex':
      bib_style = input('Please enter the bibliography style in biblatex format: ')
      print('Please enter the full path(s) to your .bib file(s). Use commas to separate if there are more than one entries:')
      bib_path = input()
      additional_options = input('Any additional bibliography options? (Y/N): ')
      if additional_options.upper() == 'Y':
         print('Specify any additional options (e.g. articletitle for chem-acs style). List as LaTeX options separated by commas. Hit enter if none: ')
         bib_additional_options = input()

# Change created_date into datetime.date format. If not defined, set to today
# Use my usual YYYYMMDD format

dp = re.compile(r'^(201[4-7])(0[1-9]|1[0-2])([0-2][0-9]|3[0-1])$')

if date != '0' and dp.search(date):
   year = dp.search(date).group(1)
   month = dp.search(date).group(2)
   day = dp.search(date).group(3)
   created_date = datetime.date(eval(year),eval(re.sub('^0','',month)),eval(re.sub('^0','',day)))
else:
   created_date = datetime.date.today()

# If title_page=='', then we manually set the is_titlepage flag to 'False'

if title_page == '':
   is_titlepage = False
else:
   is_titlepage = True

cwd = os.getcwd()

# Root node initialization
dir_tree = dirtree.DirTree(Node(cwd))

# Building the tree
dir_tree = dirtree.buildtree(dir_tree)

# Now that the tree is built, create master files at each particular directory
nodes_info = dir_tree.get_node_relations(dir_tree.root)

# generator methods now take bib_style and bib_path as argument.
# For simplicity, this update only supports one bib file.
master_generators.generator(is_english,title,author,nodes_info,hyperlink,is_titlepage,title_page,doc_type,with_bib,bib_style,bib_engine,bib_path,bib_additional_options,preamble,created_date)

process.compile_doc(is_english,dir_tree.root.val,with_bib,bib_engine,tex_prefix+'.pdf')
