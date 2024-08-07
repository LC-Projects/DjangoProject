$(document).ready(() => {
    let reader = new commonmark.Parser();
    let writer = new commonmark.HtmlRenderer();
    const addMessageForm = $('form#add_message_form');
    const listMessages = $('#list-messages');
    const textArea = $('textarea[name="content"]');


    addMessageForm.on('submit', sendMessage);
    addMessageForm.on('keydown', function (event) {
        if (event.key === 'Enter' && event.ctrlKey && !event.shiftKey) {
            event.preventDefault();
            sendMessage(event);
        }
    });

    function sendMessage(event) {
        event.preventDefault();

        const form = $('#add_message_form'); // Assuming the form has an ID 'addMessageForm'
        const textArea = form.find('textarea');

        const content = textArea.val();
        appendTempMessage(content);
        scrollBottom();

        $.ajax({
            url: form.attr('action'),
            type: "POST",
            data: form.serialize(),
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: (data) => {
                removeTempMessages();
                if (data.status === 'Valid') {
                    appendValidMessage(data.new_message);
                    appendValidBotMessage(data.bot_response);
                    scrollBottom();
                    textArea.val('');
                } else {
                    appendErrorMessage(data.new_message);
                }
            },
            error: (error) => {
                console.error('Error:', error);
            }
        });
    }

    // addMessageForm.on('submit', function (event) {
    //     event.preventDefault();

    //     const content = textArea.val();
    //     appendTempMessage(content);
    //     scrollBottom();

    //     $.ajax({
    //         url: $(this).attr('action'),
    //         type: "POST",
    //         data: $(this).serialize(),
    //         dataType: 'json',
    //         headers: {
    //             'X-CSRFToken': csrftoken
    //         },
    //         success: (data) => {
    //             removeTempMessages();
    //             if (data.status === 'Valid') {
    //                 appendValidMessage(data.new_message);
    //                 appendValidBotMessage(data.bot_response);
    //                 scrollBottom();
    //                 $(textArea).val('');
    //             } else {
    //                 appendErrorMessage(data.new_message);
    //             }
    //         },
    //         error: (error) => {
    //             console.error('Error:', error);
    //         }
    //     });
    // });


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
                            <span class="text-sm font-normal text-gray-500 dark:text-gray-400">${message.created_at}</span>
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
                            <span class="text-sm font-normal text-gray-500 dark:text-gray-400">${message.created_at}</span>
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

    function appendValidBotMessage(message) {
        console.log('===>', message);
        let parsed = reader.parse(message.content);
        let message_content = writer.render(parsed);
        console.log('--->', message_content);
        // message_content contains code block add the class hljs

        listMessages.append(`
            <div class="flex items-start">
                <div class="bg-gray-500 rounded-[8px] p-3 mb-4  gap-2.5 flex items-start">
                    <div class="relative h-7 w-7 p-1 rounded-sm text-white flex items-center justify-center bg-black/75 text-opacity-100r">
                        <svg stroke="currentColor" fill="currentColor" stroke-width="0" role="img"
                             viewBox="0 0 24 24" class="h-4 w-4 text-white" height="1em" width="1em"
                             xmlns="http://www.w3.org/2000/svg"><title></title>
                            <path d="M22.2819 9.8211a5.9847 5.9847 0 0 0-.5157-4.9108 6.0462 6.0462 0 0 0-6.5098-2.9A6.0651 6.0651 0 0 0 4.9807 4.1818a5.9847 5.9847 0 0 0-3.9977 2.9 6.0462 6.0462 0 0 0 .7427 7.0966 5.98 5.98 0 0 0 .511 4.9107 6.051 6.051 0 0 0 6.5146 2.9001A5.9847 5.9847 0 0 0 13.2599 24a6.0557 6.0557 0 0 0 5.7718-4.2058 5.9894 5.9894 0 0 0 3.9977-2.9001 6.0557 6.0557 0 0 0-.7475-7.0729zm-9.022 12.6081a4.4755 4.4755 0 0 1-2.8764-1.0408l.1419-.0804 4.7783-2.7582a.7948.7948 0 0 0 .3927-.6813v-6.7369l2.02 1.1686a.071.071 0 0 1 .038.052v5.5826a4.504 4.504 0 0 1-4.4945 4.4944zm-9.6607-4.1254a4.4708 4.4708 0 0 1-.5346-3.0137l.142.0852 4.783 2.7582a.7712.7712 0 0 0 .7806 0l5.8428-3.3685v2.3324a.0804.0804 0 0 1-.0332.0615L9.74 19.9502a4.4992 4.4992 0 0 1-6.1408-1.6464zM2.3408 7.8956a4.485 4.485 0 0 1 2.3655-1.9728V11.6a.7664.7664 0 0 0 .3879.6765l5.8144 3.3543-2.0201 1.1685a.0757.0757 0 0 1-.071 0l-4.8303-2.7865A4.504 4.504 0 0 1 2.3408 7.872zm16.5963 3.8558L13.1038 8.364 15.1192 7.2a.0757.0757 0 0 1 .071 0l4.8303 2.7913a4.4944 4.4944 0 0 1-.6765 8.1042v-5.6772a.79.79 0 0 0-.407-.667zm2.0107-3.0231l-.142-.0852-4.7735-2.7818a.7759.7759 0 0 0-.7854 0L9.409 9.2297V6.8974a.0662.0662 0 0 1 .0284-.0615l4.8303-2.7866a4.4992 4.4992 0 0 1 6.6802 4.66zM8.3065 12.863l-2.02-1.1638a.0804.0804 0 0 1-.038-.0567V6.0742a4.4992 4.4992 0 0 1 7.3757-3.4537l-.142.0805L8.704 5.459a.7948.7948 0 0 0-.3927.6813zm1.0976-2.3654l2.602-1.4998 2.6069 1.4998v2.9994l-2.5974 1.4997-2.6067-1.4997Z"></path>
                        </svg>
                    </div>
                    <div class="flex flex-col w-full  leading-1.5">
                        <div class="flex items-center space-x-2 rtl:space-x-reverse">
                            <span class="text-sm font-semibold text-gray-900 dark:text-white">GPT-Bot</span>
                            <span class="text-sm font-normal text-gray-500 dark:text-gray-400">${message.created_at}</span>
                        </div>
                        <div class="text-sm font-normal py-2 text-white">${message_content}</div>
                        <span class="text-sm font-normal text-gray-500 dark:text-gray-400">Delivered</span>
                    </div>
                </div>
            </div>
        `);
        hljs.highlightAll();
    }

    scrollBottom();

    function scrollBottom() {
        $('main > div').animate({ scrollTop: $('main > div').prop("scrollHeight") }, 1000);
    }
});