import {shallowMount} from '@vue/test-utils';

import PlayingCard from '../../../planning_poker/assets/js/components/PlayingCard.vue';

describe('PlayingCard', () => {
  const wrapper = shallowMount(PlayingCard);
  wrapper.setProps({rank: '3'});
  it('shows back', async () => {
    wrapper.setProps({isFront: false});
    await wrapper.vm.$nextTick;
    expect(() => wrapper.get('.card-content span')).toThrow();
    expect(wrapper.get('.card-content.card-back')).toBeTruthy();
  });

  it('shows front', async () => {
    wrapper.setProps({isFront: true});
    await wrapper.vm.$nextTick;
    expect(() => wrapper.get('.card-content.card-back')).toThrow();
    let children = wrapper.findAll('.card-content *').wrappers;
    expect(children.length).toBe(3);
    children.forEach(child => {
      expect(child.html()).toContain('3');
    });
  });

  it('displays correct ranks', async () => {
    wrapper.setProps({isFront: true, rank: 'Too long'});
    await wrapper.vm.$nextTick;
    expect(wrapper.text()).toBe('T T T');
  });
});
