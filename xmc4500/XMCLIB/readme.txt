The following modifications to the XMC-Lib library are neccesary in order to 
integrate it with this template:

(1) Include all header files using <> rather than "" - remove also the relative 
paths.

(2) Add the following line to the file
CMSIS/CMSIS/Infineon/XMC4500_series/Source/System_XMC4500.c in order to 
incorporate this function written in assembly.

----
extern int AllowPLLInitByStartup(void);
----
