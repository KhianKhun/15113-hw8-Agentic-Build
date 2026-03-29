# REFLECTION

1. My answer is yes, angent did do fully implement my spec. My guess is agent first try passed above 97% acceptance criteria. 

2. It is recorded in "intervaention log.md":
    -1  Prompt: Add file "README.md" and "gitignore"
    -2  I tested the program some times, where the process is based on "Behavior Description" and checked files based on "Features" requirment.
    -3  Prompt: To ensure the program remains bug-free, incorporate an "exit" function at every stage. Update the application description in `README.md`, while keeping the current terminal output display exactly as it is.
    -4  Change the "gitignore" and recheck program like the 2nd step.

3. I think AI review is really useful. I think my code has no bug in Phase 2, so AI review did not caught any actual bug which will crashed the program, also no anything is missed. Instead, it mentioned many warnings that I never consider about, the most important thing in my opinion is that my code stucture is not enough sturctual and difficult to maintain. It suggested me add new helper functions and change file structure to fix, which saves me much time.

4. I think a brainstorm and deep conversation with AI are necessary. Preciser and more detailed prompt will help AI generate better code, so people do need talk with AI to learn about what they want, such as file structure and algorithm. Also, I think we should write sudo codes in SPEC.md for file I/O or algorithom or some logic; then we send initial SEPC.md to AI for interation. 

5. I think this work flow is better than conversational back-and-forth for some small scale task. When I was using the agent, I saw the chat window cost 8k tokens (about 7% out of the chat window) one time to read my SPEC.md; however, the conversational back-and-forth will cost less token based on my experence. If our spec are more complex and longer, we need to pay more money to unlock token restriction. A possible solution is to divide that long task into several short sub-task and design clear and strict interface. Long and complex tasks without separation apply conversational back-and-forth; separated long task and short task should apply to plan-delegate-review, which can be all better than previous one in the common situation.