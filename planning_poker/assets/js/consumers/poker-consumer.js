'use strict'

import {BaseConsumer} from './base-consumer.js';

class PokerConsumer extends BaseConsumer {

  /**
   * Construct a PokerConsumer with the given parameters.
   *
   * @param {Element} container A DOM element containing all other needed elements.
   * @param {string} websocketUrl The url to the websocket to which should be connected.
   * @param {string} userId The user's id in the database.
   */
  constructor(container, websocketUrl, userId) {
    super(container, websocketUrl);
    this.container = container;
    this.userId = parseInt(userId);
    this.storyId = null;

    this.commands = {
      'story_changed': this.storyChanged.bind(this),
      'poker_session_ended': this.endPokerSession.bind(this),
      'story_points_submitted': this.storyPointsSubmitted.bind(this),
      'participants_changed': this.updateParticipantsList.bind(this),
    };

    /* istanbul ignore next */
    //The consumer sends out a heartbeat every 20 seconds to let the server know, that the user is still there.
    setInterval(() => {
      this.sendMessage('heartbeat');
    }, 20 * 1000);
  }

  /**
   * Request the next story from the websocket.
   */
  nextStoryRequested(id = null) {
    this.sendMessage('next_story_requested', {'story_id': id});
  }

  /**
   * Request a reset of all votes and hide the moderator's choices.
   */
  resetRequested() {
    this.sendMessage('reset_requested');
  }

  /**
   * Send a message to the websocket containing the chosen amount of story points. And change the moderatorElements
   * accordingly.
   *
   * @param {String} choice Containing the voter's choice.
   */
  submitStoryPoints(choice) {
    this.sendMessage('points_submitted', {'story_points': choice});
    this.nextStoryRequested();
  }

  /**
   * Send a message to the websocket containing the voter's choice.
   *
   * @param {String} choice Containing the voter's choice.
   */
  submitChoice(choice) {
    this.app.userVoted = true;
    this.sendMessage('vote_submitted', {'choice': choice});
  }

  /**
   * Add a badge next to the story with the submitted story points.
   *
   * @param {object} data Containing the amount of the submitted story points
   */
  storyPointsSubmitted(data) {
    let storiesOverview = this.app.$refs.storiesOverview;
    storiesOverview.activeStory.points = (data['story_points']);
  }

  /**
   * Call different methods depending on the user's permissions.
   *
   * @param {Object} data Containing information about the story's id and votes.
   */
  storyChanged(data) {
    let hasUserVoted = this.hasUserVoted(data.votes);
    if (!hasUserVoted && this.app.permissions.vote) {
      this.app.$refs.voteOptions.resetOptions();
      this.app.$refs.storyDetail.resetOverlay();
    }
    if (this.storyId !== data.id) {
      this.storyId = data.id;
      this.app.$refs.storiesOverview.makeActive(data.id);
      this.updateStoryInformation(data['story_label'], data.description);
      if (!this.app.permissions.moderate && hasUserVoted) {
        let choice = Object.keys(data.votes).find((vote) => {
          return data.votes[vote].some((user) => {
            return user.id === this.userId;
          });
        });
        if (choice !== undefined) {
          this.app.$refs.voteOptions.makeChosen({'rank': choice});
        }
      }
    }
    this.updateResults(data.votes);
  }

  /**
   * Update the container's title and description.
   *
   * @param {string} label The story's label.
   * @param {string} description The story's description rendered with html elements.
   */
  updateStoryInformation(label, description) {
    this.app.$refs.storyDetail.title = label;
    this.app.$refs.storyDetail.description = description;
    this.app.$refs.storyDetail.resetOverlay();
  }

  /**
   * Change the resultsContainer's content to display the given votes.
   *
   * @param {Object} votes Containing information about every choice that has votes + who voted for them.
   */
  updateResults(votes) {
    this.app.$refs.voteOverview.votes = votes;
    this.app.userVoted = this.hasUserVoted(votes);
  }

  /**
   * Return True when the user's id appears in the users who have already voted.
   *
   * @param {Object} votes Containing information about every choice that has votes + who voted for them.
   * @returns {boolean} When the user's id appears in the users who have already voted.
   */
  hasUserVoted(votes) {
    return Object.values(votes).some((users) => {
      return users.some((user) => {
        return user.id === this.userId;
      });
    });
  }

  /**
   * Update the displayed list of participants.
   *
   * @param {Object} data Containing a list of all participants and their permissions display.
   */
  updateParticipantsList(data) {
    this.app.$root.$refs.participantsList.participants = data.participants;
    this.app.$refs.voteOverview.participants = data.participants;
  }

  /**
   * End the Poker session by redirecting to the url specified by the event data.
   *
   * @param {Object} data Containing the url to which the user should be redirected.
   */
  endPokerSession(data) {
    window.location.assign(data['poker_session_end_redirect_url']);
  }
}

export {PokerConsumer};
