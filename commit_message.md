Fixed activity distribution bugs

# Bugs Removed
- latest commit was not added, some functins (input in particular) was incorrectly structured
- The incl_weekend and incl_weekday flags were not working outside their defaults values. Fixed this locating error to the way the offset days were being incremented and poorly structured if-else loop. 
- days were only being offset inside the if else loop, moved it outside. 

# Usability improvements
- Added view of how many additional days are needed in the case that the num of days was not sufficient to distribute the activity