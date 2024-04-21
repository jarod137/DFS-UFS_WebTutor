# DFS-UCS_WebTutor
## By: Jared Kaiser & Bryce Bales
This is a project for CS 475: Artificial Intelligence. It is a web-based program to show users how to use the DFS and UFS search algorithms.

## HOW TO USE
To use this program, run the Main.py file and click the link in the output. This will take you to a window in your browser where the graph will be with buttons and descriptions of the algorithms as well as the sources they are taken from. The buttons are DFS(Runs Depth-First Search), UCS(Runs Uniform-Cost Search), and Sleep(Slows down visualization). You can also click the descriptions for a link to the website sited.

## The Problem:
Search algorithms can often be hard to gauge whenever we are just looking at static images and numbers describing the algorithms. We want to help students understand how BFS and DFS work by making a visual representation using a GUI with a short description next to it. By doing this we aim to make the mystique behind how these search algorithms work no longer a mystery, but something that is easier to grasp and understand.

## Our Plan:
We plan to make a web-based program using HTML and CSS for the front end and using Python for the back end to get the visual representation to move. We are combining techniques by using different front-end and back-end languages. The problem is small enough to be completed on time because we are only using 2 search algorithms and we both have prior experience in HTML, CSS, and Python. We foresee the animation of the proper implementation of each search algorithm to be a challenge as well as making sure that the back end works seamlessly with the front end.

## The Implementation:
We have made this program by using a python library called "Dash" which allows us to make a visual representation of our tree as well as our search algorithms. For UCS we used a queue, a visited flag, and a while loop to iterate through visited and unvisited nodes. For DFS we used a stack, a visited flag, and a while loop to iterate through visited and unvisited nodes. We then generated our graph to show in a window with Dash and programmed the graph to iterate and visualize whats going on alongside each algorithm. We then initialize the Dash app and define the layout of the Dashapp. Here we have some descriptions and works cited websites linked to them. We then added functional buttons that run UCS and DFS as well as a Sleep button that will slow down the speed of the visualization to a more reasonable speed.

## References:
https://www.educative.io/answers/what-is-uniform-cost-search

https://brilliant.org/wiki/depth-first-search-dfs/#:~:text=Depth%2Dfirst%20search%20(DFS)%20is%20an%20algorithm%20for%20searching,path%2C%20and%20then%20explores%20it.

https://community.plotly.com/t/building-interactive-collapsible-tree-on-dash/8059/7
