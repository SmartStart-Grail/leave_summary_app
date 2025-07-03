
// import ChartDataLabels from 'chartjs-plugin-datalabels';
// new BrowserWindow({ webPreferences: { nodeIntegration: true } }); 
// const ChartDataLabels = require('chartjs-plugin-datalabels');
$(document).ready( function () {




    let table = new DataTable('#myTable', {
        responsive: true,
        pageLength : 10,
        lengthMenu: [[10], [10]]

    });

    let holidaytab = new DataTable('#holidayTable', {
        responsive: true,
        pageLength : 2,
        lengthMenu: [[2], [2]]

    });
    // lengthMenu: [[2, 10, 20], [2, 10, 20]] For reference
    Chart.defaults.set('plugins.datalabels', {
        color: 'black',
        font:{
            size:7
        }
      });
    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
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
                            label: 'Employee on leave',
                            data: [],
                            backgroundColor: ['rgba(68,14,196,0.7)'],
                        },
                        // {
                        //     label: 'Data3',
                        //     data: [],
                        //     backgroundColor: 'rgba(255, 206, 86, 0.7)',
                        // },
    
            ]
        },
        options: {
            plugins: {
                datalabels: {
                    display: true,
                    align: 'center',
                    anchor: 'center'
                 },
                 
                legend: {
                    plugins:{
                        legend:{
                        display:false
                    }},

                    labels: {
                        // This more specific font property overrides the global property
                        font: {
                            size: 8
                        }
                    }
                }
            },
            
            scales: {
                xAxes: [{
                    ticks: {
                     fontSize: 2
                    }
                   }],
                x: {
                    stacked: true,
                    ticks: {
                        font: {
                          size: 8,
                        //   weight: "bold"
                        },
                        color: 'black',
                      },
                },
                y: {
                    stacked: true
                }
            }
        },
        plugins: [ChartDataLabels],
        datalabels: {
            color: "#ffffff",
            font: {
              size:2,
            }
        },
//   options: {
//     // ...
//   }

    })

    function updateChart(data) {
        myChart.data.labels = data.labels;
        myChart.data.datasets[0].data = data.data1;
        myChart.data.datasets[1].data = data.data2;
        // myChart.data.datasets[2].data = data.data3;

        var colorChangeValue = 32;
        var dataset = myChart.data.datasets[0];
        var dataset_holiday = myChart.data.datasets[1]
        var chartColors = {
            red: 'rgb(255, 70, 35)',
            blue: 'rgb(54, 162, 235)',
            holi:'rgb(192,0,0)'
          };
        // for (var i = 0; i < dataset.data.length; i++) {
        // if (dataset.data[i] > colorChangeValue) {

        //     dataset.backgroundColor[i] = chartColors.red;

        // }
        // else{
        //     dataset.backgroundColor[i] = 'rgba(248, 203, 173, 0.7)';
        // }
        // }


        for (var i = 0; i < dataset_holiday.data.length; i++) {
            if (dataset_holiday.data[i] == 35){
                console.log('inside of console')
                dataset_holiday.backgroundColor[i] = chartColors.holi;
            }

            else if (dataset_holiday.data[i] > 9){
                console.log('elsekaksdk')
                dataset_holiday.backgroundColor[i] = chartColors.red;
            }



            else{
                console.log('nknskndksndk')
                dataset_holiday.backgroundColor[i] = 'rgba(68,14,196,0.7)';
            }
            }
        myChart.update();
    }
    $.ajax({
        url: '/chartfunction/',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            updateChart(data);
        },
        error: function (error) {
            console.log('Error fetching data:', error);
        }
    });






});

    // new Chart(ctx, {
    //   type: 'bar',
    //   data: {
    //     labels: ['3-july', '6-july', '7-july', '8-july', '9-july', '10-july'],
    //     datasets: [{
    //       label: '# of Votes',
    //       data: [12, 19, 3, 5, 2, 3],
    //       borderWidth: 1,
    //       barThickness:15,
    //       borderColor: '#36A2EB',
    //       backgroundColor: [
    //         'rgba(255, 99, 132, 0.2)',
    //         'rgba(255, 159, 64, 0.2)',
    //         'rgba(255, 205, 86, 0.2)',
    //         'rgba(75, 192, 192, 0.2)',
    //         'rgba(54, 162, 235, 0.2)',
    //         'rgba(153, 102, 255, 0.2)',
    //         'rgba(201, 203, 207, 0.2)'
    //       ],
    //     }]
    //   },
    //   options: {
    //     scales: {
    //       y: {
    //         beginAtZero: true
    //       }
    //     }
    //   }
    // });
    // ctx.defaults.backgroundColor = 'green';
    // ctx.defaults.borderColor = '#36A2EB';
    // const use1 = '{{ data |escapejs }}'
    // console.log(use1)
    // // var username = {{data|escapejs}};
    // var config = {
    //     type: 'pie',
    //     data: {
    //       datasets: [{
    //         data: JSON.parse('{{ data | tojson | safe}}'),
    //         backgroundColor: [
    //           '#696969', '#808080', '#A9A9A9', '#C0C0C0', '#D3D3D3'
    //         ],
    //         label: 'Population'
    //       }],
    //       labels: JSON.parse('{{ labels| tojson | safe}}')
    //     },
    //     options: {
    //       responsive: true
    //     }
    //   };

    // var myContext = document.getElementById( 
    //     "myChart").getContext('2d'); 
    
    
    
    // });
    
    // var myChart = new Chart(myContext, { 
    //     type: 'bar', 
        // data: { 
        //     labels: ["3-July", "6-July", "7-July",  
        //         "8-July", "9-July", "10-July","13-July","14-July"], 
        //     datasets: [{ 
        //         label: 'Employee on off', 
        //         backgroundColor: "blue", 
        //         data: [0, 2, 1, 5, 9, 6, 10,4], 
        //     }, { 
        //         label: 'Employee Available', 
        //         backgroundColor: "rgb(243,203,173)", 
        //         data: [34, 32, 33, 29, 25, 28,24,30], 
        //     }
        //     ], 
        // }, 
//         data: {
//             datasets: [{
//               data: {{ data|safe }},
//               backgroundColor: [
//                 '#696969', '#808080', '#A9A9A9', '#C0C0C0', '#D3D3D3'
//               ],
//               label: 'Population'
//             }],
//             labels: {{ labels|safe }}
//           },

//         options: { 
//             plugins: { 
//                 title: { 
//                     display: true, 
//                     text: 'Employee Availabilty' 
//                 }, 
//             },
//             responsive: true, 
//             maintainAspectRatio: false,

//             scales: { 
//                 x: { 
//                     stacked: true, 
//                 }, 
//                 y: { 
//                     stacked: true 
//                 } 
//             } 
//         } 
//     }); 
// } );




