let hour, min;
startTime = $('input[name=start-time]');
endTime = $('input[name=end-time]');
timeInterval = $('input[name=time-interval]');
cycle = $('input[name=cycle]');
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
    cycleVal = parseInt(cycle.val());
    row = 0;

    cells = 0;

    for (let i = 0; i < cycleVal; i++) {
           
        $('#calendars').append(
            `
            <div class="card" style="margin-right: 30px;margin-left: 30px;" >
            <div class="card-body text-center" style="width: 100%;">
                <h4 class="card-title">Week ${i+1}</h4>
                <div class="table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Time</th>
                                <th>Monday</th>
                                <th>Tuesday</th>
                                <th>Wednesday</th>
                                <th>Thursday</th>
                                <th>Friday</th>
                                <th>Saturday</th>
                            </tr>
                        </thead>
                        <tbody id="editView${i}">

                        </tbody>
                    </table>
                
                </div>
            </div>
        </div>
        
            `
        )  
        
        for (let index = startTimeInMin; index < endTimeInMin; index+=interval) {
        
            nextIndex = index+interval;
           
            $(`#editView${i}`).append(`<tr id='calendar-row-${row}'></tr>`);


            $(`#calendar-row-${row}`).append(
                `<td>${index/60 >> 0}:${index%60 == 0 ? "00" : index%60}-
                ${(nextIndex/60) >> 0}:${nextIndex%60 == 0 ? "00" : nextIndex%60}</td>`
            )
            for (let index = 0; index < 6; index++) {
                
                $(`#calendar-row-${row}`).append(
                    `
                <td>
                    <select style="width: 100%;" name="cell${cells}">
                        <option value=0 selected> ------------ </option>
                        <option value=1 color="blue">Blue</option>
                        <option value=2 color="red">Red</option>
                        <option value=3 color="yellow">Yellow</option>
                        <option value=4 color="green">Green</option>
                        <option value=5 color="grey">Grey</option>
                        <option value=6 color="purple">Purple</option>
                        <option value=7 color="tomato">Breakfast</option>
                        <option value=8 color="tomato">Snack</option>
                        <option value=9 color="tomato">Lunch</option>
                        <option value=10 color="tomato">Dinner</option>
                        <option value=11 color="fuchsia">Club and socities</option>
                        <option value=12 color="sandybrown">Research</option>
                    </select>
                </td>
                    `
                )
                cells++;
            }
            row++;
        }

        $('#calendars').append(
            `
            <input name='cells${i}' value=${cells} hidden ></input>
            `
        )
    }



    //Set color events
    $("select").change((event) => {
        selected = $(event.target);
        
        selected.parent().css( "background-color", selected.find(":selected").attr('color') );
    }
    )

}

$("input[name=time-interval], input[name=start-time], input[name=end-time], input[name=cycle]").change((event) =>{

    $('#calendars').empty();
    initUI();

});

initUI();
