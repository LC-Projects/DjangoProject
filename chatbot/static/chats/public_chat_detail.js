$(document).ready(() => {
    console.log('Public chat detail page');
    const addCommentsForm = $('form#add_comment_form');
    const listComments = $('#list-comments');

    $(addCommentsForm).find('button[type="submit"]').on('click', function (event) {
        event.preventDefault();

        const comment_content = $(addCommentsForm).find('textarea[name="comment"]').val();
        console.log(comment_content);
        if (comment_content !== "") {
            if (userId === 0) {
                document.location.href = auth_link;
            }

            $.ajax({
                url: '/chats/add_comment/',
                type: "POST",
                data: {
                    comment: comment_content,
                    user: userId,
                    chat: chatId
                },
                dataType: 'json',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                success: (data) => {
                    if (data.status === 'Valid') {
                        appendComment(data.new_comment);
                    } else {
                        alert('Invalid data');
                    }
                },
                error: (error) => {
                    console.error('Error:', error);
                }
            });
        }
    });

    function appendComment(data) {
        listComments.append(`
            <article class="p-6 text-base bg-white border-t border-gray-200 dark:border-gray-700 dark:bg-gray-900">
                    <footer class="flex justify-between items-center mb-2">
                        <div class="flex items-center">
                            <p class="inline-flex items-center mr-3 text-sm text-gray-900 dark:text-white font-semibold">
                                <img
                                        class="mr-2 w-6 h-6 rounded-full"
                                        src="https://flowbite.com/docs/images/people/profile-picture-4.jpg"
                                        alt="Helene Engels">${data.username}</p>
                            <p class="text-sm text-gray-600 dark:text-gray-400">
                                <time pubdate datetime="2022-06-23"
                                      title="${data.created_at}">${data.created_at}
                                </time>
                            </p>
                        </div>
                    </footer>
                    <p class="text-gray-500 dark:text-gray-400">${data.content}</p>
                </article>
        `);
    }
});