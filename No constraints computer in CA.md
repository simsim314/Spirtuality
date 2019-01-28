Current computer architectures are limited in both, the command range and the input size. Practically computers are not limited to 64 bit integers, and can emulate big integers of any size. But we don't have "dynamic" architectures (not that I know of), where we can code new commands, and we are not limited only to N bits. In CA we can in general code addition of any two integers as big as they come, representing numbers by stream of gliders. This is in theory could be translated into electrical charges. 

Lets place ourselves into CA with universal construction and computation. Imagine a decision tree (command tree) which can open and close gate by different gliders. So we can travel inside this tree redirecting the gates by gliders. Every command to the computer, starts from path inside this tree. Inside it there are "nodes" and there are "leaves". Each node is just redirecting the stream of gliders left or right, and every leaf can do something complex as the CA allows, which is basically everything. 

So for example we start at the root: and say 1 will mean Add, and 0 will mean Multiply. Then we need a signal, when does one integer ends and the other begins. How would we do this if we only have two bits? We would code every digit with 0 prefix. So for example we have 7: 111 and we will code it (01)(01)(01). And to code the next digit we will use 1 prefix and then the same. So for example the code for adding 5 + 7 will look like this: 
(1) - addition 
(01)(00)(01) - 5 
(1) - end of integer 
(01)(01)(01) - 7
(1) - end of integer 

So the code will look like: 101000110101001. This is a code that moves from the root to the adder leaf, and inside it it loads two integers 5 and 7 and they can be arbitrary large. How the result is returned is the next issue. 

One of the things we should notice that many times one leaf would like to send command to another leaf. Like in every programming language we would like functions in our code to be able to call other functions in our code. This is why each "callable" leaf, needs the following structure: 

Request: (helper command)(inputs for the leaf)(sender command) - this is how the information is passing from leaf to leaf inside the tree. 

So for example if we would like to use addition inside Multiplication of 5 and 7 we would use the following code: 
The input would be: 001000110101001 - we will have two integers 101 and 111.
Now I assume that we can define variables and make loops inside a leaf (but loop can also be a function inside the tree):

Create variable x = 0. 
Loop(101):
x = Add(x, 111) (here we call the root with command, 0, (x, 7), 1 and wait)
call root "print command" x

Now in order to call some other function, we need to have an inherent capability of every leaf to send message to the root. How this is done is beyond the scope of this issue, but in practice in CAs this is doable. So for example if someone asks some function to calculate something, it sends request to the root, and each smart enough leaf will know to send back to the root the result stream of the type: 

Result: (sender command)(results of calculation)

As the sender will wait for the result, after the result will come, this is up to the sender leaf to know what to do with it. We just make sure that the command tree design is supporting this option. 

Some example of problem that can rise from this design is recursion. If function is in the middle of and execution and it calls itself to make a calculation, or it calls some other function that calls the first one, this can collapse the system. So this is not a mistake free system in any way. This is up to the designers of the leafs to make sure that when they call some other function they know enough of what they are doing (like designing a stack of data for recursion). We can have some design patterns automated for this purpose, yet this is in the hands of the leaf designers. 

Now the best part of this idea can exist only in CA with universal construction. Because we can have version control and inherent part of our computer. The only thing we need to add, is a code that creates and destroys components inside this computer. So when we call a code with some version, the version loads the code that creates the whole computer. Each new version of the computer is coded inside a universal constructor. Each leaf and node of the command tree, can first be rebuilt from version 0 to version N, and then some specific code of version N can run. Every new version of the computer say version N + 1, is deleting some of the leafs replacing them by nodes, and moving the leafs downwards the tree stream (see note 3 for improved design). 

I wonder have anyone had or heard of this idea ? Or maybe someone implemented it on some emulator? I think FPGA guys should be able to think about this stuff. I was also thinking of implementing it in GeminoidParticles rule where there are reflections, duplications, and construction of any static unit but not particles - this reflects nicelly the distinction between the signal and the hardware, which usually not that clear in CAs as in reality. 

*Note* There is no need to differentiate the code and the execution. The execution is just another leaf which start to read some tape, and this is where it all originates. Not in the root but in this leaf. This leaf is somewhat special as it takes the first argument how many bits to read, then it reads those bits and sends them to the root node. And from this point onwards everything is as usual. We just need to start the execution from somewhere. 

*Note 2* Obviously something more esoteric in CA which is impossible to make in physical computer like calling a leaf with universal constructor, and generate a stream that makes another temporary leaf is also an option. 

*Note 3* Although the versions are controllable true back compatibility is an issue. But one can notice that every specific node can be only one of two things. A leaf or a node. We can make sure that each leaf is also node friendly, and we can run at first some version generator, that will not create everything from scratch, but will define the active component to be a leaf or a node. Inside each "node friendly leaf" there will a version when it became a node from a leaf, and if the current version is higher then a node will be activated. This is some sort of initialization that can be done at first as part of design pattern of the tree. Each version will need to have a special node which will return result command to the root - call the execution node once again the version is now initialized.

*Note 4* As I mentioned earlier each node is a gate which redirects the rest of the stream. One important issue should be managed in the command tree, when the command is happy and understands the input finished to be loaded, it needs to reinitialize the gate. This property is part of the node design - each node is sending its parent node everything is finished loading reinitialize back into the neutral state.
