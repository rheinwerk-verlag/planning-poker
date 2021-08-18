import Vue from 'vue';

import {createJsonElement} from '../../planning_poker/assets/js/utils.js';
import {PokerConsumer} from '../../planning_poker/assets/js/consumers/poker-consumer.js';
import PokerSite from '../../planning_poker/assets/js/components/PokerSite.vue';

describe('PokerConsumer', () => {
  document.body.innerHTML = '<PokerSite id="planning_poker-container"></PokerSite>';

  createJsonElement({
    non_point_options: [['A', 'A'], ['B', 'B']],
    point_options: [['1', '1'], ['2', '2'], ['3', '3'], ['5', '5']],
  }, 'options');

  createJsonElement([...Array(5).keys()].map(i => {
    let j = i + 1;
    return {id: j, story_label: `Story ${j}`, description: `<p>Description of Story #${j}</p>`};
  }), 'initial-stories');

  createJsonElement({moderate: false, vote: true}, 'permissions');

  let pokerConsumer = new PokerConsumer(document.body, 'ws://test', '1');
  pokerConsumer.websocket.close();

  Vue.prototype.$t = jest.fn();
  Vue.prototype.$interpolate = jest.fn();
  Vue.prototype.$consumer = pokerConsumer;

  let app = new Vue({
    el: '#planning_poker-container',
    render: h => h(PokerSite),
  });

  pokerConsumer.app = app.$children[0];
  pokerConsumer.app.$refs.storiesOverview.activeStory = {id: 1337, title: 'Story #1337', description: '<p>foo</p>'};
  pokerConsumer.app.$root = {
    '$refs': {
      'participantsList': {
        'participants': [],
      },
    },
  };

  const storiesOverview = pokerConsumer.app.$refs.storiesOverview;
  const voteOptions = pokerConsumer.app.$refs.voteOptions;
  const voteOverview = pokerConsumer.app.$refs.voteOverview;

  describe('sets the points of the currently active story', () => {
    let mockNextStoryRequested = jest.fn();
    pokerConsumer.nextStoryRequested = mockNextStoryRequested;
    it('and changes the active story to the first story in the upcoming stories list', () => {
      pokerConsumer.storyPointsSubmitted({'story_points': '3'});
      expect(storiesOverview.activeStory.id).toEqual(1);
      let lastPreviousStories = storiesOverview.previousStories[storiesOverview.previousStories.length - 1];
      expect(lastPreviousStories.points).toEqual('3');
      expect(lastPreviousStories.id).toEqual(1337);
      expect(mockNextStoryRequested.mock.calls[0]).toEqual([1]);
    });

    it('and calls nextStoryRequested with no parameters when the list of upcoming stories is empty', () => {
      storiesOverview.upcomingStories = [];
      pokerConsumer.storyPointsSubmitted({'story_points': '3'});
      expect(mockNextStoryRequested.mock.calls[1]).toEqual([]);
    });
  });

  describe('storyChanged', () => {
    it(`doesn't remove the user's choice when they haven't voted.`, () => {
      let story = {id: 3, title: 'Story 3', description: '<p>Description of Story #3</p>'};
      const data = {
        id: story.id,
        title: story.title,
        description: story.description,
        votes: {3: [{id: 20, name: 'Thorsten'}]},
      };
      storiesOverview.upcomingStories = [story];
      pokerConsumer.storyChanged(data);

      expect(pokerConsumer.storyId).toEqual(3);
      expect(storiesOverview.activeStory.id).toEqual(3);
      expect(voteOptions.options['point_options']).toContainEqual(['3', '3']);
    });

    it(`removes the user's choice when they have voted.`, () => {
      let story = {id: 2, title: 'Story 2', description: '<p>Description of Story #2</p>'};
      const data = {
        id: story.id,
        title: story.title,
        description: story.description,
        votes: {3: [{id: 1, name: 'Thorsten'}]},
      };
      storiesOverview.upcomingStories = [story];
      pokerConsumer.storyChanged(data);

      expect(pokerConsumer.storyId).toEqual(2);
      expect(storiesOverview.activeStory.id).toEqual(2);
      expect(voteOptions.options['point_options']).not.toContainEqual(['3', '3']);
    });

    it(`doesn't remove the choice if it couldn't be found in the vote options.`, () => {
      let story = {id: 4, title: 'Story 4', description: '<p>Description of Story #4</p>'};
      const data = {
        id: story.id,
        title: story.title,
        description: story.description,
        votes: {5: [{id: 1, name: 'Thorsten'}]},
      };
      let hasUserVotedSpy = jest.spyOn(pokerConsumer, 'hasUserVoted').mockImplementation(() => true);
      let removeOptionSpy = jest.spyOn(voteOptions, 'removeOption');
      let setupOverlaySpy = jest.spyOn(pokerConsumer.app.$refs.storyDetail, 'setupOverlay');
      pokerConsumer.userId = 2;
      storiesOverview.upcomingStories = [story];
      pokerConsumer.storyChanged(data);

      expect(removeOptionSpy).not.toHaveBeenCalled();
      expect(setupOverlaySpy).not.toHaveBeenCalled();
      hasUserVotedSpy.mockRestore();
      removeOptionSpy.mockRestore();
      setupOverlaySpy.mockRestore();
    });

    it(`doesn't change the story if it is already active`, () => {
      let story = {id: 1, title: 'Story 1', description: '<p>Description of Story #1</p>'};
      pokerConsumer.storyId = story.id;
      const data = {
        id: story.id,
        title: story.title,
        description: story.description,
        votes: {3: [{id: 1, name: 'Thorsten'}]},
      };
      let makeActiveSpy = jest.spyOn(storiesOverview, 'makeActive');
      let updateStoryInformationSpy = jest.spyOn(pokerConsumer, 'updateStoryInformation');
      pokerConsumer.storyChanged(data);
      expect(makeActiveSpy).not.toHaveBeenCalled();
      expect(updateStoryInformationSpy).not.toHaveBeenCalled();

      makeActiveSpy.mockRestore();
      updateStoryInformationSpy.mockRestore();
    });
  });

  it('updateStoryInformation renders the correct data', async () => {
    pokerConsumer.updateStoryInformation('Some Title', '<b>Some description</b>');
    await pokerConsumer.app.$nextTick;
    expect(document.body.querySelector('h2.story-label').innerHTML).toEqual('<!---->Some Title');
    expect(document.body.querySelector('div.description-text').innerHTML).toEqual('<b>Some description</b>');
  });

  it('updateResults updates the results correctly', () => {
    pokerConsumer.userId = 1;
    let votes = {3: [{id: 1, name: 'Thorsten'}, {id: 58, name: 'Franz'}], 13: [{id: 42, name: 'Otto'}]};
    pokerConsumer.updateResults(votes);

    expect(voteOverview.votes).toEqual(votes);
    expect(pokerConsumer.app.userVoted).toEqual(true);
  });

  it('determines whether the user has already voted or not correctly', () => {
    pokerConsumer.userId = 1;
    let votes = {3: [{id: 1, name: 'Thorsten'}, {id: 58, name: 'Franz'}], 13: [{id: 42, name: 'Otto'}]};
    expect(pokerConsumer.hasUserVoted(votes)).toEqual(true);
    votes[3][0].id = 11;
    expect(pokerConsumer.hasUserVoted(votes)).toEqual(false);
  });

  describe('nextStoryRequested sends the correct message', () => {
    let pokerConsumer = new PokerConsumer(document.body, 'ws://test', '1');
    pokerConsumer.websocket.close();

    pokerConsumer.sendMessage = jest.fn();
    pokerConsumer.nextStoryRequested();
    expect(pokerConsumer.sendMessage).toHaveBeenLastCalledWith('next_story_requested', {'story_id': null});
    pokerConsumer.nextStoryRequested(3);
    expect(pokerConsumer.sendMessage).toHaveBeenLastCalledWith('next_story_requested', {'story_id': 3});
  });

  describe('resetRequested sends the correct message', () => {
    pokerConsumer.sendMessage = jest.fn();
    pokerConsumer.resetRequested();
    expect(pokerConsumer.sendMessage).toHaveBeenLastCalledWith('reset_requested');
  });

  describe('submitStoryPoints sends the correct message', () => {
    pokerConsumer.sendMessage = jest.fn();
    pokerConsumer.submitStoryPoints('3');
    expect(pokerConsumer.sendMessage).toHaveBeenLastCalledWith('points_submitted', {'story_points': '3'});
  });

  describe('submitChoice sends the correct message', () => {
    pokerConsumer.sendMessage = jest.fn();
    pokerConsumer.app.userVoted = false;
    pokerConsumer.submitChoice('3');
    expect(pokerConsumer.app.userVoted).toEqual(true);
    expect(pokerConsumer.sendMessage).toHaveBeenLastCalledWith('vote_submitted', {'choice': '3'});
  });

  describe('updateParticipantsList correctly updates the list of participants', () => {
    let participants = [
      {id: 1, name: 'foo', permissions: ['planning_poker.vote']},
      {id: 2, name: 'bar', permissions: ['planning_poker.moderate']},
    ];
    pokerConsumer.updateParticipantsList({participants: participants});
    expect(pokerConsumer.app.$root.$refs.participantsList.participants).toEqual(participants);
    expect(voteOverview.participants).toEqual(participants);
  });

  describe('endPokerSession correctly redirects the participants', () => {
    delete window.location;
    window.location = {assign: jest.fn()};
    pokerConsumer.endPokerSession({poker_session_end_redirect_url: 'https://test-page.com'});
    expect(window.location.assign).toHaveBeenLastCalledWith('https://test-page.com');
  });
});
