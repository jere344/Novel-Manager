#!/usr/bin/python

from flask import Flask, render_template_string, send_from_directory, redirect
import lib

app = Flask(
    __name__,
    static_url_path=f"/{lib.__location__}",
    static_folder="DATA",
)

style_font = lib.style.get("WEBVIEWER", "font")
style_textcolor = lib.style.get("WEBVIEWER", "textcolor")
style_backgroundcolor = lib.style.get("WEBVIEWER", "backgroundcolor")

css = f"""                  
        @font-face {{
            font-family: "{style_font}"; 
            src: url("{{{{  url_for("static", filename="{style_font}") }}}}");
        }}

        p {{
            font-family: "{style_font}"; 
            color:{style_textcolor}; 
        }}

        p.scroll {{
            font-size:12px;
        }}
        h1 {{
            color:{style_textcolor}; 
            font-family:"{style_font}";
            text-align:center;
        }}

        div.content {{
            white-space:pre-wrap ;
            align:center; 
            margin:auto;
        }} 

        div.scroll {{
            position: fixed;
            right: 50;
        }}

        a.home {{
            color:{style_textcolor};
            font-size: 300%;
            text-decoration: none;
        }}

        div.home {{
            position: fixed;
            left: 25;
        }}
"""


def GenerateChapter(novel: str, chapter: int) -> str:
    # chapterinfo = [number, title, sourcelink]
    from os.path import isfile

    if not isfile(
        str(
            lib.__location__.joinpath("DATA/", novel, f"{novel} chapter {chapter}.txt")
        ),
    ):
        html = f"""
        <HTML> 
            <HEAD>
                <TITLE>{novel}</TITLE>
                <style>{css}</style>
            </HEAD>
            <BODY style="background-color: {style_backgroundcolor}">
                <div class="content" style="width:{lib.style.get("WEBVIEWER", "chapterwidth")};">
                    <p>This chapter hasn't been downloaded <br>
                    <br>
                    To download chapter, start the app and click the download buttons.<br>
                    If you want to do it without the gui you can execute in misc.py:<br>
                    >>> SetChapter(novel, chapter_number) <br>
                    <br>
                    <br>
                    More info on <a href="https://github.com/jere344/Novel-Manager">github</a>
                    </p>
                </div>
            </BODY>
        </HTML>
        
        """
        return html

    chapterinfo = lib.chapterlist.get(novel, str(chapter)).split("/split/")

    with open(
        str(
            lib.__location__.joinpath("DATA/", novel, f"{novel} chapter {chapter}.txt")
        ),
        "r",
        encoding="utf-8",
    ) as file:
        content = "".join(file.readlines()[1:])

    html = f"""
    <HTML> 
        <HEAD>
            <TITLE>{novel}</TITLE>
            <style>
                {css}
                a.button_navigation {{
                    -webkit-appearance: button;
                    -moz-appearance: button;
                    appearance: button;

                    background-color:  #2d73e7; 
                    color: #c9cbce;
                    padding: 8px 15px;
                    text-align: center;
                    text-decoration: none;
                    border-radius: 4px;
                    align-items: center;
                    font-size: 30px;
                }}
            </style>
        </HEAD>
        <BODY style="background-color: {style_backgroundcolor}">
            <div class="home"><a class="home" href="http://localhost:5000/">⌂</a></div>
            <div class="content" style="width:{lib.style.get("WEBVIEWER", "chapterwidth")};">
                <h1>{chapterinfo[0]}. {chapterinfo[1]}</h1>
                <p>{content}</p> 
                <table style="margin-left: auto ; margin-right: auto;">
                    <tr>
                        <td><a class="button_navigation" href="http://localhost:5000/{novel}/{chapter-1}">❮</a></td>
                        <td><a class="button_navigation" href="http://localhost:5000/{novel}/index">☰</a></td>
                        <td><a class="button_navigation" href="http://localhost:5000/{novel}/{chapter+1}">❯</a></td>
                    </tr>
                </table
            </div> 
        </BODY> 
    </HTML>
    """

    return html


def NovelIndex(novel: str) -> str:
    content = ""
    i = 1
    from textwrap import shorten

    for element in lib.chapterlist.items(novel):
        net_chapter = element[1].split("/split/")[0:2]
        # if chapter name is too long put ... instead
        # texteraper.shorten don't cut words
        text = f"{net_chapter[0]}. {shorten(net_chapter[1].strip(), width=35, placeholder='...')}"
        content += f"""<li id="{i}"class="{"black" if i%4 in [1, 2] else "white"}" style="{"margin:0 0 0 0;" if i%2 else "margin:0 0 0 5%;"}"><a href="http://localhost:5000/{novel}/{i}"><p>{text}</p></a></li>"""
        i += 1

    scroll = ""
    interval = 100
    for j in range(int(i / interval) + 1):
        scroll += f"""<p class="scroll" onClick="document.getElementById('{j*interval if j else 1}').scrollIntoView();" />{j*interval if j else 1}</p>"""

    html = f"""
    <HTML>
        <HEAD>
            <TITLE>Index of {novel}</TITLE>
                <style>
                    {css}
                    li a {{
                        text-decoration: none;
                        display:block;
                        width: 100%; 
                        height: 100%;
                        margin-left:5%;
                    }}

                    ul {{
                        margin: 0;
                        list-style-type: none;
                        box-sizing: border-box;
                    }}

                    ul li {{
                        border-bottom: 1px solid #5e5e5f;

                        float:left;
                        width:45%;
                        height: 60px;
                    }}

                    ul li.black {{
                        background-color: #121518;
                    }}

                    ul li.white {{
                        background-color: #252729;
                    }}

                    ul li:hover {{
                        background-color: #404a6f;
                        border-bottom: 1px solid  #26336a ; 
                    }}

                    li a p {{
                        display: table-cell; 
                        vertical-align: middle; 
                        height:57px;
                    }}
                </style>
        </HEAD>
        <BODY style="background-color: {style_backgroundcolor}">
            <div class="home"><a class="home" href="http://localhost:5000/">⌂</a></div>
            <div class="scroll">{scroll}</div>
            <div class="content" style="width:{lib.style.get("WEBVIEWER", "indexwidth")};">
                <h1>{lib.config.get(novel, "cleanname")}</h1>
                <ul>{content}</ul>
            </div>
        </BODY>
    </HTML>
                    
    """

    return html


@app.route("/<novel>/<chapter>")
def Chapter(novel: str, chapter: str):
    # If you put "index" in the url instead of a number load GenerateIndex(novel)
    if chapter == "index":
        return render_template_string(NovelIndex(novel))

    # Else load the chapter
    if int(chapter) == 0:
        return redirect(f"http://localhost:5000/{novel}/1")
    html = GenerateChapter(novel, int(chapter))

    # for exemple if you go to page chapter 9, set the chapter 8 as read.
    lib.config.set(novel, "chapterread", str(int(chapter) - 1))
    with open(
        lib.__location__.joinpath("config.ini"), "w", encoding="utf-8"
    ) as configfile:
        lib.config.write(configfile)

    return render_template_string(html)


@app.route("/")
@app.route("/index")
def GlobalIndex():

    novel_list = lib.config.sections()

    i = 1
    content = ""
    for novel in novel_list:
        novel_pic = lib.config.get(novel, "picture")
        # get picture path without -resized
        novel_pic = novel_pic[5:-12] + novel_pic[-4:]

        summary = lib.config.get(novel, "summary").replace("\n", "<br>")

        content += f"""
        <tr id="{i}">
            <td>
                <a href="http://localhost:5000/{novel}/index">
                    <img src="{{{{ url_for('static', filename='{novel_pic}') }}}}">
                </a>
            </td>

            <td>
                <h1>{lib.config.get(novel, "cleanname")}</h1>
                <p>{summary}</p>
                <nav>
                    <a style="margin:5px" href="http://localhost:5000/{novel}/1">
                        <span>Read chapter 1</span>
                    </a>
                    
                    {f'''
                    <a style="margin:5px" href="http://localhost:5000/{novel}/{int(lib.config.get(novel, "chapterread")) + 1}">
                        <span>Read chapter {int(lib.config.get(novel, "chapterread")) + 1}</span>
                    </a>''' 
                    if not lib.config.get(novel, "chapterread") == "0" else ""}
                    
                </nav>
                <a href="{lib.config.get(novel, "url")}">source</a>
            </td>
        </tr>"""
        i += 1

    scroll = ""
    interval = 5
    for j in range(int(i / interval) + 1):
        scroll += f"""<p class="scroll" onClick="document.getElementById('{j*interval if j else 1}').scrollIntoView();" />{j*interval if j else 1}</p>"""

    html = f"""
    <HTML>
        <HEAD>
            <TITLE>Novel Scraper Index</TITLE>
                <style>
                    {css}
                    nav a {{
                        padding: 5px 12px;
                        height: 35px;
                        width: 20%;
                        border-radius: 6px;
                        text-transform: uppercase;
                        background-color: #4470b9;
                        border: 1px solid #6e8cbd;
                        text-decoration: none;
                        color: #ececec;
                        justify-content: center;
                        align-items: center;
                        display: flex;
                        
                        
                    }}

                    nav {{
                        display: flex;
                    }}
                </style>
        </HEAD>
        <BODY style="background-color: {style_backgroundcolor}">
            <div class="scroll">{scroll}</div>
            <div class="content", style="width:{lib.style.get("WEBVIEWER", "indexwidth")}">
                <h1>Novel Scraper Index</h1><br><br><br><br>
                <table>{content}</table>
            </div>
        </BODY>
    </HTML>
    """

    with open(
        lib.__location__.joinpath("config.ini"), "w", encoding="utf-8"
    ) as configfile:
        lib.config.write(configfile)

    return render_template_string(html)


@app.route("/favicon.ico/")
def favicon():
    return send_from_directory("DATA", path="favicon.ico")
