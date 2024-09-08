const chatSocket = new WebSocket(  
    'ws://' + window.location.host + '/ws/chat/'  
);  

let chatWindow = document.getElementById('chat-window');  

chatSocket.onmessage = function(e) {  
    const data = JSON.parse(e.data);  
    const message = data.message;  
    const user = data.user;  
    const currentUser = data.current_user;  

    // Create a new message element  
    const messageDiv = document.createElement('div');
    if (user == currentUser){
        messageDiv.innerHTML = `<div class="chat chat-start"><div class="chat-bubble chat-bubble-primary">${message}</div></div>`;  
    } else {
        messageDiv.innerHTML = `<div class="chat chat-end"><div class="chat-bubble">${message}</div></div>`;
    }
    chatWindow.appendChild(messageDiv);  
    chatWindow.scrollTop = chatWindow.scrollHeight;  // Scroll to the bottom  
};  

chatSocket.onclose = function(e) {  
    console.error('Chat socket closed unexpectedly');  
};  

document.body.addEventListener('htmx:wsAfterMessage', (e) => {  
    // This can be used to trigger any additional actions after a message is received
    console.log('New message received via WebSocket');
}); 