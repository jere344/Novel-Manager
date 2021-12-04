if __name__ == "__main__":
    import flaskapp
    import webbrowser

    webbrowser.open("http://localhost:5000/index")
    flaskapp.app.run()
