# LLDB scripts

## Note currently these commands don't work in swift projects but they do work with objc in Xcode 6.3

## Installation
---
#### adding to .lldbinit
(this will allow you to have access to the commands everytime you start xcode without having to manually import them each time)

1. Clone the repo
1. copy the .lldbinit file to your home dir or copy its contents to an existing .lldbinit file
1. copy the python scrupts to ~/LLDB or change the paths at the end of .lldbinit
1. restart lldb/xcode

#### Manually import into lldb or xcode(from the lldb prompt in the debugger window)


    command script import ~/git/lldb_scripts/frame_utils.py
    command script import ~/git/lldb_scripts/capture_output.py


## Frame utils
---
### print_stack_frame/psf
This function prints the class and function for a frame from the current stack.  This allows you to log a frame from the stack that is not the current frame.  So you could see what called the method that is at the top of the stack with  
    psf -i 1 -p "called by "  
  
#####Usage :
    
    psf -i 2 -p "stop called by "
    -i --index int(default=0) the index of the frame in the stack to print.  The current frame is zero
    -p --prefix string(default="") a string to prefix all log messages with

#####Example :
    Given a stack that looks like this. With the 0 frame being the current frame. 
    
    frame #0: -[ViewController loadView]
    frame #1: -[UIViewController loadViewIfRequired]
    frame #2: -[UIViewController view]
    frame #3: -[UIWindow addRootViewControllerViewIfPossible]
    frame #4: -[UIWindow _setHidden:forced:]
    frame #5: -[UIWindow _orderFrontWithoutMakingKey]
    frame #6: -[UIWindow makeKeyAndVisible]

#####Calling 
The debugger command can be called from either the lldb prompt or in a xcode breakpoint by  using the 'Debugger command' action.
    
    psf -i 1 -p "Called by "
#####yields

    Called by -[UIViewController loadViewIfRequired]

## Capture output
---
### copy_to_paste_buffer/cpb
This fucntion copies the output from a debugger command into the paste buffer

#####Usage : 
    cpb po self

#####Example :
    cpb po @"test"

    copies 'test' into you copy buffer

### write_to_file/wf
The function writes the result of the passed in debugger function into the passed in file.  If the passed in command does not begin with po or p then 'po' will be prepended to the passed in commnd.

##### Usage :
    wf -f /tmp/lldb_cmds -c 'po self'
    -f the file tio write the result to
    -c the debugger command wrapped in single quotes('po self')

### view_in_xcode/vx
The function writes the result of the passed in debugger function into a temp file and opens it in xcode. If the passed in command does not begin with po or p then 'po' will be prepended to the passed in commnd.

##### Usage :
    vx json

