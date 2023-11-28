from flask import Flask, render_template, request, redirect, url_for
import calendar
from datetime import datetime, timedelta, date


app = Flask(__name__)


#Create dictionary to set number to month
set_month = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

eventList =[]

#Homepage displays current month
@app.route('/')
def generate_Calendar():
    #Get current year and month
    thisMonth = datetime.now()
    year = thisMonth.year
    month = thisMonth.month

    # Get word Month from dictionary using value. Use "Invalid Month" if number value is invalid
    wordMonth = set_month.get(month,'Invalid Month')

    # Set Sunday as the first day of the week
    calendar.setfirstweekday(calendar.SUNDAY)

    #display Calendar
    cal = calendar.monthcalendar(year, month)
    #Create a Calendar list that holds a week list to iterate through each day of the week 
    calendar_data = [[day if day != 0 else " " for day in week] for week in cal]

    return render_template('calendar.html', year=year, month = month, wordMonth=wordMonth, calendar_data=calendar_data)



@app.route('/update_month/<int:year>/<int:month>', methods=['GET', 'POST'])
def update_month(year, month):
    # Set Sunday as the first day of the week
    calendar.setfirstweekday(calendar.SUNDAY)

    if request.method == 'POST':
        direction = request.form['direction']

        if direction == 'prev':
            # Decrease month
            month -= 1
            if month == 0:
                # If month becomes 0 set to previous year December
                month = 12
                year -= 1
        elif direction == 'next':
            # Increase month
            month += 1
            if month > 12:
                # If month is greater than 12 set to next year January
                month = 1
                year += 1
        
        #update the url for this route passing the new year and month
        return redirect(url_for('update_month', year=year, month=month))
    
    # Get word Month from dictionary using value. Use "Invalid Month" if number value is invalid
    wordMonth = set_month.get(month,'Invalid Month')

    # Display Calendar
    cal = calendar.monthcalendar(year, month)
    #Create a Calendar list that holds a week list to iterate through each day of the week
    calendar_data = [[day if day != 0 else " " for day in week] for week in cal]

    return render_template('calendar.html', year=year, month=month, wordMonth = wordMonth, calendar_data=calendar_data)




@app.route('/tasksAndEvents/<int:year>/<int:month>/<int:day>', methods=['GET', 'POST'])
def display_events(year, month, day):
    selectedDate = f"{year}-{month:02d}-{day:02d}"

    #Adjust date 
    if request.method == 'POST':
        direction = request.form['direction']

        if direction == 'prev':
            # Decrease day
            day -= 1
            # If day becomes 0, set to last day of previous month
            if day == 0:
                month -= 1
                 # If month becomes 0, set to previous year December
                if month == 0:
                    month = 12
                    year -= 1
                #set correct last day
                day = 31 if month in {1,3,5,7,8,10,12} else 30 if month in {4,6,9,11} else 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 ==0) else 28
        elif direction == 'next':
            # Increase day
            day += 1
            #Find last day of the month
            last_day = 31 if month in {1,3,5,7,8,10,12} else 30 if month in {4,6,9,11} else 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 ==0) else 28
            if day > last_day:
                # Move month forward and adjust day if it is larger than last day
                day = 1
                month += 1
                if month > 12:
                    # Move year forward and adjust month if it is larger than Decmber
                    month = 1
                    year += 1

        #update the url for this route passing the new year and month
        return redirect(url_for('display_events', year=year, month=month, day=day))

    dateEvents = [event for event in eventList if event[2] ==selectedDate]

    # Get word Month from dictionary using value. Use "Invalid Month" if number value is invalid
    wordMonth = set_month.get(month,'Invalid Month')

    return render_template('tasksAndEvents.html', eventList = dateEvents, year=year, month=month, wordMonth = wordMonth, day = day)


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

@app.route('/upcoming_events')
def upcoming_events():
    # Calculate the start and end dates of the current week
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # Filter events and tasks within the current week
    upcoming_events = []

    for event in eventList:
        event_id, event_name, event_date_string, isTask, completed = event

        event_date = datetime.strptime(event_date_string, "%Y-%m-%d").date() if event_date_string else None

        # Check if event_date is not None before making the comparison
        if event_date and start_of_week <= event_date <= end_of_week:
            # Calculate the number of days left for each event/task from today
            days_left = (event_date - today).days
            upcoming_events.append((event_name, event_date, days_left))

    return render_template('upcoming_events.html', upcoming_events=upcoming_events, start_of_week=start_of_week, end_of_week=end_of_week)

    

#Add the option to run this file directly
if __name__=='__main__':
    app.run(debug=True)
