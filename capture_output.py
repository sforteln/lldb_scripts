#!/usr/bin/python

#command script import ~/git/lldb_scripts/lldb_utils.py
#script reload(lldb_utils)
#script help(lldb.SBFrame)

import lldb
import time
import os
import shlex
from optparse import OptionParser
from subprocess import call

def copy_to_paste_buffer(debugger, command, result, internal_dict):
  interpreter = debugger.GetCommandInterpreter()
  res = lldb.SBCommandReturnObject()
  # blindly pass everything passed to us to handleCommand()
  interpreter.HandleCommand(command, res)
  if res.Succeeded():
    print "result of " + command + " is now in copy buffer"
    # build shell command to pipe the debugger command's result to pbcopy so it ends up in the copy buffer
    #  split the debugger command's result on ' ' and skip over the result number and pointer(?) 
    #    and only return the actual result
    copy_cmd = "echo '"+res.GetOutput().split(" ",3)[3].rstrip()+"' | pbcopy"
    call(copy_cmd, shell=True)
    #print res.GetOutput().split(" ",3)[3]
  else :
    print "Command failed"


def write_to_file(debugger, command, result, internal_dict):
  """This command takes a lldb command and a file to write it to
  Ex. wf -f /tmp/lldb_output -c 'po self' """

  options = ParseWriteToFileCommands(command) 
  interpreter = debugger.GetCommandInterpreter()
  res = lldb.SBCommandReturnObject()
  # blindly pass everything passed to us to handleCommand()
  interpreter.HandleCommand(options.cmd, res)
  if res.Succeeded():
    print "wrote " + options.cmd + " to " + options.file
    # build shell command to pipe the debugger command's result to pbcopy so it ends up in the copy buffer
    #  split the debugger command's result on ' ' and skip over the result number and pointer(?) 
    #    and only return the actual result
    cmd_result = res.GetOutput().split(" ",3)[3]
    with open(options.file, "a") as myfile:
      myfile.write(cmd_result)
  else :
    print "Command failed"

def ParseWriteToFileCommands(command):
  parser = OptionParser()
  parser.add_option("-f", "--file", action="store", type="string", dest="file", default="/tmp/lldb_output" ,help="The file to write the results into [default]")
  parser.add_option("-c", "--cmd", action="store", type="string", dest="cmd",default="" ,help="the lldb command to write to the file [default]")
  (options, args) = parser.parse_args(shlex.split(command))
  return options

def __lldb_init_module(debugger, internal_dict):
  debugger.HandleCommand('command script add -f capture_output.copy_to_paste_buffer copy_to_paste_buffer')
  debugger.HandleCommand('command script add -f capture_output.copy_to_paste_buffer cpb')
  print 'The "copy_to_paste_buffer"(cpb) command has been installed and is ready of use'
  debugger.HandleCommand('command script add -f capture_output.write_to_file write_to_file')
  debugger.HandleCommand('command script add -f capture_output.write_to_file wf')
  print 'The "write_to_file"(wf) command has been installed and is ready of use.'
