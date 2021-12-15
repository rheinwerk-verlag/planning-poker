import Vue from 'vue';

import Navbar from './components/Navbar.vue';
import ParticipantsList from './components/ParticipantsList.vue';
import PokerSite from './components/PokerSite.vue';
import {PokerConsumer} from './consumers/poker-consumer.js';


let host = JSON.parse(document.getElementById('host').textContent);
let pokerSessionId = JSON.parse(document.getElementById('pokersession-id').textContent);
let userId = JSON.parse(document.getElementById('user-id').textContent);

Vue.prototype.$t = window.gettext;
Vue.prototype.$interpolate = window.interpolate;

let app = new Vue({
  el: '#app',
  components: {
    Navbar,
    PokerSite,
    ParticipantsList
  },
});

let ws_scheme = window.location.protocol === 'https:' ? 'wss' : 'ws';

Vue.prototype.$consumer = new PokerConsumer(
  document.body.querySelector('#app'), `${ws_scheme}://${host}/poker/${pokerSessionId}/`, userId
);

//Find the PokerSite component, which has access to the different $refs of the other components.
Vue.prototype.$consumer.app = app.$children.find(child => child.$options._componentTag === 'poker-site');
