# tmux-helper

Tmux-helper is a simple script for managing your tmux sessions.

I primarily use a laptop at work, but do most of computing a desktop box.  Tmux pairs well with mosh (or ssh) to provide a good experience.  But I would still find myself forgetting to open a tmux session each time.

The suggested way of using tmux-helper is by using the command:
```
ssh machine /path/to/tmux-helper.py
```

An even better way is to setup a bash alias:
```
alias desktop="mosh desktop python tmux-helper.py"
```
Then use the desktop command to access your machine.

When you connect and run tmux-helper, it will give you a list of your sessions, their state, and the option to create a new session.  Creating a new session will prompt you for a session name.
```
n) new session [new]
1) metricsdisco [attached]
3) nurse [attached]
2) mm-jtune [attached]
5) odrgen [attached]
4) odr-yaml [attached]
6) int [attached]
Make a selection:
```
