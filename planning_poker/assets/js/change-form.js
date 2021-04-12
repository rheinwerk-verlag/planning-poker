import TicketConsumer from './consumers/ticket-consumer';

let host = JSON.parse(document.getElementById('host').textContent);

new TicketConsumer(document.body.querySelector('#content-main'), `ws://${host}/admin/poker_session`);