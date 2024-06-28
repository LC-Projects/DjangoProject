$(document).ready(() => {

    initDeleteBtn();
    $('#save-chat').on('click', function (e) {
        e.preventDefault();
        const val_name = $('#add-chat-form #name').val();
        const val_category = $('#add-chat-form #categories').val();
        console.log(val_name, val_category)
        if (val_name && val_category) {
            $.ajax({
                url: '/chats/create_chat/',
                type: "POST",
                data: {
                    name: $('#add-chat-form #name').val(),
                    category: parseInt($('#add-chat-form #categories').val()),
                },
                dataType: 'json',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                success: (data) => {
                    $('#add-chat-form #name').val("");
                    $('#add-chat-form #categories').val("");
                    const chat = data.chat;
                    toggleModal();
                    $('.chat-list').append(`
                        <div class="flex justify-between items-center p-4 shadow rounded-lg max-w p-6 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700 mb-8"
                         id="chat-component-${chat.id}">
                        <h2 class="text-xl font-bold text-white">${chat.name} <br> <span class="text-gray-500 text-[14px]">${chat.category}</span></h2>
                        <div class="flex space-x-2">
                            <a class="px-4 py-2 text-white rounded hover:bg-gray-700 border border-sky-500 dark:bg-gray-800"
                               href="${chat.detail_url}"><i
                                    class="fa fa-eye text-sky-500 hover:text-sky-700"></i></a>
                            <a class="px-4 py-2 text-white rounded hover:bg-gray-700 border border-red-500 dark:bg-gray-800 delete-chat-btn"
                               data-id-chat="${chat.id}"><i class="fa fa-trash text-red-500 hover:text-red-700"></i></a>
                        </div>
                    </div>`);
                    initDeleteBtn();
                    showToastSuccess();
                },
                error: (error) => {
                    showToastError();
                }
            });
        } else {
            showToastError();
        }

    });

    let openmodal = document.querySelectorAll(".modal-open");
    for (var i = 0; i < openmodal.length; i++) {
        openmodal[i].addEventListener("click", function (event) {
            event.preventDefault();
            toggleModal();
        });
    }

    const overlay = document.querySelector(".modal-overlay");
    overlay.addEventListener("click", toggleModal);

    let closemodal = document.querySelectorAll(".modal-close");
    for (let i = 0; i < closemodal.length; i++) {
        closemodal[i].addEventListener("click", toggleModal);
    }

    document.onkeydown = function (evt) {
        evt = evt || window.event;
        var isEscape = false;
        if ("key" in evt) {
            isEscape = evt.key === "Escape" || evt.key === "Esc";
        } else {
            isEscape = evt.keyCode === 27;
        }
        if (isEscape && document.body.classList.contains("modal-active")) {
            toggleModal();
        }
    };

    function toggleModal() {
        const body = document.querySelector("body");
        const modal = document.querySelector(".modal");
        modal.classList.toggle("opacity-0");
        modal.classList.toggle("pointer-events-none");
        body.classList.toggle("modal-active");
    }

    // Function to show the toast
    function showToastSuccess() {
        $('#toast-success').removeClass('hidden')
        setTimeout(function () {
            $('#toast-success').addClass('hidden')
        }, 2000);
    }

    function showToastError() {
        $('#toast-error').removeClass('hidden')
        setTimeout(function () {
            $('#toast-error').addClass('hidden')
        }, 2000);
    }

    $('#toast-error button[aria-label="Close"], #toast-success button[aria-label="Close"]').on('click', function () {
        // Hide the toast if hidden class is not present

        if (!$('#toast-error').hasClass('hidden') || !$('#toast-success').hasClass('hidden')){
            $('#toast-error, #toast-success').addClass('hidden');
        }
    });
    function initDeleteBtn() {
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
    }
});