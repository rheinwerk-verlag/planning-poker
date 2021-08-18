import {shallowMount} from '@vue/test-utils';

import PlayingCardButton from '../../../planning_poker/assets/js/components/PlayingCardButton.vue';

describe('PlayingCardButton', () => {
  const wrapper = shallowMount(PlayingCardButton);
  it('emits make-chosen on click', async () => {
    wrapper.trigger('click');
    expect(wrapper.emitted('make-chosen')).toBeTruthy();
  });
});
