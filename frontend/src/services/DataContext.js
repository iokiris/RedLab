import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

const DataContext = createContext();

export const useData = () => {
  return useContext(DataContext);
};

const DataProvider = ({ children }) => {
  const [webResponseTime, setWebResponseTime] = useState([]);
  const [throughput, setThroughput] = useState([]);
  const [apdex, setApdex] = useState([]);
  const [errorRate, setErrorRate] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response1 = await axios.get(`/api/web-response-time`);
        setWebResponseTime(response1.data.data);

        const response2 = await axios.get(`/api/throughput`);
        setThroughput(response2.data.data);

        const response3 = await axios.get(`/api/apdex`);
        setApdex(response3.data.data);

        const response4 = await axios.get(`/api/error-rate`);
        setErrorRate(response4.data.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);
  return (
    <DataContext.Provider value={{ webResponseTime, throughput, apdex, errorRate }}>
      {children}
    </DataContext.Provider>
  );
};

export { DataContext, DataProvider };
