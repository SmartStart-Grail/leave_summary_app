

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
                console.log(e)
                alert('File uploaded successfully.')
                window.location.reload();
        }

    })
})




$('.project-radio').on('click',(e)=>{
    console.log('radio-button-clicked')
    var id = e.target.id
    console.log(id)
    if (id === 'new_project'){
        console.log('new project selected')
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
    console.log('changing is done')

    console.log($('#project_type').val())
    var project_id = $('#project_type').val()
    $.ajax({
        url : '/projectdetailfetch/',
        data:{'project_id':project_id},
        success:(response)=>{
            $('#member-id').html(response)
            $('.selectpicker').selectpicker();

        }
    })
})



$('#existing-project-container').on('submit','#new-project-form',(e)=>{
    e.preventDefault()
    let csrfmiddlewaretoken = $("input[name = 'csrfmiddlewaretoken']").prop('value')
    var project_name = $('#new-project-name').val()
    console.log($('#new-emp-select').val())
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
                console.log(e)
                alert('New project added successfully.')
                window.location.reload();
        }
    })

})


$('#existing-project-container').on('submit','#existing-project-form',(e)=>{
    e.preventDefault();
    console.log('existing form submit')
    let csrfmiddlewaretoken = $("input[name = 'csrfmiddlewaretoken']").prop('value')
    let formData = new FormData();
    var project_name = $('#project_type').val()
    console.log(project_name)
    var emp_select = $('#members-select').val()
    var spinner = '<div class =" spinner-border spinner-border-sm text-warning" role = "status"><span class = "visually-hidden">Loading..</span></div>'
    console.log(emp_select)
    if ((project_name) &&(emp_select)){
        console.log('both field selecrt')
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
                    console.log(e)
                    alert('Project updated successfully.')
                    window.location.reload();
            }
        })
    }
})

$('.selectpicker').selectpicker();

