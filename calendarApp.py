from flask import Flask, render_template, request, redirect, url_for
import calendar
from datetime import datetime, timedelta

app = Flask(__name__)

#Homepage displays current month
@app.route('/')
def generate_Calendar():
    #Get current year and month
    thisMonth = datetime.now()
    year = thisMonth.year
    month = thisMonth.month

    # Set Sunday as the first day of the week
    calendar.setfirstweekday(calendar.SUNDAY)

    #display Calendar
    cal = calendar.monthcalendar(year, month)
    #Create a Calendar list that holds a week list to iterate through each day of the week 
    calendar_data = [[day if day != 0 else " " for day in week] for week in cal]

    return render_template('calendar.html', year=year, month=month, calendar_data=calendar_data)

@app.route('/update_month/<int:year>/<int:month>', methods=['GET', 'POST'])
def update_month(year, month):
    # Set Sunday as the first day of the week
    calendar.setfirstweekday(calendar.SUNDAY)

    if request.method == 'POST':
        direction = request.form['direction']

        if direction == 'prev':
            # Decrease month
            # Create a new_date object with the current year, month and first day. Then subtract one day to change the month
            new_date = datetime(year, month, 1) - timedelta(days=1) #timedelta(days) changes the entire date if the correct conditions are met
        elif direction == 'next':
            # Increase month
            # Create a new_date object with the current year, month and 28th day. Then add 4 days to change the month (takes Feburary into account)
            new_date = datetime(year, month, 28) + timedelta(days=4)

        #update the url for this route passing the new year and month
        return redirect(url_for('update_month', year=new_date.year, month=new_date.month))

    # Display Calendar
    cal = calendar.monthcalendar(year, month)
    #Create a Calendar list that holds a week list to iterate through each day of the week
    calendar_data = [[day if day != 0 else " " for day in week] for week in cal]

    return render_template('calendar.html', year=year, month=month, calendar_data=calendar_data)

#Display current week
@app.route('/week')
def week():
    #Get current year and month
    thisMonth = datetime.now()
    year = thisMonth.year
    month = thisMonth.month

    # Set Sunday as the first day of the week
    calendar.setfirstweekday(calendar.SUNDAY)

    #display Calendar
    week = calendar.monthcalendar(year, month)[1]
    #Create a Calendar list that holds a week list to iterate through each day of the week 
    calendar_data = [day if day != 0 else " " for day in week]

    return render_template('week.html', year=year, month=month, calendar_data=calendar_data)



eventList =[]

@app.route('/tasksAndEvents/<int:year>/<int:month>/<int:day>')
def display_events(year, month, day):
    selectedDate = f"{year}-{month:02d}-{day:02d}"

    dateEvents = [event for event in eventList if event[2] ==selectedDate]

    return render_template('tasksAndEvents.html', eventList = dateEvents)

@app.route('/form', methods = ['GET'])
def render_add_event():
    return render_template('form.html')

@app.route('/add_event', methods =['POST'])
def add_event():
    event_name = request.form.get('event_name')
    event_date = request.form.get('event_date')
    isTask = 1 if request.form.get('isTask') else 0

    eventList.append((len(eventList) + 1, event_name, event_date, isTask, 0))
    return redirect(url_for('render_add_event'))

#Add the option to run this file directly
if __name__=='__main__':
    app.run(debug=True)