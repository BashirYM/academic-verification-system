import React from 'react';
import '../styles/LoadingSpinner.css';

function LoadingSpinner() {
  return (
    <div className="spring-spinner">
      <div className="spring-spinner-part top">
        <div className="spring-spinner-rotator" />
      </div>
      <div className="spring-spinner-part bottom">
        <div className="spring-spinner-rotator" />
      </div>
    </div>
  );
}

export default LoadingSpinner;
