let hour, min;
startTime = $('input[name=start-time]');
endTime = $('input[name=end-time]');
timeInterval = $('input[name=time-interval]')
// init the form when the document is ready or when the form is populated after an ajax call

//console.log($('#new-template').html());
//console.log($('#content-wrapper').html());

initUI = () =>{

    console.log("Init UI");
    [startHour, startMin] = startTime.val().split(":").map(Number);
    [endHour, endMin] = endTime.val().split(":").map(Number);
    interval = parseInt(timeInterval.val());
    startTimeInMin = startHour*60 + startMin;
    endTimeInMin= endHour*60 + endMin;

    row = 0;
    for (let index = startTimeInMin; index < endTimeInMin; index+=interval) {
       
        nextIndex = index+interval;
        console.log(index/60 >> 0, index%60);
        $('#editView').append(`<tr id='calendar-row-${row}'></tr>`);


        $(`#calendar-row-${row}`).append(
            `<td>${index/60 >> 0}:${index%60 == 0 ? "00" : index%60}-
            ${(nextIndex/60) >> 0}:${nextIndex%60 == 0 ? "00" : nextIndex%60}</td>`
        )
        for (let index = 0; index < 6; index++) {

            $(`#calendar-row-${row}`).append(
                `
            <td>
                <select style="width: 100%; name="cell-${row}-${index}">
                    <option value="0" selected> ------------ </option>
                    <option value="1" color="blue">Blue</option>
                    <option value="2" color="red">Red</option>
                    <option value="3" color="yellow">Yellow</option>
                    <option value="4" color="green">Green</option>
                    <option value="5" color="grey">Grey</option>
                    <option value="6" color="purple">Purple</option>
                    <option value="7" color="tomato">Breakfast</option>
                    <option value="8" color="tomato">Snack</option>
                    <option value="9" color="tomato">Lunch</option>
                    <option value="10" color="tomato">Dinner</option>
                    <option value="11" color="fuchsia">Club and socities</option>
                    <option value="12" color="sandybrown">Research</option>
                </select>
            </td>
                `
            )
        }
        row++;
    }

    $("select").change((event) => {
        selected = $(event.target);
        
        selected.parent().css( "background-color", selected.find(":selected").attr('color') );
    }
    )

}

$("input[name=time-interval], input[name=start-time], input[name=end-time]").change((event) =>{

    $('#editView').empty();
    initUI();

})
initUI();
