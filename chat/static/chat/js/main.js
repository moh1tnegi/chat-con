var roomName = 'online';
var user_online = document.cookie.split('=')[2].split(';')[0];
var full_name = document.cookie.split('=')[3];

if (user_online) {
    var onlineSocket = new WebSocket('wss://' + window.location.host);
    
    onlineSocket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        var uname = data['uname'] + ' - (' + data['full_name'] + ')';
        if (data['uname']) {
            if (data['online']) {
                var sanity_check = {uname: 1};
                var usr_arr = [uname];

                $('#online_users').children().each(function() {
                    usr_arr.push($(this).find('button').text());
                });

                $('#online_users').empty();
                for(var i = 0; i < usr_arr.length; i++) {
                    if(sanity_check[usr_arr[i]]) continue;
                    sanity_check[usr_arr[i]] = 1;

                    $('#online_users').append($('<li>').attr(
                        'class', 'list-group-item list-group-item-primary'
                        ).append($('<button>').attr({
                                type: 'button',
                                class: 'clickable-on round-corn',
                                role: 'button',
                                onclick: 'start_conv(this)'
                            }).text(usr_arr[i])
                        )
                    );
                }
            }
            else {
                var sanity_check = {};
                var usr_arr = [];

                $('#online_users').children().each(function() {
                    var __a = $(this).find('button').text();
                    if(uname.split(' ')[0] != __a.split(' ')[0]) usr_arr.push(__a);
                });

                $('#online_users').empty();
                for(var i = 0; i < usr_arr.length; i++) {
                    if(sanity_check[usr_arr[i]]) continue;
                    sanity_check[usr_arr[i]] = 1;

                    $('#online_users').append($('<li>').attr(
                        'class', 'list-group-item list-group-item-primary'
                        ).append($('<button>').attr({
                                type: 'button',
                                class: 'clickable-on round-corn',
                                role: 'button',
                                onclick: 'start_conv(this)'
                            }).text(usr_arr[i])
                        )
                    );
                }
            }
        }
        else {
            var msg_from = data['from'];
            var msg_to = data['to'];
            var msg = data['txt_msg'];

            if (user_online === msg_to) {
                var chat_area = document.querySelector('#' + msg_from);
                if(!chat_area) {
                    $('#add_new_area').append($('<textarea>').attr({
                            id: msg_from,
                            class: 'text-msg round-corn',
                            disabled: true
                        })
                    );
                    chat_area = document.querySelector('#' + msg_from);
                }

                chat_area.value += msg_from + ': ';
                chat_area.value += msg + '\n\n';
                chat_area.scrollTop = chat_area.scrollHeight;

                if (!$('#' + msg_from).is(':visible')) {
                    if (!document.querySelector('#msgfrom-' + msg_from)) {
                        $('#no-new').hide();
                        $('#show-new').show();
                        $('#new-msgs').append(
                            $('<li>').append(
                                $('<button>').attr({
                                    id: 'msgfrom-' + msg_from,
                                    type: 'button',
                                    class: 'clickable-on round-corn',
                                    role: 'button',
                                    onclick: 'start_conv(this)'
                                }).text(msg_from)
                            ).attr('class', 'list-group-item')
                        );
                    }
                }
            }
        }
    };

    onlineSocket.onopen = function(e) {
        onlineSocket.send(JSON.stringify({
            'user_online' : user_online,
            'full_name' : full_name
        }));
    }

    onlineSocket.onclose = function(e) {
        document.cookie = "username=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        document.cookie = "fullname=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        alert('Something went wrong. Please refresh the page!');
        console.error('Achanak band ho gya bhai!!!');
    };

    document.querySelector('#msg-input').onkeyup = function(key) {
        if (key.keyCode === 13) {
            document.querySelector('#subm-btn').click();
        }
    };

    document.querySelector('#subm-btn').onclick = function(data) {
        var to = document.querySelector('#current_name').innerHTML;
        var text = document.querySelector('#msg-input');
        var chat_area = document.querySelector('#' + to);
        if (text.value.trim()) {
            chat_area.value += 'You: ';
            chat_area.value += text.value + '\n\n';
            onlineSocket.send(JSON.stringify({
                'from': user_online,
                'to': to,
                'text': text.value
            }));
        }
        text.value = '';
        chat_area.scrollTop = chat_area.scrollHeight;
    }

    function start_conv(e) {
        var name = $(e).text().split(' ')[0];
        if(document.querySelector('#' + name)) {
            $('.text-msg').hide();
            $('#' + name).show();
        }
        else {
            $('.text-msg').hide();
            $('#add_new_area').append(
                $('<textarea>').attr({
                    id: name,
                    class: 'text-msg round-corn',
                    disabled: true
                })).show();
        }

        $('#current_name').text(name);
        $('#user-selected').show();
        $('#msg-input').focus();
        $('#no-user-selection').hide();
        $('#msgfrom-' + name).parent().remove();
        if($('#new-msgs').children().length < 3) {
            $('#show-new').hide();
            $('#no-new').show();
        }
    }
}
