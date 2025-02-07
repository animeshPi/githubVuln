import React, { useEffect, useState } from 'react';

const WebSocketClient = ({ url }) => {
  const [ws, setWs] = useState(null);

  useEffect(() => {
    // Establish WebSocket connection
    const newWs = new WebSocket(url);

    // Store the WebSocket connection
    setWs(newWs);

    // Clean up function to close the WebSocket connection when component unmounts
    return () => {
      newWs.close();
    };
  }, [url]); // Run once on component mount

  const sendData = (data) => {
    if (ws) {
      ws.send(JSON.stringify(data));
      console.log('Sent message to server:', data);
    } else {
      console.error('WebSocket connection not established.');
    }
  };

  return sendData; // Return the sendData function so it can be used elsewhere
};

export default WebSocketClient;
