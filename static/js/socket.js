document.addEventListener('DOMContentLoaded', () => {
    const socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('connect', () => {
        socket.send('I am connected!');
    });

    socket.on('message', data => {
        const paragraph = document.createElement('p');
        const line = document.createElement('br');

        paragraph.innerHTML = data;

        document.querySelector('#display-message-section').append(paragraph)
    });

    socket.on('some-event', data => {
        console.log(data);
    });

    document.querySelector('#send-message').onclick = () => {
        socket.send(document.querySelector('#user-message').value);
    }
});