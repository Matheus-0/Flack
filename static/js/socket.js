document.addEventListener('DOMContentLoaded', () => {
    const socket = io.connect('http://' + document.domain + ':' + location.port);

    let room = 'lounge';

    joinRoom(room);

    // Display messages
    socket.on('message', data => {
        const paragraph = document.createElement('p');
        const span = document.createElement('span');
        const timestamp = document.createElement('span');
        const line = document.createElement('br');

        if (data.username) {
            span.innerHTML = data.username;
            timestamp.innerHTML = data.timestamp;
            paragraph.innerHTML = span.outerHTML + line.outerHTML + data.message + line.outerHTML + timestamp.outerHTML;

            document.querySelector('#display-message-section').append(paragraph);
        }
        else {
            printSystemMessage(data.message);
        }
    });

    // Send message
    document.querySelector('#send-message').onclick = () => {
        socket.send({
            'message': document.querySelector('#user-message').value,
            'username': username,
            'room': room
        });

        // Clear input area
        document.querySelector('#user-message').value = '';
    };

    // Room selection
    document.querySelectorAll('.select-room').forEach(paragraph => {
        paragraph.onclick = () => {
            let newRoom = paragraph.innerHTML;

            if (newRoom === room) {
                const message = `You are already in this room.`;
                printSystemMessage(message);
            }
            else {
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom;
            }
        };
    });

    // Leave room
    function leaveRoom(room) {
        socket.emit('leave', {
            'username': username,
            'room': room
        })
    }

    // Join room
    function joinRoom(room) {
        socket.emit('join', {
            'username': username,
            'room': room
        });

        // Clear message area
        document.querySelector('#display-message-section').innerHTML = '';

        // Autofocus on input
        document.querySelector('#user-message').focus();
    }

    // Print system message
    function printSystemMessage(message) {
        const paragraph = document.createElement('p');

        paragraph.innerHTML = message;

        document.querySelector('#display-message-section').append(paragraph);
    }
});