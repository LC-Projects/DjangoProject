$(document).ready(() => {
    $('.delete-chat-btn').each(function () {
        $(this).on('click', function (e) {
            e.preventDefault();
            const chatId = $(this).data('id-chat');

            $.ajax({
                url: `/chats/delete/`,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                },
                data: {
                    chat_id: parseInt(chatId),
                },
                success: function (data) {
                    if (data.status === 'Valid') {
                        console.log($(`#chat-component-${chatId}`).html())
                        $(`#chat-component-${chatId}`).remove();
                    } else {
                        console.error('Error:', data.message);
                    }
                },
                error: function (error) {
                    console.error('Error:', error);
                }
            });
        });
    });
});