import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

const DataContext = createContext();

export const useData = () => {
  return useContext(DataContext);
};

const DataProvider = ({ children }) => {
  const [data, setData] = useState([]);
  const [anomCount, setAnomCount] = useState(0);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/api/enchanced_fwda');
        setData(response.data.data);
        setAnomCount(response.data.count);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <DataContext.Provider value={{ data, anomCount }}>
      {children}
    </DataContext.Provider>
  );
};

export { DataContext, DataProvider };
