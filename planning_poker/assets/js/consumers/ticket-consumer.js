import BaseConsumer from "./base-consumer.js";

class TicketConsumer extends BaseConsumer {
    /**
     * Construct a TicketConsumer with the given parameters.
     *
     * @param {Element} container A DOM element containing all other needed elements.
     * @param {string} websocketURL The url to the websocket to which should be connected.
     */
    constructor(container, websocketURL) {
        super(container, websocketURL);
        let consumer = this;

        this.searchStringText = this.container.querySelector('#id-search-string');
        this.searchButton = this.container.querySelector('.search-string-button');
        this.backendNote = this.container.querySelector('.backend-note');

        this.searchButton.addEventListener('click', function () {
            consumer.backendNote.innerText = consumer.backendNote.dataset.loadingText;
            consumer.sendMessage('stories_requested',
                {
                    'search_string': consumer.searchStringText.value
                });
        });

        this.commands = {
            'stories_received': this.storiesReceived.bind(this),
        };
    }

    /**
     * Fill in the Story inlines with the stories from the given data.
     *
     * @param data Containing information about the stories.
     */
    storiesReceived(data) {
        let tbody = this.container.querySelector('.module tbody');

        let addRow = this.container.querySelector('tr.add-row a');

        if (data.stories.length > 0) {
            this.backendNote.innerText = this.backendNote.dataset.resultsText
                .replace('%d', data.stories.length.toString());
            data.stories.forEach(story => {
                let tr = tbody.children[tbody.children.length - 3];
                tr.querySelector('.field-ticket_number').firstElementChild.value = story.number;
                tr.querySelector('.field-title').firstElementChild.value = story.title;
                tr.querySelector('.field-description').firstElementChild.value = story.description;
                addRow.click();
            });
        } else {
            this.backendNote.innerText = this.backendNote.dataset.noResultsText;
        }
    }
}

export default TicketConsumer