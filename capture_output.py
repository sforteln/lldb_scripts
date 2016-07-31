#!/usr/bin/python

#command script import ~/git/lldb_scripts/lldb_utils.py
#script reload(lldb_utils)
#script help(lldb.SBFrame)
#log enable -f /tmp/lldb-log.txt lldb api process

import lldb
import time
import os
import shlex
from optparse import OptionParser
import subprocess
import uuid

def copy_to_paste_buffer(debugger, command, result, internal_dict):
  interpreter = debugger.GetCommandInterpreter()
  res = lldb.SBCommandReturnObject()
  # if the passed in command doesn't start with po or p prefix it
  if command.startswith('p')==False :
    command = "po {0}".format(command)
  interpreter.HandleCommand(command, res)
  if res.Succeeded():
    #print >>result,"result of '{0}' is now in copy buffer".format(command)
    copy_cmd = "echo '{0}' | pbcopy".format(res.GetOutput())
    subprocess.call(copy_cmd, shell=True)
  else :
    print >>result,"Command failed"

def view_in_xcode(debugger, command, result, internal_dict):
  """This command writes the commands output into a temp file and opens it in xcode """
  view_in("Xcode.app",command,debugger,result, internal_dict)

def view_in(debugger,command,result, internal_dict):
  """This command writes the commands output into a temp file and opens it in xcode """
  temp_filename = "/tmp/{0}".format(uuid.uuid4())
  parser = view_in_commands_parser()
  (options, args) = parser.parse_args(shlex.split(command))
  if not options.cmd:
      result.PutCString("the command(-c) is required")
      return
  result = write_cmd_to_file(debugger,options.cmd, temp_filename)
  if result:
    # open with xcode
    subprocess.Popen(["open" ,"-a" ,options.app,temp_filename])
   

def write_to_file(debugger, command, result, internal_dict):
  """This command takes a lldb command and a file to write it to
  Ex. wf -f /tmp/lldb_output -c 'po self' """
  
  parser = write_to_file_commands_parser()
  (options, args) = parser.parse_args(shlex.split(command))
  if not options.cmd:
      result.PutCString("the command(-c) is required")
      return
  write_cmd_to_file(debugger,options.cmd,options.file)

def write_cmd_to_file(debugger,command, filename):
  interpreter = debugger.GetCommandInterpreter()
  res = lldb.SBCommandReturnObject()
  if command.startswith('p')==False :
    command = "po {0}".format(command)
  interpreter.HandleCommand(command, res)
  
  if res.Succeeded():
    print "wrote {0} to {1}".format(command,filename)
    cmd_result = res.GetOutput()
    with open(filename, "a") as myfile:
      myfile.write(cmd_result)
    return True
  else :
    print "Command failed"
    return False

def view_in_commands_parser():
  parser = OptionParser()
  parser.add_option("-a", "--app", action="store", type="string", dest="app", default="Xcode.app" ,help="The app to open the request in 'open -a <tempfile>' [default]")
  parser.add_option("-c", "--cmd", action="store", type="string", dest="cmd",help="the lldb command to write to the file [default]")
  return parser

def write_to_file_commands_parser():
  parser = OptionParser()
  parser.add_option("-f", "--file", action="store", type="string", dest="file", default="/tmp/lldb_output" ,help="The file to write the results into [default]")
  parser.add_option("-c", "--cmd", action="store", type="string", dest="cmd",help="the lldb command to write to the file [default]")
  return parser

def __lldb_init_module(debugger, internal_dict):
  debugger.HandleCommand('command script add -f capture_output.copy_to_paste_buffer copy_to_paste_buffer')
  debugger.HandleCommand('command script add -f capture_output.copy_to_paste_buffer cpb')
  print 'The "copy_to_paste_buffer"(cpb) command has been installed and is ready of use'
  debugger.HandleCommand('command script add -f capture_output.write_to_file write_to_file')
  debugger.HandleCommand('command script add -f capture_output.write_to_file wf')
  print 'The "write_to_file"(wf) command has been installed and is ready of use.'
  debugger.HandleCommand('command script add -f capture_output.view_in_xcode view_in_xcode')
  debugger.HandleCommand('command script add -f capture_output.view_in_xcode vx')
  debugger.HandleCommand('command script add -f capture_output.view_in vi')
  print 'The "view_in_xcode"(vx) command has been installed and is ready of use.'
