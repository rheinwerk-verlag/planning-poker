import TicketConsumer from "../../planning_poker/assets/js/consumers/ticket-consumer";
import {appendChildrenWithClass} from "../../planning_poker/assets/js/utils";

/**
 * Insert a row with the correct child elements to the given table body.
 *
 * @param {Element} tbody The table body into which the rows should be inserted.
 */
function addRow(tbody) {
    let tr = document.createElement('tr');
    appendChildrenWithClass(tr, [
        ['td', 'field-ticket_number'],
        ['td', 'field-title'],
        ['td', 'field-description']
    ]);
    tr.querySelector('.field-ticket_number').appendChild(document.createElement('input'));
    tr.querySelector('.field-title').appendChild(document.createElement('input'));
    tr.querySelector('.field-description').appendChild(document.createElement('input'));
    tbody.appendChild(tr);
}

/**
 * Add all required elements to the container element.
 *
 * @param {Element} container The container which should contain all required elements.
 */
function setupContainer(container) {
    container.innerHTML = '';
    appendChildrenWithClass(container, [
        ['button', 'search-string-button'],
        ['fieldset', 'module'],
        ['tbody', 'foo'],
        ['tr', 'add-row']
    ]);
    // Setup the table with additional rows.
    let tbody = container.querySelector('tbody');
    container.querySelector('fieldset').appendChild(tbody);
    const numInitialRows = 3;

    for (let i = 0; i < numInitialRows; i++) {
        addRow(tbody);
    }

    let addRowLink = document.createElement('a');
    container.querySelector('.add-row').appendChild(addRowLink);

    let searchStringInput = document.createElement('input');
    searchStringInput.setAttribute('type', 'text');
    searchStringInput.setAttribute('name', 'search-string');
    container.appendChild(searchStringInput);

    let backendNote = document.createElement('div');
    backendNote.classList.add('backend-note');
    backendNote.dataset.resultsText = '%d';
    container.appendChild(backendNote);
}

let container = document.createElement('body');
setupContainer(container);

afterEach(() => {
    setupContainer(container);
});

test('TicketConsumer storiesReceived', () => {
    let ticketConsumer = new TicketConsumer(container, 'ws://test');
    ticketConsumer.websocket.close();
    let tbody = container.querySelector('tbody');
    const mockClick = jest.fn( x => addRow(tbody));
    let addRowButton = container.querySelector('tr.add-row a');
    addRowButton.click = mockClick;
    let stories = [
        {'number': 'TEST-1', 'title': 'write tests for ticketConsumer', 'description': '<b>bold</b>'},
        {'number': 'FIAE-1000', 'title': 'prepare for the final exams', 'description': '<i>italic</i>'}
    ];

    ticketConsumer.storiesReceived({
        'stories': stories
    });

    for (let i = 0; i < stories.length; i++) {
        let child = tbody.children[i];
        expect(child.querySelector('.field-ticket_number').firstElementChild.value).toBe(stories[i].number);
        expect(child.querySelector('.field-title').firstElementChild.value).toBe(stories[i].title);
        expect(child.querySelector('.field-description').firstElementChild.value).toBe(stories[i].description);
    }
    expect(mockClick.mock.calls.length).toBe(stories.length);
    expect(container.querySelector('.backend-note').innerText).toBe(stories.length.toString());
});
