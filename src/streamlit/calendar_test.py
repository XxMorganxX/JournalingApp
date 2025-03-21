import streamlit as st
import streamlit.components.v1 as components


press1 = False
st.title("Streamlit Calendar Example")

# Initialize session state for events if it doesn't exist
if 'calendar_events' not in st.session_state:
    st.session_state.calendar_events = []

# Initialize press state if it doesn't exist
if 'press1' not in st.session_state:
    st.session_state.press1 = False

# HTML and JavaScript code for FullCalendar
html_string = """
<html>
  <head>
    <link href='https://cdn.jsdelivr.net/npm/fullcalendar@5.11.3/main.min.css' rel='stylesheet' />
    <script src='https://cdn.jsdelivr.net/npm/fullcalendar@5.11.3/main.min.js'></script>
    <style>
      body { margin: 0; padding: 0; font-family: Arial, sans-serif; }
      #calendar { 
        max-width: 900px; 
        margin: 40px auto;
        height: auto !important;  /* Ensure calendar takes needed height */
      }
      
      /* Custom styling for the calendar */
      .fc {
        height: auto !important;  /* Allow calendar to expand */
      }
      .fc-view {
        overflow: visible !important;  /* Prevent content clipping */
      }
      .fc-theme-standard td, .fc-theme-standard th {
        border: none;
        padding: 3px;
      }
      .fc-daygrid-day {
        background-color: rgba(245, 245, 245, 0.8);
        border-radius: 8px;
        margin: 4px;
        transform: scale(0.95);
      }
      /* Style the day of week headers */
      .fc-col-header-cell {
        color: #8B4513;  /* Saddle brown */
        font-weight: 500;
        text-transform: uppercase;
        font-size: 0.9em;
      }
      /* Style the month/year title */
      .fc-toolbar-title {
        color: #8B4513;  /* Matching saddle brown */
        font-weight: 500;
        text-align: center;
        transform: translateX(13%);  /* Move title slightly to the right */
      }
      .fc-theme-standard .fc-scrollgrid {
        border: none;
      }
      .fc-header-toolbar {
        margin-bottom: 2em !important;
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      .fc-toolbar-chunk {
        flex: 1;
        text-align: center;
      }
    </style>
  </head>
  <body>
    <div id='calendar'></div>
    <script>
      // Make calendar globally accessible
      var calendar;
      
      document.addEventListener('DOMContentLoaded', function() {
        var calendarEl = document.getElementById('calendar');
        calendar = new FullCalendar.Calendar(calendarEl, {
          initialView: 'dayGridMonth',
          headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: ''
          },
          views: {
            dayGridMonth: {
              titleFormat: { month: 'long', year: 'numeric' }
            }
          },
          events: INIT_EVENTS,
          eventClick: function(info) {
            if (info.event.url) {
              window.open(info.event.url, '_blank');
              info.jsEvent.preventDefault(); // prevents current tab from navigating
            }
          }
        });
        calendar.render();
        
        // Add listener for messages from Python
        window.addEventListener('message', function(event) {
            console.log('Received message:', event.data);  // Debug log
            if (event.data.type === 'updateEvents') {
                calendar.removeAllEvents();
                calendar.addEventSource(event.data.events);
                console.log('Updated calendar with events:', event.data.events);  // Debug log
            }
        });
      });
    </script>
  </body>
</html>
"""

def update_calendar_events(events=None):
    """
    Update the calendar with new events.
    
    Args:
        events (list): List of event dictionaries. Each event should have:
            - title (str): Event title
            - start (str): Date in 'YYYY-MM-DD' format
            - url (str): URL to navigate to when clicked
            - backgroundColor (str, optional): Event color in hex format
    """
    if events is None:
        # Default events for testing
        events = [
            {
                'title': 'Meeting',
                'start': '2025-03-20',
                'backgroundColor': '#3788d8',
                'url': 'https://example.com/meeting'
            },
            {
                'title': 'Conference',
                'start': '2025-03-22',
                'backgroundColor': '#4CAF50',
                'url': 'https://example.com/conference'
            }
        ]
    
    st.session_state.calendar_events = events
    st.rerun()

# Inject the current events into the HTML
html_string = html_string.replace('INIT_EVENTS', str(st.session_state.calendar_events))

# Embed the calendar
components.html(html_string, height=600)

custom_event = [
        {
            'title': 'Test #3',
            'start': '2025-03-15',
            'backgroundColor': '#FF5733',
            'url': 'https://example.com/team-meeting'
        },
    ]

# Example button to trigger event updates
if st.button('Update Calendar'):
    
    if not st.session_state.press1:
      print("First Press")
      st.session_state.press1 = True
      custom_events = [
          {
              'title': 'Test #1',
              'start': '2025-03-15',
              'backgroundColor': '#FF5733',
              'url': 'https://example.com/team-meeting'
          },
          {
              'title': 'Test #2',
              'start': '2025-03-25',
              'backgroundColor': '#C70039',
              'url': 'https://example.com/workshop'
          }
      ]
      update_calendar_events(custom_events)
    
    elif st.session_state.press1:
      print("Second Press")
      custom_events = [
          {
              'title': 'Test #1',
              'start': '2025-03-15',
              'backgroundColor': '#FF5733',
              'url': 'https://example.com/team-meeting'
          },
      ]
      update_calendar_events(custom_events)
    
