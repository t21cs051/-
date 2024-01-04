const plugin = {
    id: 'custom_background_color',
    beforeDraw: (chart, args, options) => {
        const {ctx} = chart;
        ctx.save();
        ctx.globalCompositeOperation = 'destination-over';
        ctx.fillStyle = options.color;
        ctx.fillRect(0, 0, chart.width, chart.height);
        ctx.restore();
    },
    defaults: {
        color: 'lightGreen'
    }
}


        // TODO: Chart.jsのバージョンアップに伴い、以下の関数は非推奨になったので、代替案を探す
        function drawBackground(target) {
            console.log('drawBackground is called');
            var capacity = 30;
            var rate70 = capacity * 0.7;
            var rate50 = capacity * 0.5;
            var xscale = target.scales["x-axis-0"];
            var yscale = target.scales["y-axis-0"];
            var left = xscale.left;
            var high_top = yscale.height;
            var high_height = yscale.getPixelForValue(rate70) - high_top; // 赤
            var middle_top = yscale.getPixelForValue(rate70);
            var middle_height = yscale.getPixelForValue(rate50) - middle_top;   // オレンジ
            var middle_top = yscale.getPixelForValue(rate50);
            var low_height = yscale.getPixelForValue(rate50) - low_top;   // 青

            // 赤い範囲
            ctx.fillStyle = "rgba(255, 0, 100, 0.2)";
            ctx.fillRect(left, high_top, xscale.width, high_height);

            // オレンジの範囲
            ctx.fillStyle = "rgba(255, 165, 0, 0.2)";
            ctx.fillRect(left, middle_top, xscale.width, middle_height);

            // 青い範囲
            ctx.fillStyle = "rgba(0, 100, 255, 0.2)";
            ctx.fillRect(left, low_top, xscale.width, low_height);
        }


var ctx{{ power_system }} = document.getElementById("Chart{{ power_system }}").getContext('2d');
var chart{{ power_system }} = new Chart(ctx, {
    type: 'line',
    data: lineChartData{{ power_system }},
    options: {
        plugins: [plugin],
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: {
                scaleLabel: {
                    display: true,
                },
                type: 'time',
                min: '{{ start_date }}',
                max: '{{ end_date }}',
                time: {
                    parser: 'YYYY-MM-DDTHH:mm:ss.SSSSSSZ',
                    unit: 'day',
                    stepSize: 1,
                    displayFormats: {
                        'day': 'MM月DD日'
                    }
                },
            },
            y: {
                beginAtZero: true,
                max: {{ capacity|get_item:power_system }},
                ticks: {
                    stepSize: 5,
                },
            },
        }
    }
});

                        annotation: {
                            annotations: {
                                {% for worklog in worklogs %}
                                'worklog{{ forloop.counter }}': {
                                    type: 'line',
                                    xMin: '{{ worklog.date }}',
                                    xMax: '{{ worklog.date }}',
                                    borderColor: 'rgb(255, 99, 132)',
                                    borderWidth: 2,
                                    label: {
                                        content: '{{ worklog.description }}',
                                        position: 'start',
                                        enabled: true
                                    }
                                },
                                {% endfor %}
                            }
                        }, 