#!/usr/bin/python
"""
tmux-helper displays a menu of existing sessions and allows for creation of new ones

When combined with mosh and invokved upon login (i.e. mosh my-box python tmux-helper.py) it makes
a handy system that allows for fluid work on remote boxes.
"""

import os
import subprocess


class TmuxSession(object):
  """
  Represents an existing tmux session
  """
  def __init__(self, id, name, description):
    self.id = id
    self.name = name
    self.description = description

  def launch(self):
    """
    Launch this session
    """
    cmd = ['tmux', 'attach', '-d', '-t', self.name]
    os.execlp('tmux', *cmd)

  def __str__(self):
    return '{id}) {description}'.format(
      id=self.id,
      description=self.description
    )


class NewTmuxSession(TmuxSession):
  """
  Special session class for new sessions
  """
  def __init__(self):
    self.id = 'n'
    self.name = 'new'
    self.description = 'Start a new session'

  def launch(self):
    """
    Launch a new session
    """
    session_name = str(raw_input('New session name: '))
    cmd = ['tmux', 'new', '-s', session_name]
    os.execlp('tmux', *cmd)


class TmuxHelper(object):
  """
  TmuxHelper implements the main logic for listing, creating and selecting sessions
  """
  def __init__(self):
    self.session_ids = []
    self.sessions = {}

  def run(self):
    """
    Run the helper
    """
    self.get_sessions()
    self.session_ids.append('n')
    self.sessions['n'] = NewTmuxSession()

    for session_id in self.session_ids:
      print str(self.sessions[session_id])

    self.read_choice()

  def get_sessions(self):
    """
    Fetches the current tmux sessions
    """
    cmd = ['tmux', 'ls']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    tmux_out, _ = proc.communicate()

    session_id = 0
    for line in tmux_out.split('\n'):
      if not line:
        continue

      session_name, _ = line.split(':', 1)
      session_id += 1
      self.session_ids.append(str(session_id))
      self.sessions[str(session_id)] = TmuxSession(session_id, session_name, line)

  def read_choice(self):
    """
    Read the users choice
    """
    while True:
      selection = str(raw_input('Make a selection: '))
      if selection in self.sessions:
        return self.sessions[selection].launch()

      print "Invalid selection! Valid choices are: {choices}".format(
        choices=', '.join(self.session_ids)
      )


if __name__ == '__main__':
  try:
    TmuxHelper().run()
  except (EOFError, KeyboardInterrupt, SystemExit):
    pass
