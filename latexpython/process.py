import re,sys,os
import subprocess as sp

class CompilationError(Exception):
   pass

def compile_doc(is_english,root_path,with_bib,final_doc_name='M-L0.pdf'):
   try:
      os.chdir(root_path)
      stdout_redirect = open(os.path.join(root_path,'output.log'),'w')
      if is_english:
         print('Generating your .pdf document with pdflatex...')
         os.chdir(root_path)
         compile_process = sp.Popen('pdflatex -interaction=nonstopmode -halt-on-error {0}'.format('M-L0.tex'),shell=True,\
               stdout=stdout_redirect,stderr=stdout_redirect)
         compile_process.wait()
         exit_code = compile_process.returncode
         if with_bib:
            compile_bib = sp.Popen('biber {0}'.format('M-L0'),shell=True,stdout=stdout_redirect,stderr=stdout_redirect)
            compile_bib.wait()
            cp2 = sp.Popen('pdflatex -interaction=nonstopmode -halt-on-error {0}'.format('M-L0.tex'),shell=True,stdout=stdout_redirect,stderr=stdout_redirect)
            cp2.wait()
            cp3 = sp.Popen('pdflatex -interaction=nonstopmode -halt-on-error {0}'.format('M-L0.tex'),shell=True,stdout=stdout_redirect,stderr=stdout_redirect)
            cp3.wait()
            exit_code = cp3.returncode
      else:
         print('Generating your .pdf document with xelatex...')
         compile_process = sp.Popen('xelatex -interaction=nonstopmode -halt-on-error {0}'.format('M-L0.tex'),shell=True,\
               stdout=stdout_redirect,stderr=stdout_redirect)
         compile_process.wait()
         if with_bib:
            compile_bib = sp.Popen('biber {0}'.format('M-L0'),shell=True,stdout=stdout_redirect,stderr=stdout_redirect)
            compile_bib.wait()
            cp2 = sp.Popen('xelatex -interaction=nonstopmode -halt-on-error {0}'.format('M-L0.tex'),shell=True,stdout=stdout_redirect,stderr=stdout_redirect)
            cp2.wait()
            cp3 = sp.Popen('xelatex -interaction=nonstopmode -halt-on-error {0}'.format('M-L0.tex'),shell=True,stdout=stdout_redirect,stderr=stdout_redirect)
            cp3.wait()
            exit_code = cp3.returncode
         exit_code = compile_process.returncode

      stdout_redirect.close()

      if exit_code:
         raise CompilationError
      else:
         print('Completed!! Exiting...')

   except CompilationError:
      print('An error has occurred. See \'output.log\' for details.')
      sys.exit(1)

   os.rename('M-L0.pdf',final_doc_name)
