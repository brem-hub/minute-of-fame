import Socket from './socket.js'
import Stream from './stream.js'
import PacketHandler from './handlers/packet_handler.js'
import VotingHandler from './handlers/voting_handler.js'
import StreamHandler from './handlers/stream_handler.js'
import QueueHandler from './handlers/queue_handler.js'
import ChatHandler from "./handlers/chat_handler";

$(document).ready(function () {
    console.log('Starting connecting')
    let socket = new Socket();
    socket.connect();

    socket.socket.onopen = (e) => {
        console.log('socket open')
        let stream = new Stream((cmd, p) => socket.send("stream", cmd, p));
        window.stream = stream;
        let packet_handler = new PacketHandler({
            'poll': new VotingHandler(socket),
            'queue': new QueueHandler(socket, stream),
            'chat': new ChatHandler(socket),
            'stream': new StreamHandler(socket, stream)
        });
        packet_handler.bind_handlers(socket);

        socket.onpacket = packet_handler.handle_packet.bind(packet_handler);
    }


});


grecaptcha.ready(function() {
    console.log('recapcha ready')
  $('#register_btn').click(function(e){
      var form = this;
      e.preventDefault()
      grecaptcha.execute('6Lc3K-MUAAAAAJM2Ho9U4tiTIZp-A9PPeGIyyw5z', {action: 'register_form'}).then(function(token) {
            console.log(token);
            console.log(document.getElementById("add_form"));
          $('#recaptcha').val(token);
          $('#register_form').submit()
      });
  })
});