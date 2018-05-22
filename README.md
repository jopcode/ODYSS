
[![buycoffee](https://az743702.vo.msecnd.net/cdn/kofi2.png?v=0)](https://ko-fi.com/X7X7D)

# Odyss a Tool for Pentesting using Python

Odyss is a tool in python, with this tool you can find possible vulnerable websites using a dork (index.php?id=). This tools is based on another tool created for my ( WhoUr ). Odyss use SearX on your localhost or oficial server.
Install

1) First you need clone the repository with :

    git clone https://github.com/jopcode/odyss

2) Next your need enter inside the folder and install the requirements with (I recommend use virtualenv for install requirements):

    cd odyss && pip install -r requirement.txt

3) Execute Odyss

    python odyss.py
![image](https://gyazo.com/eb5c5741b6a9a16c692170a41a49c858.png | width=100)
## Instructions
1) Starting Odys " python odyss.py"
All params except “Enter your query to SearX” has default yes or 1 in case of number of pages.
When the tools has been finished of testing every page this display a option for save or not the found vulnerable sites in file named sites.txt
At the end the script display a table with all sites vulnerable.

I am not responsible for the misuse that someone gives to this tool, this tool was created with the only purpose that the learning.

You can see more about this [here](https://medium.com/@jopcodecl/odyss-a-tool-for-pentesting-using-python-6c3e6777007b)
