

$('#upload-file-form').on('submit',(e)=>{
    e.preventDefault()
    let file_upload = document.getElementById('file_upload').files[0]
    let csrfmiddlewaretoken = $("input[name = 'csrfmiddlewaretoken']").prop('value')

    var spinner = '<div class ="spinner-border spinner-border-sm text-warning" role = "status"><span class = "visually-hidden">Loading..</span></div>'
    let formData = new FormData();
    formData.append('file_upload',file_upload)
    formData.append('csrfmiddlewaretoken',csrfmiddlewaretoken)
    $('.spinner-btn').html(spinner)
    $.ajax({
        url : '/fileupload/',
        type:'POST',
        data : formData,
        caches:false,
        contentType:false,
        processData:false,
        success:(e)=>{
                alert('File uploaded successfully.')
                window.location.reload();
        }

    })
})




$('.project-radio').on('click',(e)=>{
    var id = e.target.id
    if (id === 'new_project'){
        $.ajax({
            url:'/changeproject/',
            data:{'new_project':id},
            success:(response)=>{
                $('#existing-project-container').html(response)
                // $('#new-emp-select').selectpicker();
                $('.selectpicker').selectpicker();
            }
        })
    }

    else if(id === 'bluk_client_file'){
        $.ajax({
            url:'/blukprojectupload/',
            data:{'new_project':id},
            success:(response)=>{
                $('#existing-project-container').html(response)
                // $('#new-emp-select').selectpicker();
                $('.selectpicker').selectpicker();
            }
        })

    }
    else{
        $.ajax({
            url:'/changeproject/',
            data:{'existing_project':id},
            success:(response)=>{
                $('#existing-project-container').html(response)
            }
        })
    }
})


// Fetch the employee depending upon project selection
$('#existing-project-container').on('change','#project_type',(e)=>{
    var project_id = $('#project_type').val()
    $.ajax({
        url : '/projectdetailfetch/',
        data:{'project_id':project_id},
        success:(response)=>{
            $('#member-id').html(response)
            $('.selectpicker').selectpicker();
            // console.log($("#members-select").html())
            var selectedOptions = $("#members-select").find('option:selected');
              selectedOptions.detach();
              $("#members-select").prepend(selectedOptions);
              $("#members-select").selectpicker('refresh');
             

        }
    })
})



$('#existing-project-container').on('submit','#new-project-form',(e)=>{
    e.preventDefault()
    let csrfmiddlewaretoken = $("input[name = 'csrfmiddlewaretoken']").prop('value')
    var project_name = $('#new-project-name').val()
    var emp_select = $('#new-emp-select').val();
    var spinner = '<div class =" spinner-border spinner-border-sm text-warning" role = "status"><span class = "visually-hidden">Loading..</span></div>'
    let formData = new FormData();
    formData.append('project_name',project_name)
    formData.append('emp_select',emp_select)
    formData.append('csrfmiddlewaretoken',csrfmiddlewaretoken)
    $('#add-btn').html(spinner)
    $.ajax({
        url:'/addproject/',
        type:'POST',
        data : formData,
        caches:false,
        contentType:false,
        processData:false,
        success:(e)=>{
                alert('New project added successfully.')
                window.location.reload();
        }
    })

})


$('#existing-project-container').on('change','#bluk_file_upload_id',(e)=>{

    if ($('#bluk_file_upload_id').length === 0){


    }
    else{

    $('.bluk-btn').prop("disabled", false);
    }
})

// Bluk File Upload Form Functionality
$('#existing-project-container').on('submit','#bluk-file-id',(e)=>{
    e.preventDefault()
    let csrfmiddlewaretoken = $("input[name = 'csrfmiddlewaretoken']").prop('value')
    var project_name = $('#bluk_file_upload_id').val()
    var client_name = document.getElementById('bluk_file_upload_id').files[0]
    // console.log($('#new-emp-select').val())
    // var emp_select = $('#new-emp-select').val();
    var spinner = '<div class =" spinner-border spinner-border-sm text-warning" role = "status"><span class = "visually-hidden">Loading..</span></div>'
    let formData = new FormData();
    // formData.append('project_name',project_name)
    formData.append('client_name',client_name)
    formData.append('csrfmiddlewaretoken',csrfmiddlewaretoken)
    formData.append('project_name',project_name)
    $('.width-btnn').html(spinner)
    $.ajax({
        url:'/blukprojectupload/',
        type:'POST',
        data : formData,
        caches:false,
        contentType:false,
        processData:false,
        success:(response)=>{
            if (response.message){
                alert('Client added successfully.')
                window.location.reload();
                }
                else{
                    alert(response.error)
                }
                // console.log(e)
                // alert('Client added successfully.')
                // window.location.reload();
        }
    })

})


$('#existing-project-container').on('submit','#existing-project-form',(e)=>{
    e.preventDefault();
    let csrfmiddlewaretoken = $("input[name = 'csrfmiddlewaretoken']").prop('value')
    let formData = new FormData();
    var project_name = $('#project_type').val()
    var emp_select = $('#members-select').val()
    var spinner = '<div class =" spinner-border spinner-border-sm text-warning" role = "status"><span class = "visually-hidden">Loading..</span></div>'
    if ((project_name) &&(emp_select)){
        $('.width-btn').html(spinner)
        formData.append('project_name',project_name)
        formData.append('emp_select',emp_select)
        formData.append('csrfmiddlewaretoken',csrfmiddlewaretoken)
        $.ajax({
            url:'/existingprojectupdate/',
            type:'POST',
            data : formData,
            caches:false,
            contentType:false,
            processData:false,
            success:(e)=>{
                    alert('Project updated successfully.')
                    window.location.reload();
            }
        })
    }
})

$('.selectpicker').selectpicker();

$('#file_upload').change('click',(e)=>{

    if ($('#file_upload').get(0).files.length === 0){


    }
    else{
    $('.spinner-btn').prop("disabled", false);
    }
})

$('#project_type').change('click',(e)=>{

    if ($('#project_type').length === 0){


    }
    else{

    $('.up-del').prop("disabled", false);
    }
})



$('#emps_file_upload').change('click',(e)=>{

    if ($('#emps_file_upload').length === 0){


    }
    else{

    $('.emps-btn').prop("disabled", false);
    }
})



$('#emps-project-containers').on('submit','#emp-upload-file-form',(e)=>{
    e.preventDefault();
    let csrfmiddlewaretoken = $("input[name = 'csrfmiddlewaretoken']").prop('value')
    let emps_file_upload = document.getElementById('emps_file_upload').files[0]
    let formData = new FormData();
    formData.append('emps_file_upload',emps_file_upload)
    formData.append('csrfmiddlewaretoken',csrfmiddlewaretoken)
    var spinner = '<div class =" spinner-border spinner-border-sm text-warning" role = "status"><span class = "visually-hidden">Loading..</span></div>'
    $('.emps-btn').html(spinner)
    $.ajax({
        url:'/employee_upload/',
        type:'POST',
        data : formData,
        caches:false,
        contentType:false,
        processData:false,
        success:(response)=>{
                if (response.message){
                alert('Employee updated successfully.')
                window.location.reload();
                }
                else{
                    alert(response.error)
                }
        }
    })
    
})
