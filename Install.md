Once the repository is cloned, use GNU stow to create the symlinks to the cloned repository. Like,

```
  cd $HOME
  git clone https://github.com/ksubramz/dotfiles_reloaded.git
  cd dotfiles_reloaded
  stow vim
  stow qtile
```

etc..
