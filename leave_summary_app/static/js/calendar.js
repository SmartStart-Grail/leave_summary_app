

  document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var url = `/calendarfunction/`
    var calendar = new FullCalendar.Calendar(calendarEl, {

      
      height: '100%',
      eventMinWidth :5,
      expandRows: false,
      // slotMinTime: '08:00',
      // slotMaxTime: '20:00',
      headerToolbar: {
        left: 'prev,next',
        center: 'title',
        right: 'dayGridMonth'
      },
      
      initialView: 'dayGridMonth',
      // initialDate: '2024-01-01',
      initialDate: new Date(),
      navLinks: false, // can click day/week names to navigate views
      // editable: true,
      selectable: true,
      selectHelper:true,
      eventLimit:false,
      weekends:false,
      // eventMinWidth :60,
      // contentHeight:"auto",
      handleWindowResize:true,
      nowIndicator: true,
      dayMaxEvents: false, // allow "more" link when too many events
      eventLimit: true,
    
      themeSystem: 'bootstrap5',
      
      showNonCurrentDates:false, //Show the next month calendar date...
      views: {
        dayGrid: {
          dayMaxEventRows: 2// adjust to 6 only for timeGridWeek/timeGridDay
        }
      },
      events:url,
      
    });

    calendar.render();
  });

  $(".fc-day-disabled").hide()

  $('.fc-day-disabled').html('hello');



  // $(document).ready(()=>{
  //   $(".fc-day-disabled").hide();
  // })


$(".btn-filter").on('click',(e)=>{
  $(".btn-filter").css("background-color", "gray");

})

// $(window).on('click',(e)=>{
//   $(".btn-filter").css("background-color", "white");

// })

$('.selectpicker').selectpicker();


// $('#emp-select').on('change',(e)=>{
//   console.log($('#emp-select').val())
//   console.log($('#fc-dom-1').html())
//   console.log('helmljmkm')

//   var emp_select = $('#emp-select').val();

// })

$('#filter-form').on('submit',(e)=>{
  e.preventDefault();
  var emp_select = $('#emp-select').val();
  console.log(emp_select)
  console.log('checked...')
  var date = $('#fc-dom-1').html()
  console.log(date)
  if (date){
    console.log('hello')
    date=date
  }
  else{

    date = $('#selected_date_hidden').val()
  }
  console.log(date)
  let csrfmiddlewaretoken = $("input[name = 'csrfmiddlewaretoken']").prop('value')
  var project_name = $('#new-project-name').val()
  let formData = new FormData();
  formData.append('date',date)
  formData.append('emp_select',emp_select)
  formData.append('csrfmiddlewaretoken',csrfmiddlewaretoken)
  var spinner = '<div class ="spinner-border spinner-border-sm text-warning" role = "status"><span class = "visually-hidden">Loading..</span></div>'
  $('.btn-filt').html(spinner)
  $.ajax({
    url:"/updatecalendar/",
    type:'POST',
    data : formData,
    caches:false,
    contentType:false,
    processData:false,
    success:(response)=>{

      // console.log({{ text|json_script }})
      //  var h = "{{text}}"
       
       
    // JSON.parse('{{ response.event |escapejs }}')
    // console.log(JSON.parse("event_data|escapejs"))
    $('#calendar-container-parents').html(response)
    console.log($('#start_date_hidden').val())
    var start_date = $('#start_date_hidden').val()
    var calendarEl = document.getElementById('calendar');
    $('#exampleModal').modal('hide');
    $('#ap').html('Apply Filter')
    $('#cf').html('Clear Filter')
    var url = `/updatecalendarjs/${date}/${emp_select}/`
    console.log(`/updatecalendarjs/${date}/${emp_select}/`)
    console.log(response.date)
    var calendar = new FullCalendar.Calendar(calendarEl, {

      
      height: '100%',
      eventMinWidth :5,
      expandRows: false,
      // slotMinTime: '08:00',
      // slotMaxTime: '20:00',
      headerToolbar: {
        left: 'prev,next',
        center: 'title',
        right: 'dayGridMonth'
      },
      
      initialView: 'dayGridMonth',
      initialDate: start_date,
      navLinks: false, // can click day/week names to navigate views
      // editable: true,
      selectable: true,
      selectHelper:true,
      eventLimit:false,
      weekends:false,
      // eventMinWidth :60,
      // contentHeight:"auto",
      handleWindowResize:true,
      nowIndicator: true,
      dayMaxEvents: false, // allow "more" link when too many events
      eventLimit: true,
    
      themeSystem: 'bootstrap5',
      
      showNonCurrentDates:false, //Show the next month calendar date...
      views: {
        dayGrid: {
          dayMaxEventRows: 2// adjust to 6 only for timeGridWeek/timeGridDay
        }
      },
      events:url,
      
    });

    calendar.render();
            
    }
})
})

// $('#apply-filter').on('click',()=>{
//   $('#filter-form').on('submit',(e)=>{
//     e.preventDefault();
//     console.log('hello')
//   })
// })

$('#filter-id').on('change','#supervisor-select',(e)=>{
  console.log(e.target.id);
  var id = e.target.id
  var super_value = $("#supervisor-select").val();
  var emp_value = $('#emp-select').val();
  var dept_value = $('#department-select').val();
  var location_value = $('#location-select').val();
  var title_select = $('#title-select').val();
  var project_value = $('#project-select').val();


  console.log(super_value)
  if (emp_value.length ==0){
    emp_value = false
  }

  if (($('.project-class .filter-option-inner-inner').html() == undefined)||($('.project-class .filter-option-inner-inner').html() == 'selected value')){
    console.log('isniindin')

    project_value  = false
  }

  if (($('.title-class .filter-option-inner-inner').html() == undefined)||($('.title-class .filter-option-inner-inner').html() == 'selected value')){
    console.log('jnknknk')
    title_select = false
  }

  console.log(title_select)
  

  $.ajax({
            url:'/supervisorselect/',
            data:{'super_value':super_value,'emp_value':emp_value,'project_value':project_value,'title_select':title_select},
            success:(response)=>{
              // console.log(response)
              $('#filter-id').html(response)
              $('.selectpicker').selectpicker()

              if (($('.title-class .filter-option-inner-inner').html() == undefined)||(title_select == false )){
                $('.title-class .filter-option-inner-inner').html('selected value');
                  $('.title-class .filter-option-inner-inner').addClass('change-color');
              }
            
            
              if (($('.project-class .filter-option-inner-inner').html() == undefined)||(project_value == false)){
                $('.project-class .filter-option-inner-inner').html('selected value');
                  $('.project-class .filter-option-inner-inner').addClass('change-color');
              }

              $('.department-class .filter-option-inner-inner').html('selected value');
              $('.department-class .filter-option-inner-inner').addClass('change-color');
              $('.location-class .filter-option-inner-inner').html('selected value');
              $('.location-class .filter-option-inner-inner').addClass('change-color');
              $('.employee-class .filter-option-inner-inner').html('selected value');
              $('.employee-class .filter-option-inner-inner').addClass('change-color');
            }
          })
})




$('#filter-id').on('change','#title-select',(e)=>{
  console.log(e.target.id);
  var id = e.target.id
  // var super_value = $(`#${id}`).val();
  var title_select = $('#title-select').val();
  var emp_value = $('#emp-select').val();
  var super_value = $("#supervisor-select").val();
  var dept_value = $('#department-select').val();
  var location_value = $('#location-select').val();
  var project_value = $('#project-select').val();
  console.log($('.supervisor-class .filter-option-inner-inner').html())


  if (emp_value.length ==0){
    emp_value = false
  }
  if (($('.supervisor-class .filter-option-inner-inner').html() == undefined)||($('.supervisor-class .filter-option-inner-inner').html() == 'selected value')){
    console.log('isniindin')

    super_value = false
  }


  if (($('.project-class .filter-option-inner-inner').html() == undefined)||($('.project-class .filter-option-inner-inner').html() == 'selected value')){
    console.log('jnknknk')
    project_value = false
  }

  $.ajax({
            url:'/titleselect/',
            data:{'title-select':title_select,'super_value':super_value,'project_value':project_value,'emp_value':emp_value,'text':'heee'},
            success:(response)=>{
              // console.log(response)
              $('#filter-id').html(response)
              
              
              $('.selectpicker').selectpicker()

              if (($('.supervisor-class .filter-option-inner-inner').html() == undefined)||(super_value == false )){
                $('.supervisor-class .filter-option-inner-inner').html('selected value');
                  $('.supervisor-class .filter-option-inner-inner').addClass('change-color');
              }
            
            
              if (($('.project-class .filter-option-inner-inner').html() == undefined)||(project_value == false)){
                $('.project-class .filter-option-inner-inner').html('selected value');
                  $('.project-class .filter-option-inner-inner').addClass('change-color');
              }
              

              
              $('.department-class .filter-option-inner-inner').html('selected value');
              $('.department-class .filter-option-inner-inner').addClass('change-color');
              $('.location-class .filter-option-inner-inner').html('selected value');
              $('.location-class .filter-option-inner-inner').addClass('change-color');
              $('.employee-class .filter-option-inner-inner').html('selected value');
              $('.employee-class .filter-option-inner-inner').addClass('change-color');
              

            }
          })
})


$('#filter-id').on('change','#project-select',(e)=>{
  console.log(e.target.id);
  var id = e.target.id
  // var super_value = $(`#${id}`).val();
  var project_select = $('#project-select').val();
  var title_select = $('#title-select').val();
  var emp_value = $('#emp-select').val();
  var super_value = $("#supervisor-select").val();
  var dept_value = $('#department-select').val();
  var location_value = $('#location-select').val();

  if (emp_value.length ==0){
    emp_value = false
  }

 
 
  if (($('.supervisor-class .filter-option-inner-inner').html() == undefined)||($('.supervisor-class .filter-option-inner-inner').html() == 'selected value')){
    console.log('isniindin')

    super_value = false
  }

  if (($('.title-class .filter-option-inner-inner').html() == undefined)||($('.title-class .filter-option-inner-inner').html() == 'selected value')){
    console.log('jnknknk')
    title_select = false
  }





  

  $.ajax({
            url:'/projectselect/',
            data:{'project-select':project_select,'super_value':super_value,'title_select':title_select,'emp_value':emp_value},
            success:(response)=>{
              // console.log(response)
              $('#filter-id').html(response)
              
              
              $('.selectpicker').selectpicker()
             
              

              if(($('.supervisor-class .filter-option-inner-inner').html() == undefined)||(super_value == false)){
                  $('.supervisor-class .filter-option-inner-inner').html('selected value');
                  $('.supervisor-class .filter-option-inner-inner').addClass('change-color');
              }
                console.log($('.title-class .filter-option-inner-inner').html())
              if(($('.title-class .filter-option-inner-inner').html() == undefined)||(title_select == false)){
                  $('.title-class .filter-option-inner-inner').html('selected value');
                  $('.title-class .filter-option-inner-inner').addClass('change-color');
              }
              $('.department-class .filter-option-inner-inner').html('selected value');
              $('.department-class .filter-option-inner-inner').addClass('change-color');
              $('.location-class .filter-option-inner-inner').html('selected value');
              $('.location-class .filter-option-inner-inner').addClass('change-color');
              $('.employee-class .filter-option-inner-inner').html('selected value');
              $('.employee-class .filter-option-inner-inner').addClass('change-color');

            }
          })
})



$('#filter-id').on('change','#emp-select',(e)=>{
  console.log(e.target.id);
  var id = e.target.id
  // var super_value = $(`#${id}`).val();
  var emp_value = $('#emp-select').val();
  var super_value = $("#supervisor-select").val();
  var dept_value = $('#department-select').val();
  var location_value = $('#location-select').val();
  var title_value = $('#title-select').val();
  var project_value = $('#project-select').val();


  if (($('.supervisor-class .filter-option-inner-inner').html() == undefined)||($('.supervisor-class .filter-option-inner-inner').html() == 'selected value')){
    super_value = false
  }

  if (($('.title-class .filter-option-inner-inner').html() == undefined)||($('.title-class .filter-option-inner-inner').html() == 'selected value')){

    title_select = false
  }

  if (($('.project-class .filter-option-inner-inner').html() == undefined)||($('.project-class .filter-option-inner-inner').html() == 'selected value')){
    project_value = false
  }

  $.ajax({
            url:'/employeeselect/',
            data:{'emp-select':emp_value,'super_value':super_value,'project_value':project_value,'title_select':title_select},
            success:(response)=>{
              // console.log(response)
              $('#filter-id').html(response)
              
              
              $('.selectpicker').selectpicker()
              // $('.supervisor-class .filter-option-inner-inner').addClass('filter-ass');
              if(($('.supervisor-class .filter-option-inner-inner').html() == undefined)||(super_value == false)){
                $('.supervisor-class .filter-option-inner-inner').html('selected value');
                $('.supervisor-class .filter-option-inner-inner').addClass('change-color');
            }
            if(($('.title-class .filter-option-inner-inner').html() == undefined)||(title_select == false)){
                $('.title-class .filter-option-inner-inner').html('selected value');
                $('.title-class .filter-option-inner-inner').addClass('change-color');
            }

            if (($('.project-class .filter-option-inner-inner').html() == undefined)||(project_value == false)){
              $('.project-class .filter-option-inner-inner').html('selected value');
                $('.project-class .filter-option-inner-inner').addClass('change-color');
            }

              $('.department-class .filter-option-inner-inner').html('selected value');
              $('.department-class .filter-option-inner-inner').addClass('change-color');
              $('.location-class .filter-option-inner-inner').html('selected value');
              $('.location-class .filter-option-inner-inner').addClass('change-color');
              // $('.title-class .filter-option-inner-inner').html('selected value');
              // $('.title-class .filter-option-inner-inner').addClass('change-color');
              // $('.project-class .filter-option-inner-inner').html('selected value');
              // $('.project-class .filter-option-inner-inner').addClass('change-color');

            }
          })
})




$('#cf').on('click',(e)=>{
  // e.preventDefault()
  console.log('clicked')
  $.ajax({
    url:'/clearfilter/',
    success:(response)=>{
      $('#filter-id').html(response)
      $('.selectpicker').selectpicker()
      // window.location.reload();
    }
  })
})

$('.btn-close').on('click',(e)=>{
  window.location.reload();

})
