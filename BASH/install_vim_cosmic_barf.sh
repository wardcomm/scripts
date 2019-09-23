#!/bin/bash
#Option 1: Manual installation

#1.  After downloading the vim script or package, move the
    `cosmic-barf.vim` file to the `.vim/colors` directory.

#        $ cd cosmic-barf/colors
#        $ mv cosmic-barf.vim ~/.vim/colors/

#Option 2: Pathogen installation

#1.  Move or clone the `cosmic-barf` directory so that it is
#    a subdirectory of the `.vim/bundle` directory.
mkdir -p ~/.vim/bundle
cd ~/.vim/bundle
wget https://github.com/evturn/cosmic-barf/blob/master/colors/cosmic-barf.vim
mkdir -p ~/.vim/colors/
cd  ~/.vim/colors/
wget https://github.com/evturn/cosmic-barf/blob/master/colors/cosmic-barf.vim


#cd ~/.vim/bundle
#cd ~/.vim/bundle
#wget https://github.com/evturn/cosmic-barf/blob/master/colors/cosmic-barf.vim
#git clone https://github.com/evturn/cosmic-barf.git
#git clone git@github.com:evturn/cosmic-barf.git

#Modify .vimrc
#---------------------

#syntax enable
#set background=dark
#colorscheme cosmic-barf
#let g:colors_name = 'cosmic-barf'
