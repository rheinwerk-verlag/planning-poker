import {shallowMount} from '@vue/test-utils';

import {createJsonElement} from '../../../planning_poker/assets/js/utils.js';

import PokerSite from '../../../planning_poker/assets/js/components/PokerSite.vue';
import StoryDetail from '../../../planning_poker/assets/js/components/StoryDetail.vue';
import StoriesOverview from '../../../planning_poker/assets/js/components/StoriesOverview.vue';
import VoteOptions from '../../../planning_poker/assets/js/components/VoteOptions.vue';
import VoteOverview from '../../../planning_poker/assets/js/components/VoteOverview.vue';

describe('PokerSite', () => {
  createJsonElement({moderate: false, vote: true}, 'permissions');

  const wrapper = shallowMount(PokerSite);

  it('displays all other components correctly', async () => {
    expect(wrapper.findComponent(VoteOverview)).toBeTruthy();
    expect(wrapper.findComponent(StoryDetail)).toBeTruthy();
    expect(wrapper.findComponent(StoriesOverview)).toBeTruthy();
    expect(wrapper.findComponent(VoteOptions)).toBeTruthy();
  });
});
