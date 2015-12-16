set nocompatible
filetype off

set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

" let Vundle manage Vundle
" " required! 
Plugin 'VundleVim/Vundle.vim'
Plugin 'gmarik/vundle'
Plugin 'jlfwong/vim-mercenary'
Plugin 'jonathanfilip/vim-lucius'
Plugin 'bling/vim-airline'
Plugin 'noahfrederick/vim-hemisu'
Plugin 'romainl/Apprentice'
Plugin 'w0ng/vim-hybrid'
Plugin 'morhetz/gruvbox'
Plugin 'nanotech/jellybeans.vim'
Plugin 'majutsushi/tagbar'
Plugin 'Yggdroot/indentLine'
Plugin 'vim-scripts/PaperColor.vim'
Plugin 'freeo/vim-kalisi'
Plugin 'kien/ctrlp.vim'
Plugin 'gilgigilgil/anderson.vim'
Plugin 'habamax/vim-ctrlp-colorscheme'
Plugin 'WillianPaiva/vim-material-colors'
Plugin 'scrooloose/syntastic'
Plugin 'nvie/vim-flake8'
Plugin 'tmhedberg/SimpylFold'
Plugin 'vim-scripts/indentpython.vim'
Plugin 'ervandew/supertab'
Plugin 'reedes/vim-colors-pencil'
Plugin 'zenorocha/dracula-theme',{'rtp':'vim/'}


call vundle#end()
"
" The bundles you install will be listed here

filetype plugin indent on
let python_highlight_all=1
syntax on
se nu
" Set leader key to comma
let mapleader=","
set t_Co=256
set background=light
colo kalisi
set hlsearch

set foldmethod=indent
set foldlevel=99
noremap <space> :bn<CR> 

if has('gui_running')
  "set guifont=Consolas:h16
  "set guifont=Inconsolata:h18
  set guifont=PragmataPro\ 12 linespace=1
  "set guifont=Ubuntu\ Mono:h18
  "set guifont=Source\ Code\ Pro:h16
  "set guifont=Source\ Code\ Pro\ for\ Powerline:h14
endif

set laststatus=2
set ttimeoutlen=50
" Enable the list of buffers
let g:airline#extensions#tabline#enabled = 1
" Show just the filename
let g:airline#extensions#tabline#fnamemod = ':t'

"Tagbar
map <F8> :TagbarToggle<CR>
map <leader>r :!ctags --python-kinds=-i --exclude=*/.hg/* .<CR><CR>

"CtrlP
" Set no max file limit
let g:ctrlp_max_files = 0
let g:ctrlp_user_command = {
\ 'types': {
\ 1: ['.hg/', 'hg --cwd %s locate -I .'],
\ },
\ 'fallback': 'find %s -type f'
\ }
" Search from current directory instead of project root
map <leader>f :CtrlP<cr>
map <leader>g :CtrlPBuffer<cr>
map <leader>c :CtrlPColorscheme<cr>

" F1 to open current file
nnoremap <F1> <c-w>gF
nnoremap <F12> bd

"split navigations
nnoremap <C-J> <C-W>j
nnoremap <C-K> <C-W>k
nnoremap <C-L> <C-W>l
nnoremap <C-H> <C-W>h
nnoremap <Right> :wincmd w<cr>

" PEP8 indentantion
au BufNewFile,BufRead *.py
    \ set tabstop=4 |
    \ set softtabstop=4 |
    \ set shiftwidth=4 |
    \ set expandtab |
    \ set autoindent |
    \ set fileformat=unix |

"syntastic setup
set statusline+=%#warningmsg#
set statusline+=%{SyntasticStatuslineFlag()}
set statusline+=%*

let g:syntastic_python_python_exec = '/usr/bin/python2.7'
let g:syntastic_always_populate_loc_list = 1
let g:syntastic_auto_loc_list = 1
let g:syntastic_check_on_open = 1
let g:syntastic_check_on_wq = 0

" Flag unnecessary whitespace
highlight BadWhitespace ctermbg=red guibg=darkred
au BufRead,BufNewFile *.py,*.pyw,*.c,*.h match BadWhitespace /\s\+$/

" Ctrl-R will replace the visually selected text everywhere 
vnoremap <C-r> "hy:%s/<C-r>h//gc<left><left><left>
