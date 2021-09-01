import {shallowMount} from '@vue/test-utils';

import Vote from '../../../planning_poker/assets/js/components/Vote.vue';
import PlayingCard from '../../../planning_poker/assets/js/components/PlayingCard.vue';

describe('Vote', () => {
  const users = [{name: 'Katharina'}, {name: 'Laura'}, {name: 'Thorsten'}];
  const $consumer = {submitStoryPoints: jest.fn()};
  const wrapper = shallowMount(Vote, {
    propsData: {
      permissions: {
        moderate: false,
      },
      users: users,
      value: '3',
      showValue: false,
    },
    mocks: {
      $consumer,
    }
  });

  it('shows correct amount of cards', async () => {
    expect(wrapper.findAllComponents(PlayingCard)).toHaveLength(2);
    wrapper.setProps({users: [{name: 'Peter'}]});
    await wrapper.vm.$nextTick();
    expect(wrapper.findAllComponents(PlayingCard)).toHaveLength(1);
  });

  it(`emits submit-points when it's clickable`, async () => {
    wrapper.setProps({
      permissions: {
        moderate: true,
      },
      showValue: true,
      value: '3',
    });
    await wrapper.vm.$nextTick();
    let div = wrapper.find('div.vote > div');
    div.trigger('click');
    expect($consumer.submitStoryPoints.mock.calls[0]).toEqual(['3']);
    wrapper.setProps({
      permissions: {
        moderate: false,
      },
      showValue: true,
      value: '3',
    });
    await wrapper.vm.$nextTick();
    div.trigger('click');
    expect($consumer.submitStoryPoints.mock.calls.length).toEqual(1);
  });

  it('displays the correct string of the users.', async () => {
    wrapper.setProps({users: users});
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.voterNames).toEqual('Katharina, Laura, Thorsten');

    wrapper.setProps({users: [{name: 'Donald'}]});
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.voterNames).toEqual('Donald');
  });

  it('returns the correct amount of cards', async () => {
    wrapper.setProps({users: users});
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.displayedCardsAmount).toEqual(2);

    wrapper.setProps({users: [{name: 'Django'}]});
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.displayedCardsAmount).toEqual(1);
  });

  it('is clickable when the user has already voted, is a moderator and the option is a valid option for a story',
      async () => {
        wrapper.setProps({
          showValue: true,
          value: '3',
          permissions: {
            moderate: false,
          },
        });
        await wrapper.vm.$nextTick();
        expect(wrapper.vm.isClickable).toBeFalsy();

        wrapper.setProps({
          showValue: false,
          value: '3',
          permissions: {
            moderate: true,
          },
        });
        await wrapper.vm.$nextTick();
        expect(wrapper.vm.isClickable).toBeFalsy();

        wrapper.setProps({
          showValue: true,
          value: 'Not a valid value',
          permissions: {
            moderate: true,
          },
        });
        await wrapper.vm.$nextTick();
        expect(wrapper.vm.isClickable).toBeFalsy();

        wrapper.setProps({
          showValue: true,
          value: '3',
          permissions: {
            moderate: true,
          },
        });
        await wrapper.vm.$nextTick();
        expect(wrapper.vm.isClickable).toBeTruthy();
      });
});
