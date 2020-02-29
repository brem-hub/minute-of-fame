let connection = new RTCMultiConnection();
// v3.4.7 or newer
connection.socketURL = 'http://' + location.hostname + ':9001/';
connection.videosContainer = document.getElementById('stream-box');

let user_room_id = document.getElementById('user_room_id');

function screen_stream() {
    connection.session = {
        screen: true,
        oneway: true
    };

    connection.sdpConstraints.mandatory = {
        OfferToReceiveAudio: false,
        OfferToReceiveVideo: false
    };
    connection.openOrJoin(user_room_id.value.toString());
}

function webcam_stream() {

    navigator.getMedia = (navigator.getUserMedia || // use the proper vendor prefix
        navigator.webkitGetUserMedia ||
        navigator.mozGetUserMedia ||
        navigator.msGetUserMedia);

    navigator.getMedia({video: true, audio: true}, function () {
        // webcam is available
        alert("Microphone or webcam are connected with your system");
        connection.session = {
            audio: true,
            video: true
        };

        connection.sdpConstraints.mandatory = {
            OfferToReceiveAudio: true,
            OfferToReceiveVideo: true
        };
        connection.openOrJoin(user_room_id.value.toString());

    }, function () {
        // webcam is not available
        alert("Microphone or webcam are not connected with your system");

    });
}

function stopStream() {
    connection.getAllParticipants().forEach(function (pid) {
        connection.disconnectWith(pid);
    });

    // stop all local cameras
    connection.attachStreams.forEach(function (localStream) {
        localStream.stop();
    });

    // close socket.io connection
    connection.closeSocket();
}

function watchStream() {
    let input_room_id = document.getElementById('input_room_id');

    connection.checkPresence(input_room_id.value.toString(), function (isRoomExist, room_id) {
        if (isRoomExist === true) {

            connection.session = {
                data: true
            };

            connection.sdpConstraints.mandatory = {
                OfferToReceiveAudio: true,
                OfferToReceiveVideo: true
            };
            connection.join(room_id);
        } else {
            alert('Такой комнаты не существует!');
        }
    });

}