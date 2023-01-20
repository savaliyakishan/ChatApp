const sender_id = JSON.parse(document.getElementById('sender_id').textContent);
const reciver_id = JSON.parse(document.getElementById('reciver_id').textContent);
const socket = new WebSocket(`ws://` + window.location.host + `/ws/jac/${sender_id}/${reciver_id}` + `/`);
socket.onopen = function (e) {
    console.log("[open]");
};


function sendfunction(){
    const messageValue = document.getElementById('message_send_input').value;
    socket.send(JSON.stringify({ 
        'message': messageValue,
        "sender_user_id": sender_id,
        "reciver_user_id":reciver_id}));
        document.getElementById('message_send_input').value = '';
    }


socket.onmessage = function (event) {
    data = JSON.parse(event.data)
    let message = data['message']['message']
    let reciver_group_name = data['message']['reciver_group_name']
    let sender_group_name = data['message']['sender_group_name']
    newMessage(message, reciver_group_name, sender_group_name)
};

function newMessage(message, reciver_group_name, sender_group_name) {
    if ($.trim(message) === '') {
		return false;
	}

    var date = new Date();
    var month = date.toLocaleString('default', { month: 'short' });
    var today_date =  date.getDate()
    var year = date.getFullYear()
    var hours = date.getHours() > 12 ? date.getHours() - 12 : date.getHours();
    var am_pm = date.getHours() >= 12 ? "p.m." : ".a.m.";
    hours = hours < 10 ? "0" + hours : hours;
    var minutes = date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes();
    var seconds = date.getSeconds() < 10 ? "0" + date.getSeconds() : date.getSeconds();
    Sending_Time = month +". " + today_date +", "+ year + " " + hours + ":" + minutes + " " + am_pm;
    

    let message_element;
    let sender_group_name_Check = 'user_chatroom_' + sender_id + '_' + reciver_id
    if(sender_group_name === sender_group_name_Check){
        message_element = `<div class="message  sent ">
            ${message}
            <span class="metadata">
                <span class="time">${Sending_Time}</span><span class="tick"></span>
            </span>
        </div>`
    }else if(reciver_group_name === sender_group_name_Check){
        message_element = `<div class="message  received ">
            ${message}
            <span class="metadata">
                <span class="time">${Sending_Time}</span><span class="tick"></span>
            </span>
        </div>`
    }
    document.getElementById('messagelist').innerHTML += message_element;
    $('#messagelist').scrollTop($('#messagelist')[0].scrollHeight);
}

