import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ChartComponent from './ChartComponent';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { registerLocale, setDefaultLocale } from 'react-datepicker';
import ru from 'date-fns/locale/ru';

registerLocale('ru', ru);
setDefaultLocale('ru');

const ChartPage = () => {
    const [startTime, setStartTime] = useState('');
    const [endTime, setEndTime] = useState('');
    
    const minTime = '2024-04-15T00:00:00'
    const maxTime = '2024-05-16T00:00:00'
   

    const formatTime = (time) => {
        if (!time) return '';
        const date = new Date(time);
        const formattedTime = date.toISOString().slice(0, 19);
        return formattedTime;
    };

    return (
        <div className="container">
            <form>
                <div className="cp-form-group">
                    <label htmlFor="start_time" className="cp-time-label">Начальное время:</label>
                    <DatePicker
                        id="start_time"
                        className="form-control"
                        selected={startTime}
                        onChange={(date) => setStartTime(date)}
                        showTimeSelect
                        timeFormat="HH:mm"
                        timeIntervals={5}
                        dateFormat="Pp"
                        locale="ru"
                        minDate={minTime}
                        maxDate={maxTime}
                    />
                </div>

                <div className="cp-form-group">
                    <label htmlFor="end_time" className='cp-time-label'>Конечное время:</label>
                    <DatePicker
                        id="end_time"
                        className="form-control"
                        selected={endTime}
                        onChange={(date) => setEndTime(date)}
                        showTimeSelect
                        timeFormat="HH:mm"
                        timeIntervals={5}
                        dateFormat="Pp"
                        locale="ru"
                        minDate={minTime}
                        maxDate={maxTime}
                    />
                </div>
            </form>
            <ChartComponent start_time={formatTime(startTime)} end_time={formatTime(endTime)} limit={3.3329455500570346} />
        </div>
    );
};

export default ChartPage;
