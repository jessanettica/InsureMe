from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = "SECRET"

###############################################
# Routes

@app.route('/')
def home():
	return render_template('base.html')

###############################################
# Main

if __name__ == '__main__':
	app.run(debug=True)