# Novel Manager

Don't use it, it's outdated and unmaintained. I keep it there since it uses Kivy which is quite uncommon.

A simple novel scraper / manager in python.
Was made with mobile in mind but perfectly usable on pc




## Features

* Download novels by choosing the source.
    Currently lightnovelpub only but new sources are easy to implement

* Directly manage your novel library

* Export your novels as epub or pdf

* Directly read in your browser and save your progress automaticaly

* Open source and no ads


## Getting Started

### Dependencies

(result from pip list, what to install exactly bellow in Installing section)

Package            Version
------------------ ----------
    beautifulsoup4     4.10.0      
    certifi            2021.10.8 
    charset-normalizer 2.0.7     
    click              8.0.3     
    cloudscraper       1.2.58    
    colorama           0.4.4     
    docutils           0.18      
    EbookLib           0.17.1    
    Flask              2.0.2     
    fpdf2              2.4.6     
    idna               3.3       
    itsdangerous       2.0.1     
    Jinja2             3.0.3     
    Kivy               2.0.0     
    kivy-deps.angle    0.3.0     
    kivy-deps.glew     0.3.0     
    kivy-deps.sdl2     0.3.1     
    Kivy-examples      2.0.0     
    Kivy-Garden        0.1.4
    lxml               4.6.4
    MarkupSafe         2.0.1
    mypy-extensions    0.4.3
    pathspec           0.9.0
    Pillow             8.4.0
    pip                21.3.1
    platformdirs       2.4.0
    Pygments           2.10.0
    pyparsing          3.0.6
    pypiwin32          223
    pywin32            302
    regex              2021.11.10
    requests           2.26.0
    requests-toolbelt  0.9.1
    setuptools         58.3.0
    six                1.16.0
    soupsieve          2.3.1
    tomli              1.2.2
    typing_extensions  4.0.0
    urllib3            1.26.7
    Werkzeug           2.0.2
    wheel              0.37.0


### Installing :
No executable yet.
Tested only on ubuntu and windows 10.


* Installs dependencies by running :  
> pip install beautifulsoup4  
> pip install EbookLib  
> pip install cloudscraper  
> pip install Flask  
> pip install Kivy  
> pip install lxml  
> pip install fpdf2  
> pip install requests  
> pip install configparser  

* Run start.py

to add novel :
Only source currently is lightnovelpub  
In the bottom row :

    - select lightnovelpub in source

    - paste the novel name in the text input : https://www.lightnovelpub.com/novel/lord-of-the-mysteries-wn-19072354 -> lord-of-the-mysteries-wn-19072354

    - press "Add"



## Authors

jere344
discord : bygourou (jere344)#0802


## Version History

* 0.1
    * Initial Release

## Acknowledgments

* [README template](https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc)
* [cloudscraper](https://github.com/VeNoMouS/cloudscraper)
