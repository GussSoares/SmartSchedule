









var cal = new Calendar('#calendar', {
    useCreationPopup: true,
    useDetailPopup: true,
})
cal.on({
    'beforeCreateSchedule': function(e) {
        console.log('beforeCreateSchedule', e);
        // open a creation popup
    },
})

$('#calendar').tuiCalendar({
    defaultView: 'month',
    taskView: true,
    template: {
        monthDayname: function(dayname) {
            return '<span class="calendar-week-dayname-name">' + dayname.label + '</span>';
        }
    }
});
