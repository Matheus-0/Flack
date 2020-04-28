document.addEventListener('DOMContentLoaded', () => {
    // Use ENTER key to submit message
    let message = document.querySelector('#user-message');

    message.addEventListener('keyup', event => {
        event.preventDefault();

        if (event.keyCode === 13) {
            document.querySelector('#send-message').click();
        }
    });
});