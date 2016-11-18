from bottle import route, run, static_file
import webbrowser

@route('/')
def home():
    return static_file("index.html", root="", mimetype='text/html')

@route('/bootstrap/js/<filename:re:.*\.js>')
def getBS(filename):
    return static_file(filename, root="bootstrap/js", mimetype='text/javascript')

@route('/scripts/<filename:re:.*\.js>')
def getScript(filename):
	return static_file(filename, root="scripts", mimetype='text/javascript')

@route('/bootstrap/css/<filename:re:.*\.css>')
def getBSC(filename):
	return static_file(filename, root="bootstrap/css", mimetype='text/css')

@route('/css/<filename:re:.*\.css>')
def getCSS(filename):
	return static_file(filename, root="css", mimetype='text/css')

@route('/fonts/<filename:re:.*\.woff>')
def getCSS(filename):
	return static_file(filename, root="fonts", mimetype='application/x-font-woff')

@route('/fonts/<filename:re:.*\.woff2>')
def getCSS(filename):
	return static_file(filename, root="fonts", mimetype='application/x-font-woff2')

@route('/fonts/<filename:re:.*\.ttf>')
def getCSS(filename):
	return static_file(filename, root="fonts", mimetype='application/x-font-ttf')

@route('/bootstrap/fonts/<filename:re:.*\.woff>')
def getCSS(filename):
	return static_file(filename, root="bootstrap/fonts", mimetype='application/x-font-woff')

@route('/bootstrap/fonts/<filename:re:.*\.woff2>')
def getCSS(filename):
	return static_file(filename, root="bootstrap/fonts", mimetype='application/x-font-woff2')

@route('/bootstrap/fonts/<filename:re:.*\.ttf>')
def getCSS(filename):
	return static_file(filename, root="bootstrap/fonts", mimetype='application/x-font-ttf')

@route('/post/<key>')
def api(key):
	if (key == "click"):
		return "Click event called"
	elif(key == "test"):
		return "backend connected!"
	else:
		return "API call for: " + key


webbrowser.open("http://localhost:8080/")

run(host='localhost', port=8080, debug=True)

