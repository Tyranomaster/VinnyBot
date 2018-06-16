.. documentation about page, created 11/15 by mrb25

VinnyBot Documentation
============================

Documentation On ... Documentation?
----------------------------------------------------------
Seems silly, but if its hard, no one will do it. And I don't want that.

Documentation is held on readthedocs.org under the vinnybot project, and is automatically updated whenever new code is pushed.
If you've never worked with readthedocs before, it utilizes sphinx to create pages from restructured text, a language similar to markdown.
I have also made it possible to just use markdown files, so If you don't want to learn rst, you don't need to.

Basically each file corresponds to a page on the documentation, with the name of the file corresponding to the name on the sidebar.

Modifying Existing Files
--------------------------------------
Basically just change whatever you want to, and it will build the new docs when the code is pushed to gihub again.
Make sure to use whatever language the file is already in (.md - markdown, .rst - restructured text)

Which might leave you asking "How do I check that something I did isn't broke as hell?"

Building The Site Locally
---------------------------------------
1) Install a few extra python packages:
    * pip install recommonmark
    * pip install sphinx_rtd_theme
    * pip install sphinx sphinx-autobuild
2) open up command prompt/terminal in the docs/directory and enter the command "make html"
3) If all goes according to plan, it will make the website in the _bulid/ directory (This is ignored by git)

Creating A New Page
-----------------------------------
* The files must be stored in the docs/ directory as markdown (.md) or restructured text (.rst)
* Make the name of the file what it will be about, this name will be public.
* add the name of the file to index.rst in the toctree after the files that are already there.
