const initWebsockets = () => {
    const msgContainerEl = document.getElementById('container');

    let ws = new WebSocket('ws://localhost:8000/ws');
    let counter = 0; 

    ws.onmessage = (e) => { 
        msgContainerEl.innerHTML += `
            <p>websocket message: ${e.data}</p>
        `;
    };

    ws.onclose = () => { 
        console.log('Closing websocket connection');
    };
}

initWebsockets(); 