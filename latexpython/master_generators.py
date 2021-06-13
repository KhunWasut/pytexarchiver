import re,os,sys
import latexpython.dirtree as dirtree
import datetime

# Define necessary dictionary mapping

thai_month_dict = {1:'มกราคม',2:'กุมภาพันธ์',3:'มีนาคม',4:'เมษายน',5:'พฤษภาคม',6:'มิถุนายน',7:'กรกฎาคม',8:'สิงหาคม',9:'กันยายน',10:'ตุลาคม',11:'พฤศจิกายน',12:'ธันวาคม'}

# Define new root_head to be complelely modular

# Currently hardcode the book format to force it to be one-sided.
def root_head(file_obj,doc_type,font_size='',is_onesided=True):
   if font_size != '':
      if doc_type == 'book' and is_onesided == True:
         file_obj.write('\\documentclass[{0}pt,oneside]{{{1}}}'.format(font_size,doc_type))
      else:
         file_obj.write('\\documentclass[{0}pt]{{{1}}}'.format(font_size,doc_type))
   else:
      file_obj.write('\\documentclass{{{0}}}\n\n'.format(doc_type))


def root_book_head(file_obj):
   file_obj.write('\\documentclass{book}\n\n')
#   if is_english:
#      file_obj.write('\\input{{{0}}}\n\n'.format(preamble_paths_eng[machine]))
#   else:
#      file_obj.write('\\input{{{0}}}\n\n'.format(preamble_paths_thai[machine]))

def root_begin_doc(file_obj):
   file_obj.write('\\begin{document}\n')

def root_end(file_obj):
   file_obj.write('\\end{document}\n')

def root_title(is_english,title,author,file_obj,created_date=datetime.date.today()):
   file_obj.write('\\title{{{0}}}\n'.format(title))
   file_obj.write('\\author{{{0}}}\n'.format(author))
   if is_english:
      date_string = created_date.strftime('%B %-d, %Y')
   else:
      date_string = '{0} {1} พ.ศ. {2}'.format(created_date.day,thai_month_dict[created_date.month],created_date.year+543)
   file_obj.write('\\date{{\\textbf{{Originally Written}}: {0} \\\\ \\textbf{{Last Updated}}: \\today}}\n'.format(date_string))
   file_obj.write('\\maketitle\n')
   file_obj.write('\\vspace{5em}\n')
   file_obj.write('\\begin{center}\n')
   file_obj.write('   {\\Large \\textbf{DIGNITY, SERVICE, EVOLUTION, INNOVATION}} \\\\ \\vspace{1.2em}\n')
   file_obj.write('   {Enrich the Strengths, Accept the Weaknesses, Follow the Sacred Values, Inspire the Future!! \\\\ \\vspace{1.2em}}\n')
   file_obj.write('   {For an EPIC life filled with Ethics, Passions, Intelligence, and Creativity!!}\n')
   file_obj.write('\\end{center}\n\n')


def root_body(ancestors_list,current_node,children_list,file_obj):
   # Don't expect root level to have individual .tex file, but will add the individual code just in case
   # If individual .tex file hangs around in that node, simply import or subimport it in the master file
   # Check each children for being a directory or a file. If a directory, subimport/import the children and its master file. If a file, just import/subimport a file
   # at the parent dir.
   for child in children_list:
      path_at_node = dirtree.get_path_at_this_node(ancestors_list,current_node)
      path_to_child = os.path.join(path_at_node,child)
      if os.path.isfile(path_to_child):
         tex_pattern = re.compile('\.tex$')
         child = re.sub(tex_pattern,'',child)
         #file_obj.write('\\newpage\n')
         file_obj.write('\\import{{./}}{{{0}}}\n'.format(child))
      elif os.path.isdir(path_to_child):
         level_pattern = re.compile('^L([1-9]|[1-9][0-9])-')
         level_num = eval(level_pattern.search(child).group(1))
         child_master_tex_prefix = 'M-L{0}'.format(level_num)
         #file_obj.write('\\newpage\n')
         file_obj.write('\\import{{./{0}/}}{{{1}}}\n'.format(child,child_master_tex_prefix))


def non_root_body(ancestors_list,current_node,children_list,file_obj):
   for child in children_list:
      path_at_node = dirtree.get_path_at_this_node(ancestors_list,current_node)
      path_to_child = os.path.join(path_at_node,child)
      if os.path.isfile(path_to_child):
         tex_pattern = re.compile('\.tex$')
         child = re.sub(tex_pattern,'',child)
         file_obj.write('\\subimport{{./}}{{{0}}}\n'.format(child))
      elif os.path.isdir(path_to_child):
         level_pattern = re.compile('^L([1-9]|[1-9][0-9])-')
         level_num = eval(level_pattern.search(child).group(1))
         child_master_tex_prefix = 'M-L{0}'.format(level_num)
         file_obj.write('\\subimport{{./{0}/}}{{{1}}}\n'.format(child,child_master_tex_prefix))


def create_master_root(is_english,title,author,root_tuple,hyperlink,with_bib,title_page_content,doc_type,bib_style='',bib_engine='',bib_path='',bib_additional_options='',preamble='',created_date=datetime.date.today(),is_titlepage=False):
   path_at_node = dirtree.get_path_at_this_node(root_tuple[2],root_tuple[0])
   root_file_obj = open(os.path.join(path_at_node,'M-L0.tex'),'w')

   # doc_type will now be the actual 'documentclass' head
   root_file_obj.write(doc_type+'\n')
   root_file_obj.write(preamble+'\n')
   # PLACEHOLDER FOR EXTRA CONTENTS CODE!!
   if with_bib:
      # As of Mar 24, bib_path is modeled to restrict to only one path. If the situation dictates more than one .bib files,
      # will make changes here accordingly and please refer to the proposed schemes in the main execution code.
      # Updated: Apr 18, 2018 - Allow the specification of bibliography styles beside using biber
      if bib_engine == 'biblatex':
        if bib_additional_options:
           root_file_obj.write('\\usepackage[backend=biber,style={0},{1}]{{biblatex}}\n'.format(bib_style,bib_additional_options))
           root_file_obj.write('\\addbibresource{{{0}}}\n'.format(bib_path))
        else:
           root_file_obj.write('\\usepackage[backend=biber,style={0}]{{biblatex}}\n'.format(bib_style))
           root_file_obj.write('\\addbibresource{{{0}}}\n'.format(bib_path))
      elif bib_engine == 'bibtex':
        # IF USING BIBTEX, NO NEED TO SPECIFY BIB_STYLE AND BIB_PATH (THESE ARE TAKEN CARE OF IN THE BIBLIOGRAPHY PART OF DOCUMENT)
        pass
   if hyperlink:
      root_file_obj.write('\\usepackage{hyperref}\n')
      root_file_obj.write('\\hypersetup{linktocpage}\n')    # Not 100% correct. Will make adjustments here on better hyperref settings later but for now this works.
   root_begin_doc(root_file_obj)
   if is_titlepage:
      root_file_obj.write('{0}\n'.format(title_page_content))
   else:
      root_title(is_english,title,author,root_file_obj,created_date)
   root_body(root_tuple[2],root_tuple[0],root_tuple[3],root_file_obj)
   root_end(root_file_obj)

   root_file_obj.close()


def create_master_non_root(node_tuple):
   path_at_node = dirtree.get_path_at_this_node(node_tuple[2],node_tuple[0])
   level_pattern = re.compile('^L([1-9]|[1-9][0-9])-')
   level_num = eval(level_pattern.search(node_tuple[0]).group(1))
   node_file_obj = open(os.path.join(path_at_node,'M-L{0}.tex'.format(level_num)),'w')

   non_root_body(node_tuple[2],node_tuple[0],node_tuple[3],node_file_obj)

   node_file_obj.close()


def generator(is_english,title,author,nodes_info,hyperlink,is_titlepage,title_page_content,doc_type,with_bib,bib_style='',bib_engine='',bib_path='',bib_additional_options='',preamble='',created_date=datetime.date.today()):
   # This is probably the trickiest method here. 'nodes_info' is a result of the information query from the tree and is a list of 4-elem tuples containing info for all nodes.
   # The condition here is traversing all nodes except the leaves

   for node_tuple in nodes_info:
      if node_tuple[3] != []:      # Not a leaf
         # If node_tuple[0] (node name) doesn't start with 'L', it means that's a root node.
         is_not_root_pattern = re.compile('^L')
         if is_not_root_pattern.search(node_tuple[0]):
            # Means this is not a root, so simply create a master file
            create_master_non_root(node_tuple)
         else:
            create_master_root(is_english,title,author,node_tuple,hyperlink,with_bib,title_page_content,doc_type,bib_style,bib_engine,bib_path,bib_additional_options,preamble,created_date,is_titlepage)
