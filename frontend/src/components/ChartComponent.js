import React, { useEffect, useState, useContext } from 'react';
import { Line } from 'react-chartjs-2';
import axios from 'axios';
import 'chart.js/auto';
import './components.css';
import { DataContext } from '../services/DataContext';
import Notification from './Notification/Notification';

const ChartComponent = ({ start_time, end_time }) => {
  const { data: contextData } = useContext(DataContext);
  const [chartData, setChartData] = useState({ datasets: [] });
  const [chartData2, setChartData2] = useState({ datasets: [] });
  const [chartData3, setChartData3] = useState({ datasets: [] });
  const [chartData4, setChartData4] = useState({ datasets: [] });
  const [anomalyCount, setAnomalyCount] = useState(0);
  const [showLargeRequestNotification, setShowLargeRequestNotification] = useState(false);

  const aggregateData = (data, interval) => {
    const aggregated = [];
    let sum = 0;
    let count = 0;
    let currentInterval = null;

    data.forEach(item => {
      const itemDate = new Date(item[0]);
      const itemValue = item[1] !== null ? item[1] : 0;

      if (!currentInterval) {
        currentInterval = new Date(itemDate);
        currentInterval.setMinutes(Math.floor(currentInterval.getMinutes() / interval) * interval);
      }

      if (itemDate - currentInterval < interval * 60 * 1000) {
        sum += itemValue;
        count += 1;
      } else {
        aggregated.push([currentInterval.getTime(), sum / count]);
        currentInterval = new Date(itemDate);
        currentInterval.setMinutes(Math.floor(currentInterval.getMinutes() / interval) * interval);
        sum = itemValue;
        count = 1;
      }
    });

    if (count > 0) {
      aggregated.push([currentInterval.getTime(), sum / count]);
    }

    return aggregated;
  };

  const formatData = (data, label, borderColor, backgroundColor, fill) => {
    const labels = data.map(item => new Date(item[0]).toLocaleString('en-GB', {
      day: '2-digit',
      month: '2-digit',
      year: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    }));
    const values = data.map(item => item[1] !== null ? item[1] : 0); // заменяем null на 0 для плавности
    let borderSize = 2.0;
    if (values.length > 1000) {
      borderSize = 1.0;
    }

    return {
      labels: labels,
      datasets: [
        {
          label: label,
          data: values,
          borderColor: borderColor,
          backgroundColor: backgroundColor,
          fill: fill,
          tension: 0.0,
          borderWidth: borderSize,
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
      return;
    }
    const fetchData = async () => {
      try {
        const response = await axios.get(`/api/enchanced_fwda?start_time=${start_time}&end_time=${end_time}`);
        const data = response.data.data;
        processChartData(data);
        // Подсчет аномалий
        const count = data.reduce((acc, item) => acc + item[5], 0);
        setAnomalyCount(count);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    const processChartData = (data) => {
      const wrData = data.map(item => [item[0], item[1]]);
      const thData = data.map(item => [item[0], item[2]]);
      const apdexData = data.map(item => [item[0], item[3]]);
      const fwdaData = data.map(item => [item[0], item[4]]);

      setChartData(formatData(aggregateData(wrData, 5), 'WR', 'rgba(153,102,255,1)', 'rgba(153,102,255,0.2)', true));
      setChartData2(formatData(aggregateData(thData, 5), 'THROUGHPUT', 'rgba(54,162,235,1)', 'rgba(54,162,235,0.2)', true));
      setChartData3(formatData(aggregateData(apdexData, 5), 'APDEX', 'rgba(75,192,192,1)', 'rgba(75,192,192,0.2)', false));
      setChartData4(formatData(aggregateData(fwdaData, 5), 'ANOMALITY RATE', 'rgba(255,99,132,1)', 'rgba(255,99,132,0.2)', true));
    };

    if (contextData.length === 0) {
      fetchData();
    } else {
      const filteredData = filterDataByTime(contextData, start_time, end_time);
      processChartData(filteredData);
      // подсчет аномалий в отфильтрованных данных
      const count = filteredData.reduce((acc, item) => acc + item[5], 0);
      setAnomalyCount(count);
    }

    const duration = Math.abs(new Date(end_time) - new Date(start_time)) / (1000 * 60 * 60);
    setShowLargeRequestNotification(duration > 48); // показываем плашку из временного промежутка
  }, [start_time, end_time, contextData]);

  return (
    <div className="chart-grid">
      {showLargeRequestNotification && <Notification type="warn" message="Выбран большой промежуток, возможны задержки." isVisible={showLargeRequestNotification} setIsVisible={setShowLargeRequestNotification} />}
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
      <div className="anomaly-count">
        <p>Количество аномалий: {anomalyCount}</p>
      </div>
    </div>
  );
};

export default ChartComponent;
