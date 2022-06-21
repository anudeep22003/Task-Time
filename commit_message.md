Removed bugs and minor experience improvements

# Bugs Removed
- Entering a number at the beginning was an uncaught exception causing the program to crash. Addressed this in the while loop to only accept valid preset choices.
- The number formating on some views was showing float when it should show int, fixed that.
- Adding a note or context to a daughter was added to the same line. Some rejigging of next line needed to be done to improve capture. 

# Usability improvements
- The better user experience is one where the user only adds notes to a task. When creating a daughter, the notes are copied as the context of the daughter. This leaves the note section empty and relevant to today. 