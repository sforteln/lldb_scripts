# LLDB scripts

## Installation
1. Clone the repo
1. copy the .lldb file to your home dir or copy its contents to an existing .lldb file

###OR



## frame utils

### print_stack_frame/psf
  This function prints the class and function for a frame from the current stack.  This 
  allows you to log a frame from the stack that is not the current frame.  So you could 
  see what called the method that is at the top of the stack witj
    psf -i 1 -p "called by "  
  
####Usage :
    
    psf -i 2 -p "stop called by "
    -i --index int(default=0) the index of the frame in the stack to print.  The current frame is zero
    -p --prefix string(default="") a string to prefix all log messages with

####Example:
    Given a stack that looks like this. With the 0 frame being the current frame. 
    
    frame #0: -[ViewController loadView]
    frame #1: -[UIViewController loadViewIfRequired]
    frame #2: -[UIViewController view]
    frame #3: -[UIWindow addRootViewControllerViewIfPossible]
    frame #4: -[UIWindow _setHidden:forced:]
    frame #5: -[UIWindow _orderFrontWithoutMakingKey]
    frame #6: -[UIWindow makeKeyAndVisible]

#####Calling 
   The debugger command can be called from either the lldb prompt or in a xcode breakpoint by using the 'Debugger command' action.
    
    psf -i 1 -p "Called by "
#####yields

    Called by -[UIViewController loadViewIfRequired]

  
