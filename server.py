import Pyro4
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
Leader = None

@app.route("/")
def getLeader():
	global Leader
	try:
		node = Pyro4.Proxy("PYRONAME:C")    # use name node object lookup uri shortcut
		Leader = node.findLeader()
		return(Leader)
	except:
		try:
			node = Pyro4.Proxy("PYRONAME:B")    # use name node object lookup uri shortcut
			Leader = node.findLeader()
			return(Leader)
		except:
			try:
				node = Pyro4.Proxy("PYRONAME:A")    # use name node object lookup uri shortcut
				Leader = node.findLeader()
				return(Leader)
			except:
				return "no nodes is on"

@app.route("/data", methods=['GET', 'POST'])
def data():
	getLeader()
	if request.method == 'POST':
		data = request.form
		print Leader
		lead = Pyro4.Proxy(Leader)
		lead.setData(data)
		return render_template("index.html",data = data)

		
	return render_template("form.html")

if __name__ == '__main__':
	app.run(debug=True)



