from webgui.home import app

if __name__ == '__main__':
    app.run_server(debug=True, threaded=False, processes=1)