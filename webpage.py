from flask import Flask, request, render_template
import status
app = Flask(__name__)

@app.route('/',methods = ['POST','GET'])
def home():
    #when a button is pushed on the webpage, the status file changes
    #after status changes, the form is changed by render() then returned
    #buttons are disabled not removed as changing button locations = bad UX
    statuses = status.STATUSES
    if request.method =='POST':
        if request.form['status'] in statuses:
            status.change_status(request.form['status'])
    #if it's the first time opening accessing form results causes a crash
    #so this is checks if it's post and if not it doesn't load form results
    #if it is the first time, the form is loaded and results aren't accessed
    return render()

#the following function disables/enables buttons and changes the page title
#the title is changed depending on the current status
#the button for the current status is disabled aswell
def render():
    current_status = status.get_status() #returns the whole dictionary
    return render_template('layout.html',
                           title = current_status['title'],
                           current_status = current_status,
                           statuses = status.STATUSES
                           )

if __name__ == '__main__':
    app.run(debug=True)
