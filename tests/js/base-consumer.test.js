import {BaseConsumer} from '../../planning_poker/assets/js/consumers/base-consumer.js';

let container = document.createElement('body');

test('BaseConsumer sendMessage', () => {
    let baseConsumer = new BaseConsumer(container, 'ws://test');
    baseConsumer.websocket.close();
    const mockSend = jest.fn();

    baseConsumer.websocket.send = mockSend;
    baseConsumer.sendMessage('event', {'some': 'data'});

    expect(mockSend.mock.calls[0][0]).toBe('{"event":"event","data":{"some":"data"}}');
});

test('BaseConsumer sendMessage no data parameter', () => {
    let baseConsumer = new BaseConsumer(container, 'ws://test', '1');
    baseConsumer.websocket.close();
    const mockSend = jest.fn();

    baseConsumer.websocket.send = mockSend;
    baseConsumer.sendMessage('event');

    expect(mockSend.mock.calls[0][0]).toBe('{"event":"event","data":{}}');
});

test('BaseConsumer processMessage', () => {
    let baseConsumer = new BaseConsumer(container, 'ws://test', '1');
    baseConsumer.websocket.close();
    const mockCommand = jest.fn();
    baseConsumer.commands = {
        'mock_event': mockCommand
    };

    baseConsumer.processMessage({'event': 'mock_event', 'data': {'some': 'data'}});

    expect(mockCommand.mock.calls[0][0]).toStrictEqual({'some': 'data'});
});
