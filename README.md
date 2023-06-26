#pygame_example

Created by QuantumKnight135
Created Date: 20/06/2023
Updated Date: 26/06/2023

# Installation

To install this game, simply download ArenaChallenge_WINDOWS_1.0_setup.exe in the `main` branch, and run through the installation wizard. You will then me able to run the executable ArenaChallenge.exe.


# Back Story

This project is a personalized version of a wonderfully done tutorial video by @ClearCode that I found on Youtube 
[ClearCode's Channel] (https://youtube.com/@ClearCode/videos)
. The base tutorial that I followed was his "Zelda in Python" tutorial, then I expanded my project based on his other tutorials. The point of this project is for my own personal education, and no money has been nor will be made by me in the sharing of this project.

The entire point of sharing this project is to get user and programmer feedback. I am an experienced software engineer, but I am new to python, pygame, and game development in general, so I know that there is going to be a lot that I do not know. If there is anything you like or dislike here, feel free to either let me know or to leave me forever wondering.


I have used at least one free art asset as described in the tutorial video, links will be provided below. As I expand my own ability with pixel art, I intend to utilize my own assets instead of anyone elses, simply so that I have the practice of creating each item that I want to display. I will leave the links for the assets that I have used, even after I stop using them, so that everyone can see where I have drawn inspiration.


# Tutorials that I have utilized:

So the obvious place that I started was with ClearCode's "Zelda in Python" tutorial, but anyone who looks at the code within the `00_example` directory will see that it is very different from what is in the main code directory. At the time of creating this repo, I had already utilized concepts that I learned in ClearCode's "A guide to level creation with Tiled". Between these two tutorials, and wanting to take a stab at my own art from the get go, I implemented some of the Tile Layers manipulation to figure out where sprites should be placed, instead of the csv files, and created a little tower library for a few of the enemy sprites to fight with the player. I did not add the grass elements, though I did put some of the code into my files so that I could eventually have something destructable in this version of the game. The biggest advantage that I see with this combination of tutorials was that I would be able to save resources, hopefully, when loading the map, as I don't have to step over every tile of the map over every csv file to place everything properly. Using Tiled's Tile Layers, I am able to grab a list of sprites directly, without worrying about all of the empty space.

Next, as I started getting this repo put together, I wanted to do a little bit of configuration control. I did some quick searching online, and found a lot of references to a tool called Pipenv. Apparently this tool is a recommended combination of pip and virtualenv, used for package management and virtual environments. Neat! I picked up a second capability for free. I have used a few methods of package management and virtualization before, but not having used this tool specifically, I grabbed a tutorial from:
[Corey Schafer] (https://www.youtube.com/@coreyms)
for "Python Tutorial: Pipenv - Easily Manage Packages and Virtual Environments". As I finish this tutorial, I am planning on setting up the first few pieces in a CI/CD pipeline. I am NOT planning on finishing this pipeline here. That will be for my next couple of projects. This is just to get the ball rolling on those skills as I finish up some last few updates that I want to make to this project. I have run into a few errors on my machine and trying to spin up the virtual environments, so I don't know if I will be able to make full use of it in this project. However, I will be working to integrate this tool into future projects, so I am still acknoledging Corey here for really getting me into Pipenv.

The third major thing that I wanted to figure out was how to put together an easy solution for less tech savvy people to install and try out this game. This requires an executable and setup/installer file pair that will allow users to download one file, install the game and all of its dependent packages, and easily run the game. The first part of this, the executable, was also discovered by a quick search. The current "hype" solution seems to be pyinstaller. This CLI tool combines some functionality of some older graphical applications, but is said to have better configuration. I haven't tried the older graphical applications, but pyinstaller is pretty nice. Out of the box, all you have to do is provide it with the entry point into your application, main.py, and with a few configuration options, it will create your executable file. Pair that with a program that creates an setup/installer file, of which there are a few to choose from, and I am able to accomplish what I set out to do. There were several tutorials online for pyinstaller, but each either showed a different setup/installer creation program, or denounced pyinstaller as unworthy of professional projects because of difficulties that were addressed in the other tutorials. In the end, I decided to go with 
[Python Simplified] (https://www.youtube.com/@PythonSimplified)
's tutorial, "Convert GUI App to Real Program - Python to exe to setup wizard". While Mariya covers a lot of the same information about pyinstaller that the other good tutorials do, she extends this into formatting your project to easily work with the software she uses to create the setup/installer file, Inno Setup. I definitely want to improve upon some of what she describes, but she had the best overall tutorial here, so acknoledgement goes to her.


# Art Asset Packs

Below is the information from the NinjaAdventure Asset Pack that I utilized through the tutorial.
<NinjaAdventure Pack README>
# Ninja Adventure Asset Pack

Assets created by:
[Pixel-boy](https://pixel-boy.itch.io/)
[AAA](https://www.instagram.com/challenger.aaa/?hl=fr)

# License

They are released under the Creative Commons Zero (CC0) license.

You can use any and all of the assets found in this package in your own games,
even commercial ones. Attribution is not required but appreciated.

# Placing one of these links somewhere would be awesome :)
Patreon: https://www.patreon.com/pixelarchipel 
Itchio Page: https://pixel-boy.itch.io/
Pack Page: https://pixel-boy.itch.io/ninja-adventure-asset-pack
</NinjaAdventure Pack README>
