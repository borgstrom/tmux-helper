#!/usr/bin/python
"""
tmux-helper displays a menu of existing sessions and allows for creation of new ones

When combined with mosh and invokved upon login (i.e. mosh my-box python tmux-helper.py) it makes
a handy system that allows for fluid work on remote boxes.
"""

from collections import namedtuple
import os
import re
import subprocess

TmuxSession = namedtuple('TmuxSession', ('session_id', 'session_state'))

class TmuxStatus(object):

  def __init__(self):
    self.sessions = []
    self.get_sessions()

  def get_sessions(self):
    cmd = ['tmux', 'ls']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    self.tmux_out, self.tmux_err = proc.communicate()
    self.parse_session_data()

  def parse_session_data(self):
    for line in self.tmux_out.split('\n'):
      if not line:
        continue
      match = re.match('(.*): \d* windows \(.*\) \[.*\](.*)', line)
      if not match:
        raise Exception('Unable to match tmux output: {0}'.format(line))
      session_id = match.group(1)
      if 'attached' in match.group(2):
        session_state = 'attached'
      else:
        session_state = 'detached'
      session_data = TmuxSession(session_id, session_state)
      self.sessions.append(session_data)

class SessionSelection(object):
  
  def __init__(self, session_data):
    self.session_data = session_data
    self.choices = {}
    self.build_choices()
    self.render_options()
    self.read_choice()
    self.launch()

  def build_choices(self):
    sessions = []
    [sessions.append(s) for s in self.session_data if s.session_state == 'detached']
    [sessions.append(s) for s in self.session_data if s.session_state == 'attached']

    i = 0
    for s in sessions:
      i += 1
      self.choices[str(i)] = s

    self.choices['n'] = TmuxSession(session_id='new session',  session_state='new')

  def launch(self):
    session_data = self.choices[self.session_id]
    if session_data.session_state == 'new':
      session_name = str(raw_input('Session name?'))
      cmd = ['tmux', 'new-session', '-s', session_name]
    else:
      cmd = ['tmux', 'attach', '-t', session_data.session_id]
    os.execlp('tmux', *cmd)   
 
  def render_options(self):
   # print(chr(27) + "[2J")
    for s_id, s_data in self.choices.iteritems():
      print '{0}) {1} [{2}]'.format(s_id, s_data.session_id, s_data.session_state)

  def read_choice(self):
    self.session_id = str(raw_input('Make a selection:'))

if __name__ == '__main__':
  sessions = TmuxStatus().sessions
  SessionSelection(sessions)
