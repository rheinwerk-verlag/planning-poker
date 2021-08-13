class BaseConsumer {

  /**
   * Construct a BaseConsumer with the given parameters.
   *
   * @param {Element} container A DOM element containing all other needed elements.
   * @param {string} websocketUrl The url to the websocket to which should be connected.
   */
  constructor(container, websocketUrl) {
    let consumer = this;
    this.container = container;

    this.websocket = new WebSocket(websocketUrl);
    this.websocket.onmessage = function (e) {
      consumer.processMessage(JSON.parse(e.data));
    };

    this.commands = {};
  }

  /**
   * Call the method given by the object with the additional data.
   *
   * @param {Object} message The message containing the event and data.
   */
  processMessage(message) {
    this.commands[message.event](message.data);
  }

  /**
   * Send a message to the websocket with the given event and data.
   *
   * @param {string} event The event which should be triggered on the server's consumer.
   * @param {Object} data An object containing the necessary data to process the message.
   */
  sendMessage(event, data = {}) {
    this.websocket.send(JSON.stringify({
      event: event,
      data: data,
    }));
  }
}

export {BaseConsumer};
