import {shallowMount} from '@vue/test-utils';

import ParticipantsList from '../../../planning_poker/assets/js/components/ParticipantsList.vue';

describe('ParticipantsList', () => {
  const mocks = {
    $t: jest.fn(x => x)
  };

  const wrapper = shallowMount(ParticipantsList, {
    mocks: mocks
  });

  const participants = [
    {id: 1, username: 'Bob', permissions: ['planning_poker.vote']},
    {id: 2, username: 'Ross', permissions: ['planning_poker.vote']}
  ];

  describe('Tooltip', () => {
    let tests = [
      {
        'testName': `doesn't display when the participants list is empty`,
        'participants': [],
        'event': 'mouseover',
        'displayTooltip': true,
        'tooltipHandler': 'toThrow',
      },
      {
        'testName': `doesn't display when the mouse left the component previously`,
        'participants': participants,
        'event': 'mouseleave',
        'displayTooltip': false,
        'tooltipHandler': 'toThrow',
      },
      {
        'testName': 'displays when the participants list is filled',
        'participants': participants,
        'event': 'mouseover',
        'displayTooltip': true,
        'tooltipHandler': 'toBeTruthy',
      },
    ];

    tests.forEach(test => {
      it(test['testName'], async () => {
        wrapper.vm.participants = test['participants'];
        wrapper.trigger(test['event']);
        await wrapper.vm.$nextTick();
        expect(wrapper.vm.displayTooltip).toEqual(test['displayTooltip']);
        expect(() => wrapper.get('.participants-list .participants-tooltip'))[test['tooltipHandler']]();
      });
    });
  });

  describe('permissionsDisplay', () => {
    let tests = [
      {
        'testName': 'is empty when the user has no permissions',
        'user': {
          'username': 'spectator',
          'permissions': [],
        },
        'expectedValue': '',
      },
      {
        'testName': `returns '(Voter)' when the user has the vote permission`,
        'user': {
          'username': 'voter',
          'permissions': ['planning_poker.vote'],
        },
        'expectedValue': '(Voter)',
      },
      {
        'testName': `returns '(Moderator)' when the user has the moderate permission`,
        'user': {
          'username': 'moderator',
          'permissions': ['planning_poker.moderate'],
        },
        'expectedValue': '(Moderator)',
      },
      {
        'testName': `returns '(Moderator, Voter)' when the user has the moderate and vote permission`,
        'user': {
          'username': 'superuser',
          'permissions': ['planning_poker.vote', 'planning_poker.moderate'],
        },
        'expectedValue': '(Moderator, Voter)',
      },
    ];

    tests.forEach(test => {
      it(test['testName'], () => {
        expect(wrapper.vm.permissionsDisplay(test['user'])).toEqual(test['expectedValue']);
      });
    });
  });
});
