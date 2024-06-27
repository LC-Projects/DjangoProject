$(document).ready(() => {
    const addMessageForm = $('form#add_message_form');
    const listMessages = $('#list-messages');
    const textArea = $('textarea[name="content"]');

    addMessageForm.on('submit', function (event) {
        event.preventDefault();

        const content = textArea.val();
        appendTempMessage(content);

        $.ajax({
            url: $(this).attr('action'),
            type: "POST",
            data: $(this).serialize(),
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: (data) => {
                removeTempMessages();
                if (data.status === 'Valid') {
                    appendValidMessage(data.new_message);
                } else {
                    appendErrorMessage(data.new_message);
                }
            },
            error: (error) => {
                console.error('Error:', error);
            }
        });
    });

    function appendTempMessage(content) {
        listMessages.append(`
            <div class="flex justify-end temp-message">
                <div class="mb-4 bg-gray-600 p-3 rounded-[8px] items-start flex gap-2.5">
                    <div class="flex flex-col w-full  leading-1.5">
                        <div class="flex items-center space-x-2 rtl:space-x-reverse">
                            <span class="text-sm font-semibold text-gray-900 dark:text-white">Me</span>
                            <span class="text-sm font-normal text-gray-500 dark:text-gray-400"></span>
                        </div>
                        <p class="text-sm font-normal py-2 text-gray-900 dark:text-white">${content}</p>
                        <span class="text-sm font-normal text-gray-500 dark:text-gray-400">Loading...</span>
                    </div>
                    <div class="relative h-7 w-7 p-1 rounded-sm text-white flex items-center justify-center bg-black/75 text-opacity-100r">
                        <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 20 20"
                             aria-hidden="true" class="h-4 w-4 text-white" height="1em" width="1em"
                             xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd"
                                  d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
                                  clip-rule="evenodd"></path>
                        </svg>
                    </div>
                </div>
            </div>
        `);
    }

    function removeTempMessages() {
        listMessages.find('.temp-message').remove();
    }

    function appendValidMessage(message) {
        listMessages.append(`
            <div class="flex justify-end">
                <div class="mb-4 bg-gray-600 p-3 rounded-[8px] items-start flex gap-2.5">
                    <div class="flex flex-col w-full  leading-1.5">
                        <div class="flex items-center space-x-2 rtl:space-x-reverse">
                            <span class="text-sm font-semibold text-gray-900 dark:text-white">Me</span>
                            <span class="text-sm font-normal text-gray-500 dark:text-gray-400">${message.create_at}</span>
                        </div>
                        <p class="text-sm font-normal py-2 text-gray-900 dark:text-white">${message.content}</p>
                        <span class="text-sm font-normal text-gray-500 dark:text-gray-400">Delivered</span>
                    </div>
                    <div class="relative h-7 w-7 p-1 rounded-sm text-white flex items-center justify-center bg-black/75 text-opacity-100r">
                        <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 20 20"
                             aria-hidden="true" class="h-4 w-4 text-white" height="1em" width="1em"
                             xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd"
                                  d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
                                  clip-rule="evenodd"></path>
                        </svg>
                    </div>
                </div>
            </div>
        `);
    }

    function appendErrorMessage(message) {
        listMessages.append(`
           <div class="flex justify-end">
                <div class="mb-4 bg-gray-600 p-3 rounded-[8px] items-start flex gap-2.5">
                    <div class="flex flex-col w-full  leading-1.5">
                        <div class="flex items-center space-x-2 rtl:space-x-reverse">
                            <span class="text-sm font-semibold text-gray-900 dark:text-white">Me</span>
                            <span class="text-sm font-normal text-gray-500 dark:text-gray-400">${message.create_at}</span>
                        </div>
                        <p class="text-sm font-normal py-2 text-gray-900 dark:text-white">${message.content}</p>
                        <span class="text-sm font-normal text-gray-500 dark:text-red-400">Error try again</span>
                    </div>
                    <div class="relative h-7 w-7 p-1 rounded-sm text-white flex items-center justify-center bg-black/75 text-opacity-100r">
                        <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 20 20"
                             aria-hidden="true" class="h-4 w-4 text-white" height="1em" width="1em"
                             xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd"
                                  d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
                                  clip-rule="evenodd"></path>
                        </svg>
                    </div>
                </div>
            </div>
        `);
    }
});