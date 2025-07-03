console.log('hello')

$('#profile-reset').on('submit',(e)=>{
    e.preventDefault()
    console.log('profile-reset')
    let csrfmiddlewaretoken = $("input[name = 'csrfmiddlewaretoken']").prop('value')
    var old_password = $('#old_password').val()
    var new_password1 = $('#new_password1').val()
    var new_password2 = $('#new_password2').val()

    var spinner = '<div class ="spinner-border spinner-border-sm text-warning" role = "status"><span class = "visually-hidden">Loading..</span></div>'
    let formData = new FormData();
    formData.append('old_password',old_password)
    formData.append('new_password1',new_password1)
    formData.append('new_password2',new_password2)
    formData.append('csrfmiddlewaretoken',csrfmiddlewaretoken)
    $('#btn-password').html(spinner)
    $.ajax({
        url:'/passwordreset/',
        type:'POST',
        data : formData,
        caches:false,
        contentType:false,
        processData:false,
        success:(e)=>{
                console.log(e)
                if (e.message){
                alert(e.success_message)
                window.location.reload();
                }
                else{
                    alert(e.error_message)
                    window.location.reload();
                }
        }

    })
})

$( "#datepicker" ).datepicker({
    dateFormat: 'dd/mm/yy' 
});

$('#holiday-id').on('submit',(e)=>{
    e.preventDefault();

    var date = $('#datepicker').val()
    var holiday_select = $('#holiday-select').val()
    var holiday_name = $('#holiday-name').val()
    let csrfmiddlewaretoken = $("input[name = 'csrfmiddlewaretoken']").prop('value')
    var spinner = '<div class ="spinner-border spinner-border-sm text-warning" role = "status"><span class = "visually-hidden">Loading..</span></div>'
    let formData = new FormData();
    formData.append('date',date)
    formData.append('holiday_select',holiday_select)
    formData.append('holiday_name',holiday_name)
    formData.append('csrfmiddlewaretoken',csrfmiddlewaretoken)
    $('#holiday-btn').html(spinner)
    $.ajax({
        url:'/holidayadd/',
        type:'POST',
        data : formData,
        caches:false,
        contentType:false,
        processData:false,
        success:(e)=>{
                console.log(e)
                if (e.message){
                alert('New holiday added successfully.')
                window.location.reload();
                }
                else{
                    alert(e.error_message)
                    window.location.reload();
                }
        }

    })

})