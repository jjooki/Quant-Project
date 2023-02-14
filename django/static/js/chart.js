class Chart {
    constructor() {
        this.height = 350;
        this.chartObject = new Object();

        axios.defaults.xsrfCookieName = 'csrftoken';
		axios.defaults.xsrfHeaderName = 'X-CSRFToken';
    }

    drawChart(canvas_id, data, type, colors, height=null) {
        const options = {
            series: data,

            colors: colors,

            chart: {
                type: type,
                stacked: false,
                height: (height === null) ? this.height : height,
                width: '100%',
                zoom: {
                    type: 'xy',
                    enabled: true,
                    autoScaleYaxis: true
                },
                toolbar: {
                    autoSelected: 'zoom'
                }
            },

            dataLabels: {
                enabled: false
            },

            markers: {
                size: 0,
            },

            fill: {
                type: 'gradient',
                gradient: {
                    opacityFrom: 0,
                    opacityTo: 0,
                },
            },

            tooltip: {
                shared: false,
            },
        };

        const chart = new ApexCharts(document.getElementById(canvas_id), options);
        chart.render();
        return chart;
    }

    updateChart(chart, data) {
        chart.updateSeries(data);
    }

    getAxios(url, method, formData=null) {
        const self = this;
        let kwargs = {
            url: url,
	        method: method,
        }

        if (method == 'post' && formData != null) {
            kwargs['data'] = formData;
        }

        axios(kwargs)
        .then(function (response) {
            const data = response.data;

            Object.keys(data).forEach(key => {
                if (method == 'get') {
                    self.chartObject[key] = self.drawChart(
                        key, 
                        data[key]['data'], 
                        data[key]['type'],
                        data[key]['colors'],
                        data[key]['height']
                    );
                } else {
                    self.updateChart(
                        self.chartObject[key],
                        data[key]['data'], 
                    );
                }
            })
        }).catch(function (err) {
            console.error(err);
        })
    }

    requestGet(url) {
        this.getAxios(url, 'get');
    }

    requestPost(url) {
        document.getElementById('select-options-form').addEventListener('submit', e => {
            e.preventDefault();

            const formData = new FormData(e.target);
            this.getAxios(url, 'post', formData);
        });
    }
}