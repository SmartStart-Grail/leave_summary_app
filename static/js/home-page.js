$(document).ready(function () {
    let table = new DataTable('#myTable', {
        // responsive: true,
        // pageLength: 10,
        // lengthMenu: [[10], [10]],
        responsive: true,
        autoWidth: false, // Prevents auto column width issues
        scrollX: false,    // Enables horizontal scrolling
        dom: 'Bfrtip',
        buttons: ['excelHtml5', 'pdfHtml5'],
        lengthMenu: [[10, 25, 50], [ 10, 25, 50]],
        columnDefs: [
            { width: "200px", targets: 0 }, // Adjust width manually if needed
        ]
    });

    let holidaytab = new DataTable('#holidayTable', {
        responsive: true,
        pageLength: 5,
        lengthMenu: [[5], [5]]
    });

    Chart.defaults.set('plugins.datalabels', {
        color: 'black',
        font: {
            size: 7
        }
    });

    let myChart = null; // Declare globally

    // Function to create chart
    const chart_func = () => {
        const ctx = document.getElementById('myChart').getContext('2d');
    
        if (myChart instanceof Chart) {
            myChart.destroy();
        }
    
        myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'Employee available',
                        data: [],
                        backgroundColor: ['rgba(248, 203, 173, 0.7)'],
                    },
                    {
                        label: 'Employee on Leave',
                        data: [],
                        backgroundColor: ['rgba(68,14,196,0.7)'],
                    },
                    {
                        label: 'Employee on Public Holiday',
                        data: [],
                        backgroundColor: 'rgb(64,224,208)',
                    },
                    {
                        label: '10 and More Employees on Leave',
                        data: [],
                        backgroundColor: 'red',
                    },
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    datalabels: {
                        display: true,
                        align: 'center',
                        anchor: 'center',
                        formatter: function (value) {
                            return value > 0 ? value : '';
                        },
                        font: {
                            size: 10,
                            weight: 'bold'
                        }
                    },
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            font: { size: 12 },
                            color: '#333',
                            generateLabels: function (chart) {
                                const defaultLabels = Chart.defaults.plugins.legend.labels.generateLabels(chart);
                                return defaultLabels.map(label => {
                                    if (label.text === 'Employee on Leave') {
                                        return {
                                            ...label,
                                            fillStyle: 'rgba(68,14,196,0.7)', // Fixed legend color
                                        };
                                    }
                                    return label;
                                });
                            }
                        }
                    },
                    tooltip: {
                        enabled: true,
                        callbacks: {
                            label: function (context) {
                                let datasetLabel = context.dataset.label || '';
                                let value = context.raw;
                                return `${datasetLabel}: ${value}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        stacked: true,
                        ticks: {
                            font: { size: 10 },
                            color: 'black'
                        },
                        categoryPercentage: 0.8,
                        barPercentage: 0.9,
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        stacked: true,
                        beginAtZero: true,
                        ticks: {
                            font: { size: 10 },
                            color: 'black',
                            precision: 0
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)',
                            drawBorder: false
                        }
                    }
                }
            },
            plugins: [ChartDataLabels]
        });
    };

    // Function to update chart data
    function updateChart(data) {
        console.log(data)
        if (!data || !data.labels || !data.data1) {
            return;
        }
    
        myChart.data.labels = data.labels;
        myChart.data.datasets[0].data = data.data1; // Employee available
        myChart.data.datasets[1].data = data.data2; // Employee on leave
        myChart.data.datasets[2].data = data.data3; // Employee on holiday
    
        const total_emp = data.total_emp;
    
        const chartColors = {
            red: 'rgb(255, 70, 35)',      // High leave count
            blue: 'rgb(54, 162, 235)',    // Normal holiday
            holi: 'turquoise',            // Full holiday
            available: 'rgba(68,14,196,0.7)' // Low leave count
        };
    
        const leaveColors = [];
        const holidayColors = [];
    
        for (let i = 0; i < myChart.data.datasets[1].data.length; i++) {
            const leaveValue = myChart.data.datasets[1].data[i];
            const holidayValue = myChart.data.datasets[2].data[i];
    
            // Set holiday bar color
            if (holidayValue === total_emp) {
                holidayColors.push(chartColors.holi); // Full holiday
            } else {
                holidayColors.push(chartColors.blue); // Partial holiday/default
            }
    
            // Set leave bar color
            if (leaveValue > 9) {
                leaveColors.push(chartColors.red); // More than 9
            } else {
                leaveColors.push(chartColors.available); // Less than or equal to 9
            }
        }
    
        // Apply new bar colors
        myChart.data.datasets[1].backgroundColor = leaveColors;
        myChart.data.datasets[2].backgroundColor = holidayColors;
    
        myChart.update();
    }
    

    function loadChartData() {
        $('#chart-loader').show(); // Show loader before loading chart
        $('#myChart').hide(); // Hide chart initially

        $.ajax({
            url: '/chartfunction/',
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                chart_func(); // Create chart only once
                updateChart(data);

                $('#chart-loader').hide();
                $('#myChart').show();
            },
            error: function (error) {
                console.log('Error fetching data:', error);
                $('#chart-loader').hide(); // Hide loader on error
            }
        });
    }

    loadChartData();

    $('#next-btn').on('click', (e) => {
        let next_date = $('#next-date-value').val();
        let depart = $('#department-select').val() || null;  // Handle null case
        let locat = $('#location-select').val() || null;
    
        $('#chart-loader').show(); // Show loader before updating
        $('#myChart').hide(); // Hide chart while loading
    
        $.ajax({
            url: '/nextweek/',
            data: {
                'next_date': next_date,
                'depart[]': depart,  // Ensure arrays are sent properly
                'locat[]': locat
            },
            success: (response) => {
                updateChart(response.data); // Update chart without re-creating it
    
                // Update leave table
                $('#leave-table-id').html(response.element1);
    
                // Destroy existing DataTable before reinitialization
                if ($.fn.DataTable.isDataTable('#myTable')) {
                    $('#myTable').DataTable().destroy();
                }
    
                let table = new DataTable('#myTable', {

                    responsive: true,
                    autoWidth: false, // Prevents auto column width issues
                    scrollX: false,    // Enables horizontal scrolling
                    dom: 'Bfrtip',
                    buttons: ['excelHtml5', 'pdfHtml5'],
                    lengthMenu: [[10, 25, 50], [ 10, 25, 50]],

                });

                $('#holiday-table').html(response.holiday_content)
                let holiday_table = new DataTable('#holidayTable', {

                    responsive: true,
                    pageLength: 5,
                    lengthMenu: [[5], [5]]
                });
    
                // Hide loader and show chart
                $('#chart-loader').hide();
                $('#myChart').show();
    
                // Update date values
                $('#previous-date-value').val(response.previous_week);
                $('#next-date-value').val(response.next_week);
            },
            error: function (error) {
                console.error('Error fetching data:', error);
                alert('Failed to fetch data. Please try again.');
    
                $('#chart-loader').hide();
                $('#myChart').show();
            }
        });
    });
    
    //After clicking on prev btn on homepage, This event is fire and call the function
    $('#prev-btn').on('click', (e) => {
        let next_date = $('#next-date-value').val();
        let prev_date = $('#previous-date-value').val();

        let today = new Date().toISOString().split('T')[0];
        let prev_dates = new Date(prev_date)

        let year = prev_dates.getFullYear();
        let month = String(prev_dates.getMonth() + 1).padStart(2, '0'); // Ensure two digits
        let day = String(prev_dates.getDate()).padStart(2, '0');
        let formattedDate = `${year}-${month}-${day}`;

        let depart =  $('#department-select').val() ||null
        let locat =  $('#location-select').val()||null
        if((today <= formattedDate) && (formattedDate)){
            $('#chart-loader').show(); // Show loader before updating
            $('#myChart').hide(); // Hide chart while loading
            $.ajax({
                url: '/previousweek/',
                data: { 'next_date': next_date, 'prev_date':prev_date,'depart':depart,'locat':locat},
                success: (response) => {

                    updateChart(response.data); // Update chart without re-creating it

                $('#leave-table-id').html(response.element1);
                // Destroy existing DataTable before reinitialization
                if ($.fn.DataTable.isDataTable('#myTable')) {
                    $('#myTable').DataTable().destroy();
                }
    
                let table = new DataTable('#myTable', {

                    responsive: true,
                    autoWidth: false, // Prevents auto column width issues
                    scrollX: false,    // Enables horizontal scrolling
                    dom: 'Bfrtip',
                    
                    buttons: ['excelHtml5', 'pdfHtml5'],
                    lengthMenu: [[10, 25, 50], [ 10, 25, 50]],
                    columnDefs: [
                        { width: "200px", targets: 0 }, // Adjust width manually if needed
                    ]
                });
                    $('#holiday-table').html(response.holiday_content)
                    let holiday_table = new DataTable('#holidayTable', {

                        responsive: true,
                        pageLength: 5,
                        lengthMenu: [[5], [5]]
                    });
        
                    //  Hide loader and show chart after update
                    $('#chart-loader').hide();
                    $('#myChart').show();
        
                    $('#previous-date-value').val(response.previous_week);
                    $('#next-date-value').val(response.next_week);
                },
                error: function (error) {
                    console.log('Error fetching data:', error);
                    $('#chart-loader').hide();
                    $('#myChart').show();
                }
            });
        }

    })
    $('#filter-id').on('change','.selectpicker',(e)=>{
        $('.btn-filt').attr('disabled',false);
    })
    
    $('#cf').on('click',(e)=>{
        $('.btn-filt').attr('disabled', true);
    
    })


    //Filter Function
    $('#filter-form-home-id').on('submit', '#filter-form-home', function (e) {
        e.preventDefault();
        // var values = $(this).serialize();;
        let values = new FormData(this);  // Convert form to FormData
        let next_date = $('#next-date-value').val();
        values.append('next_date', next_date);  // Append extra data

        //Important how to object data.
        // var formData = {};
        // $(this).serializeArray().forEach(function (field) {
        //     formData[field.name] = field.value;
        // });

        // console.log(formData); // Now this will return the correct object
        if ([...values.entries()].length > 1){
        $('#chart-loader').show();
        $('#myChart').hide();
        // $('#leave-table-id').hide();
        $('#exampleModal').modal('hide');
        $.ajax({
            url:'/homefilter/',
            type:'post',
            data:values,
            processData: false,  // Prevent jQuery from processing the data
            contentType: false,  // Prevent jQuery from setting the content type
            success:(response)=>{

                updateChart(response.data); // Update chart without re-creating it
                // Update leave table
                $('#leave-table-id').html(response.element1);
    
                // Destroy existing DataTable before reinitialization
                if ($.fn.DataTable.isDataTable('#myTable')) {
                    $('#myTable').DataTable().destroy();
                }
    
                let table = new DataTable('#myTable', {

                    responsive: true,
                    autoWidth: false, // Prevents auto column width issues
                    scrollX: false,    // Enables horizontal scrolling
                    dom: 'Bfrtip',
                    buttons: ['excelHtml5', 'pdfHtml5'],
                    lengthMenu: [[10, 25, 50], [ 10, 25, 50]],
                    columnDefs: [
                        { width: "200px", targets: 0 }, // Adjust width manually if needed
                    ]
                });
                $('#chart-loader').hide();
                $('#myChart').show();
                // $('#leave-table-id').show();
            }

        })
    }
    });


    //Clear Filter Function
    $('#cf').on('click',(e)=>{
    $.ajax({
        url:'/clearhomefilter/',
        success:(response)=>{
            $('#filter-id').html(response.element)
            $('.selectpicker').selectpicker()
            // window.location.reload();
        }
        })
    })


    //Close Btn Function
    $('#close-filter-btn').on('click',(e)=>{
        let departmentSelected = $('#department-select').val() && $('#department-select').val().length > 0;
        let locationSelected = $('#location-select').val() && $('#location-select').val().length > 0;
        if (departmentSelected || locationSelected){
            $('#exampleModal').modal('hide');
        }
        else{
            window.location.reload();
        }
    })





});
//End Of Documents





