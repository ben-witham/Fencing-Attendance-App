# Overview

This is my fencing attendance software! I have a club that I like to go to, but we're needing a better way to keep track of attendace with everyone. This software I'm building is hopefully to help fill that gap.

This sotware works entirely in terminal, and when you start the software, it gives you all the options that you can do. Selecting the normal sign-in option asks for your name. If this is your first time the database will create a new spot for you, and ask for you email so that we can contact fencers easily. If this is not your first time, the software will just increment the amount of times you've been at the club.

If you select the admin actions, it requires a password. If the correct password is given the admin can see the fencer's names, their emails, and the number of times they've been at the club.

[See it in action here!](https://youtu.be/ICHVUPGHFIM)

# Cloud Database

I'm using google Firebase for this project.

The database has a collection of fencers, and each fencer is saved as a document with their name as the document name
The database also has a collection for the password and the attendance dates, which is a feature not fully set up yet.

# Development Environment

The code was all written in python in VS Code. The firebase libraries were required to be able to communicate with the database.

# Useful Websites

* [Firebase, so you can actually have a cloud database](https://firebase.google.com/)
* [This site's tutorial was pretty helpful in figuring out what is happening with the database](https://www.tutorialspoint.com/firebase/index.htm)

# Future Work

* I want to add a day attendance feature, so the database keeps track of who was there on the day.
* A better password system, and maybe a more in-depth admin creation system
* Finally, I want to make this a web app so it's more user-friendly.