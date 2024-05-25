import React, { useEffect, useState, useContext } from 'react';
import { Line } from 'react-chartjs-2';
import axios from 'axios';
import 'chart.js/auto';
import './components.css';
import { DataContext } from '../services/DataContext';

const ChartComponent = ({ start_time, end_time }) => {
    const { webResponseTime, throughput, apdex, errorRate } = useContext(DataContext);
    const [chartData, setChartData] = useState({ datasets: [] });
    const [chartData2, setChartData2] = useState({ datasets: [] });
    const [chartData3, setChartData3] = useState({ datasets: [] });
    const [chartData4, setChartData4] = useState({ datasets: [] });

    const formatData = (data, label, borderColor, backgroundColor, fill) => {
        const labels = data.map(item => new Date(item[0]).toLocaleString('en-GB', {
            day: '2-digit',
            month: '2-digit',
            year: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        }));
        const values = data.map(item => item[1] !== null ? item[1] : 0);  // заменяем 0 на null для плавности

        return {
            labels: labels,
            datasets: [
                {
                    label: label,
                    data: values,
                    borderColor: borderColor,
                    backgroundColor: backgroundColor,
                    fill: fill,
                    tension: 1.0,
                    borderWidth: 1.0,
                    pointBorderWidth: 0.0,
                    pointRadius: 0
                }
            ]
        };
    };

    const filterDataByTime = (data, start_time, end_time) => {
        const startDate = new Date(start_time);
        const endDate = new Date(end_time);
        return data.filter(item => {
            const itemDate = new Date(item[0]);
            return itemDate >= startDate && itemDate <= endDate;
        });
    };

    useEffect(() => {
        if (!start_time || !end_time) {
            console.log('Null time');
            return;
        }

        if (webResponseTime.length > 0) {
            const filteredData = filterDataByTime(webResponseTime, start_time, end_time);
            setChartData(formatData(filteredData, 'WR', 'rgba(153,102,255,1)', 'rgba(153,102,255,0.2)', true));
        } else {
            axios.get(`api/web-response-time?start_time=${start_time}&end_time=${end_time}`)
                .then(response => {
                    const data = response.data.data;
                    setChartData(formatData(data, 'WR', 'rgba(153,102,255,1)', 'rgba(153,102,255,0.2)', true));
                })
                .catch(error => console.error('Error fetching data: ', error));
        }
    }, [start_time, end_time, webResponseTime]);

    useEffect(() => {
        if (!start_time || !end_time) {
            console.log('Null time');
            return;
        }

        if (throughput.length > 0) {
            const filteredData = filterDataByTime(throughput, start_time, end_time);
            setChartData2(formatData(filteredData, 'THROUGHPUT', 'rgba(54,162,235,1)', 'rgba(54,162,235,0.2)', true));
        } else {
            axios.get(`api/throughput?start_time=${start_time}&end_time=${end_time}`)
                .then(response => {
                    const data = response.data.data;
                    setChartData2(formatData(data, 'THROUGHPUT', 'rgba(54,162,235,1)', 'rgba(54,162,235,0.2)', true));
                })
                .catch(error => console.error('Error fetching data: ', error));
        }
    }, [start_time, end_time, throughput]);

    useEffect(() => {
        if (!start_time || !end_time) {
            console.log('Null time');
            return;
        }

        if (apdex.length > 0) {
            const filteredData = filterDataByTime(apdex, start_time, end_time);
            setChartData3(formatData(filteredData, 'APDEX', 'rgba(75,192,192,1)', 'rgba(75,192,192,0.2)', false));
        } else {
            axios.get(`api/apdex?start_time=${start_time}&end_time=${end_time}`)
                .then(response => {
                    const data = response.data.data;
                    setChartData3(formatData(data, 'APDEX', 'rgba(75,192,192,1)', 'rgba(75,192,192,0.2)', false));
                })
                .catch(error => console.error('Error fetching data: ', error));
        }
    }, [start_time, end_time, apdex]);

    useEffect(() => {
        if (!start_time || !end_time) {
            console.log('Null time');
            return;
        }

        if (errorRate.length > 0) {
            const filteredData = filterDataByTime(errorRate, start_time, end_time);
            setChartData4(formatData(filteredData, 'ERROR-RATE', 'rgba(255,99,132,1)', 'rgba(255,99,132,0.2)', true));
        } else {
            axios.get(`api/error-rate?start_time=${start_time}&end_time=${end_time}`)
                .then(response => {
                    const data = response.data.data;
                    setChartData4(formatData(data, 'ERROR-RATE', 'rgba(255,99,132,1)', 'rgba(255,99,132,0.2)', true));
                })
                .catch(error => console.error('Error fetching data: ', error));
        }
    }, [start_time, end_time, errorRate]);

    return (
        <div className="chart-grid">
            <div className="chart-item">
                <Line data={chartData} />
            </div>
            <div className="chart-item">
                <Line data={chartData2} />
            </div>
            <div className="chart-item">
                <Line data={chartData3} />
            </div>
            <div className="chart-item">
                <Line data={chartData4} />
            </div>
        </div>
    );
};

export default ChartComponent;
