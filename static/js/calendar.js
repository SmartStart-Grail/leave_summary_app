

  document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var url = `/calendarfunction/`
    var calendar = new FullCalendar.Calendar(calendarEl, {
      eventClick: function(info) {
        
        calendarEventFunction(info)
      },
 
      height: '100%',
      eventMinWidth :5,
      expandRows: false,
      // slotMinTime: '08:00',
      // slotMaxTime: '20:00',
      headerToolbar: {
        left: 'prev,next',
        center: 'title',
        right: ''
      },
      
      initialView: 'dayGridMonth',
      // initialDate: '2024-01-01',
      initialDate: new Date(),
      navLinks: false, // can click day/week names to navigate views
      // editable: true,
      selectable: true,
      selectHelper:true,
      eventLimit:false,
      weekends:true,
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
          dayMaxEventRows: 4// adjust to 6 only for timeGridWeek/timeGridDay
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
  var date = $('#fc-dom-1').html()
  if (date){
    date=date
  }
  else{

    date = $('#selected_date_hidden').val()
  }

  let departmentSelected = $('#department-select').val();
  let locationSelected = $('#location-select').val();
  let supervisorSelected = $('#supervisor-select').val();
  let titleSelect = $('#title-select').val();

  let csrfmiddlewaretoken = $("input[name = 'csrfmiddlewaretoken']").prop('value')
  var project_name = $('#new-project-name').val()
  let formData = new FormData();
  formData.append('date',date)
  formData.append('emp_select',emp_select)
  formData.append('departmentSelected',departmentSelected)
  formData.append('locationSelected',locationSelected)
  formData.append('supervisorSelected',supervisorSelected)
  formData.append('titleSelect',titleSelect)
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

    $('#calendar-container-parents').html(response)

    var start_date = $('#start_date_hidden').val()
    var emp_select = $('#selected_employee_hidden').val()
    var calendarEl = document.getElementById('calendar');
    $('#exampleModal').modal('hide');
    $('#ap').html('Apply Filter')
    $('#cf').html('Clear Filter')
    var url = `/updatecalendarjs/${date}/${emp_select}/`
    var calendar = new FullCalendar.Calendar(calendarEl, {
        eventClick: function(info) {
          calendarEventFunction(info)
        },

      
      height: '100%',
      eventMinWidth :5,
      expandRows: false,
      // slotMinTime: '08:00',
      // slotMaxTime: '20:00',
      headerToolbar: {
        left: 'prev,next',
        center: 'title',
        right: ''
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
          dayMaxEventRows: 4// adjust to 6 only for timeGridWeek/timeGridDay
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

// $('#filter-id').on('change','#supervisor-select',(e)=>{
//   var id = e.target.id
//   var super_value = $("#supervisor-select").val();
//   var emp_value = $('#emp-select').val();
//   var dept_value = $('#department-select').val();
//   var location_value = $('#location-select').val();
//   var title_select = $('#title-select').val();
//   var project_value = $('#project-select').val();


//   if (($('.employee-class .filter-option-inner-inner').html() == undefined)||($('.employee-class .filter-option-inner-inner').html() == 'selected value')){

//    var emp_value = false
//   }
//   // if (emp_value.length ==0){
//   //   emp_value = false
//   // }

//   if (($('.project-class .filter-option-inner-inner').html() == undefined)||($('.project-class .filter-option-inner-inner').html() == 'selected value')){
//    var project_value  = false
//   }

//   if (($('.title-class .filter-option-inner-inner').html() == undefined)||($('.title-class .filter-option-inner-inner').html() == 'selected value')){
//    var title_select = false
//   }

//   if (($('.department-class .filter-option-inner-inner').html() == undefined)||($('.department-class .filter-option-inner-inner').html() == 'selected value')){
//    var dept_value = false
//   }

//   if (($('.location-class .filter-option-inner-inner').html() == undefined)||($('.location-class .filter-option-inner-inner').html() == 'selected value')){
//    var location_value = false
//   }
  

//   $.ajax({
//             url:'/supervisorselect/',
//             data:{'super_value':super_value,'emp_value':emp_value,'project_value':project_value,'title_select':title_select,
//               'dept_value':dept_value,'location_value':location_value
//           },
//             success:(response)=>{
//               // console.log(response)
//               $('#filter-id').html(response)
//               $('.selectpicker').selectpicker()

//               if (($('.title-class .filter-option-inner-inner').html() == undefined)||(title_select == false )){
//                 $('.title-class .filter-option-inner-inner').html('selected value');
//                   $('.title-class .filter-option-inner-inner').addClass('change-color');
//               }
            
            
//               if (($('.project-class .filter-option-inner-inner').html() == undefined)||(project_value == false)){
//                 $('.project-class .filter-option-inner-inner').html('selected value');
//                   $('.project-class .filter-option-inner-inner').addClass('change-color');
//               }

//               if (($('.department-class .filter-option-inner-inner').html() == undefined)||(dept_value == false)){
//                 $('.department-class .filter-option-inner-inner').html('selected value');
//                   $('.department-class .filter-option-inner-inner').addClass('change-color');
//               }

//               if (($('.location-class .filter-option-inner-inner').html() == undefined)||(location_value == false)){
//                 $('.location-class .filter-option-inner-inner').html('selected value');
//                   $('.location-class .filter-option-inner-inner').addClass('change-color');
//               }
//               $('.employee-class .filter-option-inner-inner').html('selected value');
//               $('.employee-class .filter-option-inner-inner').addClass('change-color');
//               $('#supervisor-select option:selected').prependTo('#supervisor-select');
//               // $('#id_users option:selected').prependTo('#id_users')
              
//               $( "#supervisor-select" ).sortable();
//               var selectedOptions = $("#supervisor-select").find('option:selected');
//               selectedOptions.detach();
//               $("#supervisor-select").prepend(selectedOptions);
//               $("#supervisor-select").selectpicker('refresh');
             
//             }
//           })
// })




// $('#filter-id').on('change','#title-select',(e)=>{
//   var id = e.target.id
//   // var super_value = $(`#${id}`).val();
//   var title_select = $('#title-select').val();
//   var emp_value = $('#emp-select').val();
//   var super_value = $("#supervisor-select").val();
//   var dept_value = $('#department-select').val();
//   var location_value = $('#location-select').val();
//   var project_value = $('#project-select').val();

//   // if (emp_value.length ==0){
//   //   emp_value = false
//   // }
//   // console.log(emp_value)

//   if (($('.employee-class .filter-option-inner-inner').html() == undefined)||($('.employee-class .filter-option-inner-inner').html() == 'selected value')){

//     var emp_value = false
//   }
//   if (($('.supervisor-class .filter-option-inner-inner').html() == undefined)||($('.supervisor-class .filter-option-inner-inner').html() == 'selected value')){

//     var super_value = false
//   }


//   if (($('.project-class .filter-option-inner-inner').html() == undefined)||($('.project-class .filter-option-inner-inner').html() == 'selected value')){

//     var project_value = false
//   }

//   if (($('.department-class .filter-option-inner-inner').html() == undefined)||($('.department-class .filter-option-inner-inner').html() == 'selected value')){

//     var dept_value  = false
//   }
//   if (($('.location-class .filter-option-inner-inner').html() == undefined)||($('.location-class .filter-option-inner-inner').html() == 'selected value')){
//     var location_value = false
//   }

//   $.ajax({
//             url:'/titleselect/',
//             data:{'title-select':title_select,'super_value':super_value,'project_value':project_value,'emp_value':emp_value,'dept_value':dept_value,
//                   'location_value':location_value},
//             success:(response)=>{
//               $('#filter-id').html(response)
              
              
//               $('.selectpicker').selectpicker()

//               if (($('.supervisor-class .filter-option-inner-inner').html() == undefined)||(super_value == false )){
//                 $('.supervisor-class .filter-option-inner-inner').html('selected value');
//                   $('.supervisor-class .filter-option-inner-inner').addClass('change-color');
//               }
            
            
//               if (($('.project-class .filter-option-inner-inner').html() == undefined)||(project_value == false)){
//                 $('.project-class .filter-option-inner-inner').html('selected value');
//                   $('.project-class .filter-option-inner-inner').addClass('change-color');
//               }

//               if (($('.department-class .filter-option-inner-inner').html() == undefined)||(dept_value == false)){
//                 $('.department-class .filter-option-inner-inner').html('selected value');
//                   $('.department-class .filter-option-inner-inner').addClass('change-color');
//               }

//               if (($('.location-class .filter-option-inner-inner').html() == undefined)||(location_value == false)){
//                 $('.location-class .filter-option-inner-inner').html('selected value');
//                   $('.location-class .filter-option-inner-inner').addClass('change-color');
//               }
              

              
//               // $('.department-class .filter-option-inner-inner').html('selected value');
//               // $('.department-class .filter-option-inner-inner').addClass('change-color');
//               $('.employee-class .filter-option-inner-inner').html('selected value');
//               $('.employee-class .filter-option-inner-inner').addClass('change-color');

//               var selectedOptions = $("#title-select").find('option:selected');
//               selectedOptions.detach();
//               $("#title-select").prepend(selectedOptions);
//               $("#title-select").selectpicker('refresh');
              
              

//             }
//           })
// })


// $('#filter-id').on('change','#project-select',(e)=>{

//   var id = e.target.id
//   // var super_value = $(`#${id}`).val();
//   var project_select = $('#project-select').val();
//   var title_select = $('#title-select').val();
//   var emp_value = $('#emp-select').val();
//   var super_value = $("#supervisor-select").val();
//   var dept_value = $('#department-select').val();
//   var location_value = $('#location-select').val();

//   // if (emp_value.length ==0){
//   //   emp_value = false
//   // }

//   if (($('.employee-class .filter-option-inner-inner').html() == undefined)||($('.employee-class .filter-option-inner-inner').html() == 'selected value')){

//     var emp_value = false
//   }

 
 
//   if (($('.supervisor-class .filter-option-inner-inner').html() == undefined)||($('.supervisor-class .filter-option-inner-inner').html() == 'selected value')){

//     var super_value = false
//   }

//   if (($('.title-class .filter-option-inner-inner').html() == undefined)||($('.title-class .filter-option-inner-inner').html() == 'selected value')){
//     var title_select = false
//   }

//   if (($('.department-class .filter-option-inner-inner').html() == undefined)||($('.department-class .filter-option-inner-inner').html() == 'selected value')){

//     var dept_value  = false
//   }

//   if (($('.location-class .filter-option-inner-inner').html() == undefined)||($('.location-class .filter-option-inner-inner').html() == 'selected value')){
//     var location_value = false
//   }





  

//   $.ajax({
//             url:'/projectselect/',
//             data:{'project-select':project_select,'super_value':super_value,'title_select':title_select,'emp_value':emp_value,
//                     'dept_value':dept_value,'location_value':location_value},
//             success:(response)=>{
//               // console.log(response)
//               $('#filter-id').html(response)
              
              
//               $('.selectpicker').selectpicker()
             
              

//               if(($('.supervisor-class .filter-option-inner-inner').html() == undefined)||(super_value == false)){
//                   $('.supervisor-class .filter-option-inner-inner').html('selected value');
//                   $('.supervisor-class .filter-option-inner-inner').addClass('change-color');
//               }
//               if(($('.title-class .filter-option-inner-inner').html() == undefined)||(title_select == false)){
//                   $('.title-class .filter-option-inner-inner').html('selected value');
//                   $('.title-class .filter-option-inner-inner').addClass('change-color');
//               }
//               if (($('.department-class .filter-option-inner-inner').html() == undefined)||(dept_value == false)){
//                 $('.department-class .filter-option-inner-inner').html('selected value');
//                   $('.department-class .filter-option-inner-inner').addClass('change-color');
//               }
//               if (($('.location-class .filter-option-inner-inner').html() == undefined)||(location_value == false)){
//                 $('.location-class .filter-option-inner-inner').html('selected value');
//                   $('.location-class .filter-option-inner-inner').addClass('change-color');
//               }
//               $('.employee-class .filter-option-inner-inner').html('selected value');
//               $('.employee-class .filter-option-inner-inner').addClass('change-color');

//               var selectedOptions = $("#project-select").find('option:selected');
//               selectedOptions.detach();
//               $("#project-select").prepend(selectedOptions);
//               $("#project-select").selectpicker('refresh');

//             }
//           })
// })



// $('#filter-id').on('change','#emp-select',(e)=>{
//   var id = e.target.id
//   // var super_value = $(`#${id}`).val();
//   var emp_value = $('#emp-select').val();
//   var super_value = $("#supervisor-select").val();
//   var dept_value = $('#department-select').val();
//   var location_value = $('#location-select').val();
//   var title_value = $('#title-select').val();
//   var project_value = $('#project-select').val();


//   if (($('.supervisor-class .filter-option-inner-inner').html() == undefined)||($('.supervisor-class .filter-option-inner-inner').html() == 'selected value')){
//     var super_value = false
//   }

//   if (($('.title-class .filter-option-inner-inner').html() == undefined)||($('.title-class .filter-option-inner-inner').html() == 'selected value')){

//    var  title_select = false
//   }

//   if (($('.project-class .filter-option-inner-inner').html() == undefined)||($('.project-class .filter-option-inner-inner').html() == 'selected value')){
//     var project_value = false
//   }

//   if (($('.department-class .filter-option-inner-inner').html() == undefined)||($('.department-class .filter-option-inner-inner').html() == 'selected value')){

//    var dept_value  = false
//   }
//   if (($('.location-class .filter-option-inner-inner').html() == undefined)||($('.location-class .filter-option-inner-inner').html() == 'selected value')){
//    var location_value = false
//   }

//   $.ajax({
//             url:'/employeeselect/',
//             data:{'emp-select':emp_value,'super_value':super_value,'project_value':project_value,'title_select':title_select,'dept_value':dept_value,'location_value':location_value},
//             success:(response)=>{
//               // console.log(response)
//               $('#filter-id').html(response)
              
              
//               $('.selectpicker').selectpicker()
//               // $('.supervisor-class .filter-option-inner-inner').addClass('filter-ass');
//               if(($('.supervisor-class .filter-option-inner-inner').html() == undefined)||(super_value == false)){
//                 $('.supervisor-class .filter-option-inner-inner').html('selected value');
//                 $('.supervisor-class .filter-option-inner-inner').addClass('change-color');
//             }
//             if(($('.title-class .filter-option-inner-inner').html() == undefined)||(title_select == false)){
//                 $('.title-class .filter-option-inner-inner').html('selected value');
//                 $('.title-class .filter-option-inner-inner').addClass('change-color');
//             }

//             if (($('.project-class .filter-option-inner-inner').html() == undefined)||(project_value == false)){
//               $('.project-class .filter-option-inner-inner').html('selected value');
//                 $('.project-class .filter-option-inner-inner').addClass('change-color');
//             }

//             if (($('.department-class .filter-option-inner-inner').html() == undefined)||(dept_value == false)){
//               $('.department-class .filter-option-inner-inner').html('selected value');
//                 $('.department-class .filter-option-inner-inner').addClass('change-color');
//             }
//             if (($('.location-class .filter-option-inner-inner').html() == undefined)||(location_value == false)){
//               $('.location-class .filter-option-inner-inner').html('selected value');
//                 $('.location-class .filter-option-inner-inner').addClass('change-color');
//             }
//             // $( "#emp-select" ).sortable();
//             var selectedOptions = $("#emp-select").find('option:selected');
//               selectedOptions.detach();
//               $("#emp-select").prepend(selectedOptions);
//               $("#emp-select").selectpicker('refresh');


//               // $('.title-class .filter-option-inner-inner').html('selected value');
//               // $('.title-class .filter-option-inner-inner').addClass('change-color');
//               // $('.project-class .filter-option-inner-inner').html('selected value');
//               // $('.project-class .filter-option-inner-inner').addClass('change-color');

//             }
//           })
// })



// $('#filter-id').on('change','#department-select',(e)=>{

//   var id = e.target.id
//   // var super_value = $(`#${id}`).val();
//   var emp_value = $('#emp-select').val();
//   var super_value = $("#supervisor-select").val();
//   var dept_value = $('#department-select').val();
//   var location_value = $('#location-select').val();
//   var title_select = $('#title-select').val();
//   var project_value = $('#project-select').val();


//   if (($('.supervisor-class .filter-option-inner-inner').html() == undefined)||($('.supervisor-class .filter-option-inner-inner').html() == 'selected value')){
//    var super_value = false
//   }

//   if (($('.title-class .filter-option-inner-inner').html() == undefined)||($('.title-class .filter-option-inner-inner').html() == 'selected value')){

//   var  title_select = false
//   }

//   if (($('.project-class .filter-option-inner-inner').html() == undefined)||($('.project-class .filter-option-inner-inner').html() == 'selected value')){
//     var  project_value = false
//   }



//   if (($('.location-class .filter-option-inner-inner').html() == undefined)||($('.location-class .filter-option-inner-inner').html() == 'selected value')){
//   var  location_value = false
//   }
  


//   $.ajax({
//             url:'/departmentselect/',
//             data:{'dept_value':dept_value,'super_value':super_value,'project_value':project_value,'title_select':title_select,
//               'dept_value':dept_value,'location_value':location_value},
//             success:(response)=>{
//               // console.log(response)
//               $('#filter-id').html(response)
              
              
//               $('.selectpicker').selectpicker()
//               // $('.supervisor-class .filter-option-inner-inner').addClass('filter-ass');
//               if(($('.supervisor-class .filter-option-inner-inner').html() == undefined)||(super_value == false)){
//                 $('.supervisor-class .filter-option-inner-inner').html('selected value');
//                 $('.supervisor-class .filter-option-inner-inner').addClass('change-color');
//             }
//             if(($('.title-class .filter-option-inner-inner').html() == undefined)||(title_select == false)){
//                 $('.title-class .filter-option-inner-inner').html('selected value');
//                 $('.title-class .filter-option-inner-inner').addClass('change-color');
//             }

//             if (($('.project-class .filter-option-inner-inner').html() == undefined)||(project_value == false)){
//               $('.project-class .filter-option-inner-inner').html('selected value');
//                 $('.project-class .filter-option-inner-inner').addClass('change-color');
//             }
//             if (($('.department-class .filter-option-inner-inner').html() == undefined)||(dept_value == false)){
//               $('.department-class .filter-option-inner-inner').html('selected value');
//                 $('.department-class .filter-option-inner-inner').addClass('change-color');
//             }

//             if (($('.location-class .filter-option-inner-inner').html() == undefined)||(location_value == false)){
//               $('.location-class .filter-option-inner-inner').html('selected value');
//                 $('.location-class .filter-option-inner-inner').addClass('change-color');
//             }

//             $('.employee-class .filter-option-inner-inner').html('selected value');
//             $('.employee-class .filter-option-inner-inner').addClass('change-color');


//             var selectedOptions = $("#department-select").find('option:selected');
//               selectedOptions.detach();
//               $("#department-select").prepend(selectedOptions);
//               $("#department-select").selectpicker('refresh');

//               // $('.department-class .filter-option-inner-inner').html('selected value');
//               // $('.department-class .filter-option-inner-inner').addClass('change-color');
              
//               // $('.title-class .filter-option-inner-inner').html('selected value');
//               // $('.title-class .filter-option-inner-inner').addClass('change-color');
//               // $('.project-class .filter-option-inner-inner').html('selected value');
//               // $('.project-class .filter-option-inner-inner').addClass('change-color');

//             }
//           })
// })



// $('#filter-id').on('change','#location-select',(e)=>{

//   var id = e.target.id
//   // var super_value = $(`#${id}`).val();
//   var emp_value = $('#emp-select').val();
//   var super_value = $("#supervisor-select").val();
//   var dept_value = $('#department-select').val();
//   var location_value = $('#location-select').val();
//   var title_value = $('#title-select').val();
//   var project_value = $('#project-select').val();


//   if (($('.supervisor-class .filter-option-inner-inner').html() == undefined)||($('.supervisor-class .filter-option-inner-inner').html() == 'selected value')){
//    var super_value = false
//   }

//   if (($('.title-class .filter-option-inner-inner').html() == undefined)||($('.title-class .filter-option-inner-inner').html() == 'selected value')){

//    var title_select = false
//   }

//   if (($('.project-class .filter-option-inner-inner').html() == undefined)||($('.project-class .filter-option-inner-inner').html() == 'selected value')){
//    var project_value = false
//   }

//   if (($('.department-class .filter-option-inner-inner').html() == undefined)||($('.department-class .filter-option-inner-inner').html() == 'selected value')){

//    var dept_value  = false
//   }

//   if (($('.employee-class .filter-option-inner-inner').html() == undefined)||($('.employee-class .filter-option-inner-inner').html() == 'selected value')){

//    var emp_value = false
//   }

  


//   $.ajax({
//             url:'/locationselect/',
//             data:{'dept_value':dept_value,'super_value':super_value,'project_value':project_value,'title_select':title_select,
//                     'location_value':location_value,'emp_value':emp_value},
//             success:(response)=>{
//               // console.log(response)
//               $('#filter-id').html(response)
              
              
//               $('.selectpicker').selectpicker()
//               // $('.supervisor-class .filter-option-inner-inner').addClass('filter-ass');
//               if(($('.supervisor-class .filter-option-inner-inner').html() == undefined)||(super_value == false)){
//                 $('.supervisor-class .filter-option-inner-inner').html('selected value');
//                 $('.supervisor-class .filter-option-inner-inner').addClass('change-color');
//             }
//             if(($('.title-class .filter-option-inner-inner').html() == undefined)||(title_select == false)){
//                 $('.title-class .filter-option-inner-inner').html('selected value');
//                 $('.title-class .filter-option-inner-inner').addClass('change-color');
//             }

//             if (($('.project-class .filter-option-inner-inner').html() == undefined)||(project_value == false)){
//               $('.project-class .filter-option-inner-inner').html('selected value');
//                 $('.project-class .filter-option-inner-inner').addClass('change-color');
//             }
//             if (($('.department-class .filter-option-inner-inner').html() == undefined)||(dept_value == false)){
//               $('.department-class .filter-option-inner-inner').html('selected value');
//                 $('.department-class .filter-option-inner-inner').addClass('change-color');
//             }

//             $('.employee-class .filter-option-inner-inner').html('selected value');
//             $('.employee-class .filter-option-inner-inner').addClass('change-color');

//             var selectedOptions = $("#location-select").find('option:selected');
//               selectedOptions.detach();
//               $("#location-select").prepend(selectedOptions);
//               $("#location-select").selectpicker('refresh');

//               // $('.department-class .filter-option-inner-inner').html('selected value');
//               // $('.department-class .filter-option-inner-inner').addClass('change-color');
//               // $('.location-class .filter-option-inner-inner').html('selected value');
//               // $('.location-class .filter-option-inner-inner').addClass('change-color');
//               // $('.title-class .filter-option-inner-inner').html('selected value');
//               // $('.title-class .filter-option-inner-inner').addClass('change-color');
//               // $('.project-class .filter-option-inner-inner').html('selected value');
//               // $('.project-class .filter-option-inner-inner').addClass('change-color');

//             }
//           })
// })


$('#cf').on('click',(e)=>{
  // e.preventDefault()
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

$('#filter-id').on('change','.selectpicker',(e)=>{
  $('.btn-filt').attr('disabled',false);
})

$('#cf').on('click',(e)=>{
  $('.btn-filt').attr('disabled', true);

})


// $(document).ready(()=>{
// $('.selectpicker').multiselect({
//   beforeopen: function(event, ui) {
//       $('.selectpicker option:selected').prependTo('.selectpicker');
//       $('.selectpicker').multiselect('refresh');
//   }
// });

// })






$('.fc-h-event').on('click',(e)=>{

})



var emp_data
var date
// Outlook Functionality
let calendarEventFunction = (info)=>{

  if (info.event.id !=1){
  const myModal = document.getElementById('myModal')
  $('#myModal').modal('show');
  emp_data = info.event.title
  date = info.event.id
  var queryParams = 'emp_data=' + encodeURIComponent(emp_data) + '&date=' + encodeURIComponent(date);
  $('#downl').attr('href','/outlookcalendar/?' + queryParams)
  // $('#myModal').modal('hide');
  // $('#downl').removeAttr('href')

  }

  // $.ajax({
  //   url:'/outlookcalendar/',
  //   data:{'emp_data':info.event.title,'date':info.event.id},
  //   success:(response)=>{
  //     alert('File Successfully Downloaded in your download foler.')

  //   }
  // })
}

$('#download-files').on('click',(e)=>{
  // $.ajax({
  //   url:'/outlookcalendar/',
  //   data:{'emp_data':emp_data,'date':date},
  //   success:(response)=>{
  //     alert('File Successfully Downloaded in your download foler.')
  //     location.reload()

  //   }
  // })
  // data = {'emp_data':emp_data,'date':date}

  var queryParams = 'emp_data=' + encodeURIComponent(emp_data) + '&date=' + encodeURIComponent(date);

  var xhr = new XMLHttpRequest();
  xhr.open('GET', '/outlookcalendar/?' + queryParams, true);  // Append the query string to the URL
  xhr.responseType = 'blob'; 

    xhr.onload = function() {
      if (xhr.status === 200) {
        var blob = xhr.response;
        console.log(blob)
        var link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'event.ics';  // Set the file name for download
        link.click();
      } else {
        alert('Failed to download the file.');
      }
    };

    xhr.send();

})
