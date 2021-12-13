import lib


def GenerateHTML():
    style_font = lib.style.get("WEBVIEWER", "font")
    style_textcolor = lib.style.get("WEBVIEWER", "textcolor")
    style_backgroundcolor = lib.style.get("WEBVIEWER", "backgroundcolor")

    css = f"""@font-face {{
        font-family: "{style_font}";
        src: url("DATA/{style_font}");
    }}

    p {{
        font-family: "{style_font}"; 
        color:{style_textcolor}; 
    }}

    h1 {{
        color:{style_textcolor}; 
        font-family: "{style_font}";
        text-align:center;
    }}

    div.content {{
        white-space:pre-wrap ;
        width:50%;
        margin:auto;
    }}"""

    html = f"""
    <HTML>

        <HEAD>
            <meta charset="UTF-8">
            <TITLE>Novel Manager First Use Tutorial</TITLE>
            <style>{css}</style>
        </HEAD>

        <BODY style="background-color:#101010">
            <div class="content">
                <h1>First use :</h1>

                <p>
    First you will need to download some novel.<br>
    * To do that, go on <a href="https://www.lightnovelpub.com/">lightnovelpub</a>, the only source currently
    available<br>
    * Then choose the novel you want to add. Here we will take Lord Of The Mysteries.<br>
    * Copy only the novel name from the url :<br>
        https://www.lightnovelpub.com/novel/lord-of-the-mysteries-wn-19072354 
        =>  lord-of-the-mysteries-wn-19072354<br>
    * Go back to Novel Manager app and paste it in the add novel input at the bottom of the app.<br>
    * Select lightnovelpub from the menu next to the button "Add"<br>
    * Click on the add button, wait a few second and that's it, you now have your first novel, you can now download chapters and read them thought the web reader of export them as epub or pdf<br>


    More info on <a href="https://github.com/jere344/Novel-Manager">github</a>
                </p>
            </div>
        </BODY>

    </HTML>

    """
    with open(str(lib.__location__.joinpath("first-use.html")), "w") as html_file:
        html_file.write(html)


def AndroidOpenHTML():
    pass  # TODO


def DesktopOpenHTML():
    import webbrowser

    webbrowser.open("file://" + str(lib.__location__.joinpath("first-use.html")))
