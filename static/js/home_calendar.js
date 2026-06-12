document.addEventListener('DOMContentLoaded', function() {
    
    var calendarEl = document.getElementById('calendar');
    var calevents = JSON.parse(document.getElementById("events_context_elem").getAttribute("data"));;
    
    var typeColors = {
        'W': '#FFA07A',  
        'T': '#90EE90', 
        'C': '#FFFACD',   
        'P': '#ADD8E6',
        'O': '#CCCCCC' 
    };
    events = []
    for (e of calevents){
        var event = {
            id: e.id,
            title: e.title,
            start: e.start,
            end: e.end,
            backgroundColor: typeColors[e.type],
            textColor: 'black',
            extendedProps: {
                type: e.type,
            },
            editable: false
        }
        events.push(event);
    }

    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'timeGridWeek',
      headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'timeGridWeek,timeGridDay,dayGridMonth,listWeek',
      },
      slotDuration: '02:00:00',
      contentHeight: 'auto',
      nowIndicator: true,
      events: events,eventClick: function(info) {
        var eventStart = new Date(info.event.start);
        var eventStartUTC = new Date(eventStart.getTime() - (eventStart.getTimezoneOffset() * 60000));
        start = eventStartUTC.toISOString().slice(0, 16);
        var eventEnd = new Date(info.event.end);
        var eventEndUTC = new Date(eventEnd.getTime() - (eventEnd.getTimezoneOffset() * 60000));
        end = eventEndUTC.toISOString().slice(0, 16);

        document.getElementById('scheduleEventPopup').style.display = 'block';
        document.getElementById('eventId').value = info.event.id;
        document.getElementById('eventTitle').value = info.event.title;
        document.getElementById('startDateTime').value = start;
        document.getElementById('endDateTime').value = end;
        document.getElementById('eventType').value = info.event.extendedProps.type;
        document.getElementById('deketeEventButton').disabled = false;
      }
    });
  
    calendar.render();

    var scheduleEventButton = document.getElementById('scheduleEventButton');
    scheduleEventButton.addEventListener('click', function() {
        document.getElementById('scheduleEventPopup').style.display = 'block';
        document.getElementById('eventId').value = "";
        document.getElementById('eventTitle').value = "";
        document.getElementById('startDateTime').value = "";
        document.getElementById('endDateTime').value = "";
        document.getElementById('eventType').value = "";
        document.getElementById('deleteEventButton').disabled = true;
    });
    var closeScheduleEventButton = document.getElementById('closeScheduleEventButton');
    closeScheduleEventButton.addEventListener('click', function() {
        document.getElementById('scheduleEventPopup').style.display = 'none';
    });

});