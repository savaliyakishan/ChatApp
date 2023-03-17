document.getElementById("answer").style.display = "none";
document.getElementById("videos").style.display = "none";
document.getElementById("inCall").style.display = "none";
document.getElementById("calling").style.display = "none";


const s_username = JSON.parse(document.getElementById('sender_username').textContent);
const r_username = JSON.parse(document.getElementById('reciver_username').textContent);
let ws_scheme = window.location.protocol == "https:" ? "wss://" : "ws://";

myName = s_username; 
console.log(s_username)
console.log(r_username)
console.log(ws_scheme)
const baseURL = "/"

let localVideo = document.querySelector('#localVideo');
let remoteVideo = document.querySelector('#remoteVideo');
let btnToggleAudio = document.querySelector('#btn_toggle_audio');
let btnToggleVideo = document.querySelector('#btn_toggle_video');
let otherUser;
let remoteRTCMessage;

let iceCandidatesFromCaller = [];
let peerConnection;
let remoteStream;
let localStream;

let callInProgress = false;

let socket;
let callSocket;
function call() {
    let userToCall = r_username;
    otherUser = userToCall;
    console.log(otherUser)
    
    beReady()
    .then(bool => {
        processCall(userToCall)
    })
}
function answer() {
    //do the event firing
    
    beReady()
    .then(bool => {
        processAccept();
    })
    
    document.getElementById("answer").style.display = "none";
}
let pcConfig = {
    "iceServers":
    [
        { "url": "stun:stun.jap.bloggernepal.com:5349" },
        {
            "url": "turn:turn.jap.bloggernepal.com:5349",
            "username": "guest",
            "credential": "somepassword"
            },
            {"url": "stun:stun.l.google.com:19302"}
        ]
    };

    // Set up audio and video regardless of what devices are present.
    let sdpConstraints = {
        offerToReceiveAudio: true,
        offerToReceiveVideo: true
    };
    
    connectSocket()
    function connectSocket() {
        let ws_scheme = window.location.protocol == "https:" ? "wss://" : "ws://";
        callSocket = new WebSocket(`ws://` + window.location.host + `/ws/call/`);
        console.log(ws_scheme);
        
        
    callSocket.onopen = (e) =>{
        callSocket.send(JSON.stringify({
            type: 'login',
            data: {
                name: myName
            }
        }));
    }

    callSocket.onmessage = (e) =>{
        let response = JSON.parse(e.data);

        // console.log(response);

        let type = response.type;

        if(type == 'connection') {
            console.log(response.data.message)
        }

        if(type == 'call_received') {
            // console.log(response);
            onNewCall(response.data)
        }

        if(type == 'call_answered') {
            onCallAnswered(response.data);
        }

        if(type == 'ICEcandidate') {
            onICECandidate(response.data);
        }
    }

    const onNewCall = (data) =>{
        //when other called you
        //show answer button

        otherUser = data.caller;
        remoteRTCMessage = data.rtcMessage

        // document.getElementById("profileImageA").src = baseURL + callerProfile.image;
        document.getElementById("answer").style.display = "block";
    }

    const onCallAnswered = (data) =>{
        //when other accept our call
        remoteRTCMessage = data.rtcMessage
        peerConnection.setRemoteDescription(new RTCSessionDescription(remoteRTCMessage));

        document.getElementById("calling").style.display = "none";

        console.log("Call Started. They Answered");
        // console.log(pc);

        callProgress()
    }

    const onICECandidate = (data) =>{
        // console.log(data);
        console.log("GOT ICE candidate");

        let message = data.rtcMessage

        let candidate = new RTCIceCandidate({
            sdpMLineIndex: message.label,
            candidate: message.candidate
        });

        if (peerConnection) {
            console.log("ICE candidate Added");
            peerConnection.addIceCandidate(candidate);
        } else {
            console.log("ICE candidate Pushed");
            iceCandidatesFromCaller.push(candidate);
        }

    }

}


/**
 * 
 * @param {Object} data 
 * @param {number} data.name - the name of the user to call
 * @param {Object} data.rtcMessage - the rtc create offer object
 */
function sendCall(data) {
    //to send a call
    console.log("Send Call");
    var call = JSON.stringify({type: 'call',data})
    // socket.emit("call", data);
    callSocket?.send(call);

    document.getElementById("otherUserNameCA").innerHTML = otherUser;
    document.getElementById("calling").style.display = "block";
}



/**
 * 
 * @param {Object} data 
 * @param {number} data.caller - the caller name
 * @param {Object} data.rtcMessage - answer rtc sessionDescription object
 */
function answerCall(data) {
    //to answer a call
    // socket.emit("answerCall", data);
    var answer = JSON.stringify({
        type: 'answer_call',
        data
    })
    callSocket?.send(answer);
    callProgress();
}

/**
 * 
 * @param {Object} data 
 * @param {number} data.user - the other user //either callee or caller 
 * @param {Object} data.rtcMessage - iceCandidate data 
 */
function sendICEcandidate(data) {
    //send only if we have caller, else no need to
    var iceCandidate = JSON.stringify({
        type: 'ICEcandidate',
        data
    })
    callSocket?.send(iceCandidate);

}

function beReady() {
    return navigator.mediaDevices.getUserMedia({
        audio: true,
        video: true
    })
        .then(stream => {
            localStream = stream;
            localVideo.srcObject = stream;
            localVideo.muted = true

            var audioTracks = stream.getAudioTracks();
            var videoTracks = stream.getVideoTracks();
            console.log(audioTracks);
            audioTracks[0].enabled = true
            videoTracks[0].enabled = true

            btnToggleAudio.addEventListener('click', () =>{
                audioTracks[0].enabled = !audioTracks[0].enabled;
                if(audioTracks[0].enabled) {
                    btnToggleAudio.innerHTML = "Audio Mute";
                    return 
                } 
                btnToggleAudio.innerHTML = "Audio Unmute";
            });

            btnToggleVideo.addEventListener('click', () =>{
                videoTracks[0].enabled = !videoTracks[0].enabled;
                if(videoTracks[0].enabled) {
                    btnToggleVideo.innerHTML = "Video Off";
                    return 
                } 
                btnToggleVideo.innerHTML = "video on";
            });
            return createConnectionAndAddStream()
        })
        .catch(function (e) {
            alert('getUserMedia() error: ' + e.name);
        });
}

function createConnectionAndAddStream() {
    createPeerConnection();
    peerConnection.addStream(localStream);
    return true;
}

function processCall(userName) {
    peerConnection.createOffer((sessionDescription) => {
        peerConnection.setLocalDescription(sessionDescription);
        sendCall({
            name: userName,
            rtcMessage: sessionDescription
        })
    }, (error) => {
        console.log("Error");
    });
}

function processAccept() {

    peerConnection.setRemoteDescription(new RTCSessionDescription(remoteRTCMessage));
    peerConnection.createAnswer((sessionDescription) => {
        peerConnection.setLocalDescription(sessionDescription);

        if (iceCandidatesFromCaller.length > 0) {
            for (let i = 0; i < iceCandidatesFromCaller.length; i++) {
                let candidate = iceCandidatesFromCaller[i];
                console.log("ICE candidate Added From queue");
                try {
                    peerConnection.addIceCandidate(candidate).then(done => {
                        console.log(done);
                    }).catch(error => {
                        console.log(error);
                    })
                } catch (error) {
                    console.log(error);
                }
            }
            iceCandidatesFromCaller = [];
            console.log("ICE candidate queue cleared");
        } else {
            console.log("NO Ice candidate in queue");
        }

        answerCall({
            caller: otherUser,
            rtcMessage: sessionDescription
        })

    }, (error) => {
        console.log("Error");
    })
}


function createPeerConnection() {
    try {
        peerConnection = new RTCPeerConnection(pcConfig);
        peerConnection.onicecandidate = handleIceCandidate;
        peerConnection.onaddstream = handleRemoteStreamAdded;
        peerConnection.onremovestream = handleRemoteStreamRemoved;
        console.log('Created RTCPeerConnnection');
        return;
    } catch (e) {
        console.log('Failed to create PeerConnection, exception: ' + e.message);
        alert('Cannot create RTCPeerConnection object.');
        return;
    }
}

function handleIceCandidate(event) {
    if (event.candidate) {
        console.log("Local ICE candidate");
        sendICEcandidate({
            user: otherUser,
            rtcMessage: {
                label: event.candidate.sdpMLineIndex,
                id: event.candidate.sdpMid,
                candidate: event.candidate.candidate
            }
        })

    } else {
        console.log('End of candidates.');
    }
}

function handleRemoteStreamAdded(event) {
    console.log('Remote stream added.');
    remoteStream = event.stream;
    remoteVideo.srcObject = remoteStream;
}

function handleRemoteStreamRemoved(event) {
    console.log('Remote stream removed. Event: ', event);
    remoteVideo.srcObject = null;
    localVideo.srcObject = null;
}

window.onbeforeunload = function () {
    if (callInProgress) {
        stop();
    }
};

function callProgress() {
    document.getElementById("videos").style.display = "block";
    document.getElementById("otherUserNameC").innerHTML = otherUser;
    document.getElementById("inCall").style.display = "block";

    callInProgress = true;
}

function stop() {
    localStream.getTracks().forEach(track => track.stop());
    callInProgress = false;
    peerConnection.close();
    peerConnection = null;
    document.getElementById("answer").style.display = "none";
    document.getElementById("videos").style.display = "none";
    document.getElementById("inCall").style.display = "none";
    document.getElementById("calling").style.display = "none";
    document.getElementById("remoteVideoDiv").style.display = "none";
    otherUser = null;
    console.log(otherUser)

    
}
