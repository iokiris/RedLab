import React, { useState, useEffect } from 'react';
import './Notification.css';
import {ReactComponent as WarningIcon} from '../../media/svg/warning-icon.svg'
const Notification = ({ type, message, isVisible, setIsVisible }) => {
  useEffect(() => {
    if (isVisible) {
      const timer = setTimeout(() => {
        setIsVisible(false);
      }, 3000); 

      return () => clearTimeout(timer); 
    }
  }, [isVisible, setIsVisible]);

  return (
    <>
      {isVisible && (
        <div className={`notification ${type === 'warn' ? 'warn' : ''}`}>
          {type === 'warn' && (
            <WarningIcon />
          )}
          <span className="notification-message">{message}</span>
        </div>
      )}
    </>
  );
};

export default Notification;
