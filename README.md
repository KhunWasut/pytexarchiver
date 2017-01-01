# pytexarchiver

<h2>Table of Contents</h2>
<ul>
  <li><a href="#intro">Introduction to <code>pytexarchiver</code></a></li>
  <li><a href="#install">Requirements and Installation</a></li>
  <li><a href="#usage">Usage</a></li>
  <li><a href="#dirstructure">Directory Structure</a></li>
  <li><a href="#opensource">Open Source Policies</a></li>
  <li><a href="#knownissue">Khown Issues (v0.1)</a></li>
</ul>

<h2 id="intro">Introduction to <code>pytexarchiver</code></h2>

<p>
  This is a python-based UNIX command line tool that compiles <code>.tex</code> files from multiple level of directories into
  a single <code>.pdf</code> document; therefore, it is very useful for writing large LaTeX documents like Ph.D. theses or
  manuscripts for scholarly publications as being able to organize <code>.tex</code> files into directories based on
  the structure of the document does indeed save hassles from later proofreading and make life easier when writing large
  documents.
</p>

<h2 id="install">Requirements and Installation</h2>

<h4>Requirements</h4>
<ul>
  <li>Users must be running any variants of UNIX terminal emulator (cygwin, MacOS terminal, Linux terminal etc.)</li>
  <li>Within the running UNIX terminal emulator of your choice, you must have python version 3 installed. As 
      this is designed to also work with unicode documents, I chose to only develop this with python 3+ for better
      unicode supports.</li>
</ul>

<h4>Installation</h4>
<ul>
  <li>Clone this repository to your working directory 
    <ul>
      <li>If you do not know where you are, type <code>pwd</code> in your terminal</li>
      <li>It is recommended that you planned ahead where to put the files from this repo</li>
      <li>To clone this repo, type <code>git clone https://github.com/KhunWasut/pytexarchiver.git</code></li>
    </ul>
   </li>
   <li>If the permission of the file has not yet been set, at least set it to be executable by the user by
   typing <code>chmod 700 [your_working_directory]/pytexarchiver/pytexarchiver.py</code></li>
   <li>If you wish, you may designate your working directory your UNIX a <code>PATH</code> variable</li>
</ul>

<h2 id="usage">Usage</h2>
<ul>
  <li>The executable is called by invoking either the relative or the absolute path to the executable.
    <ul>
      <li>If you are in <code>[your_installation_dir]/pytexarchiver</code>, you can simply call <code>./pytexarchiver.py</code>
      </li>
      <li>If you have set your installation directory to UNIX's <code>PATH</code> variable, calling the executable
      simply <code>pytexarchiver.py</code> works</li>
    </ul>
  </li>
  <li>
    Usage: <code>pytexarchiver.py [--options_with_argument ARGUMENT] [--options-without-argument]</code>
    <ul>
      <li>For helps on whether which command line option does what, simply type <code>pytexarchiver.py --help</code>
      and you will see the list of options.</li>
      <li><code>pytexarchiver</code> follows a very strict pattern of directory structure to enforce structural
      integrity of the document. Please click this <a href="#dirstructure">link</a> to go to the section describing directory structure.</li>
    </ul>
  </li>
  <li>Example usage (assumed that you have created a structure outlined in <a href="#dirstructure">Directory Structure</a> section)</li>
  <ul>
    <li><code>pytexarchiver.py --preamble "$(<preamble_filename)" --title-page "$(<titlepage_filename)" --bib --bib-style "chem-acs" --bib-fullpath "your-path-to-bib-file"</code></li>
  </ul>
</ul>

<h2 id="dirstructure">Directory Structure</h2>

<ul>
  <li>The naming scheme is <code>L<em>m</em>-<em>n</em>-<em>description</em></code>
    <ul>
      <li><code><em>m</em></code> is any integer from 1. This is a <em>leveling number</em></li>
      <li><code><em>n</em></code> is also any integer from 1. This is a <em>ordering number</em></li>
      <li><code><em>description</em></code> is any contiguous string with no space that describes what is in this directory</li>
      <li>This scheme both works with directories and terminal <code>.tex</code> files</li>
    </ul>
  </li>
  <li>Any directories or files that do not follow the above naming scheme will not be compiled.</li>
  <li>At the deepest level (leaves) of the tree, there can only be the <code>.tex</code> files else the code will not
  work.</li>
  <li>Example of the working structure: <br />
  <div color="#FFA500">
. <br />
├── L1-1-introduction <br />
│   ├── L2-1-free-energy-calculation <br />
│   │   ├── L3-1.tex <br />
│   │   └── L3-2-probabilistic-definition <br />
│   │       └── L4-1.tex <br />
│   ├── L2-2-weighted-histogram <br />
│   │   └── L3-1 <br />
│   │       └── L4-1.tex <br />
│   └── L2-3-biased-potential <br />
│       └── L3-1.tex <br />
├── L1-2-methods <br />
│   └── L2-1.tex <br />
├── L1-3-results-discussion <br />
│   └── L2-1.tex <br />
└── L1-4-conclusion <br />
    └── L2-1.tex <br />
  </div>
  </li>
  <li><code>pytexarchiver</code> has to be compiled at the root directory of your document ONLY.</li>
</ul>

<h2 id="opensource">Open Source Policies</h2>

<p>
  <code>pytexarchiver</code> is provided under the MIT license, so you may fork this repository and extend the features or 
  make any modifications as you wish. However, I would be really appreciated if my name is at least mentioned. I believe
  in the power of open source, and my fellow coder friends who are more experienced than me will extend the feature
  of this little tool far more than I can ever imagine!
</p>

<h2 id="knownissue">Known Issues (v0.1)</h2>

<ul>
  <li>The code does not strictly follow PEP8 guideline. Pardon my amateur programming experience.</li>
  <li>Exceptions catching are not yet very well implemented.</li>
  <li>I feel like the tree data structure that represents the directory tree can be implemented more efficiently</li>
</ul>

<p>&copy; 2016 Wasut 'Khun' Pornpatcharapong. All Rights Reserved.</p>
