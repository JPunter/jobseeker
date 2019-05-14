Job Seeker Tool

Using the Reed API this program runs a job search based on user input. The returned data will then be passed to a PostGreSQL database.

Future features ideas: Frontend UI, probably tkinter initially. Check for overlapping jobId numbers in single output table

0.1: Currently the program outputs a search to a new table. This prevents data overlaps. The next update will have a feature to check that a certain jobId doesnt already exist in the database. Allowing for a single table to be built upon.
