import {shallowMount} from '@vue/test-utils';

import AsideStory from '../../../planning_poker/assets/js/components/AsideStory.vue';

async function asyncForEach(array, callback) {
  for (let index = 0; index < array.length; index++) {
    await callback(array[index], index, array);
  }
}

describe('AsideStory', () => {
  const wrapper = shallowMount(AsideStory, {
    propsData: {
      permissions: {
        moderate: false,
      },
    },
  });

  it('emits activate-story when the correct permission is set', async () => {
    let properties = [{permissions: {moderate: false}}, {permissions: {moderate: true}}];
    await asyncForEach(properties, async (property) => {
      wrapper.setProps(property);
      await wrapper.vm.$nextTick();
      wrapper.trigger('click');
      let expection = expect(wrapper.emitted('activate-story'));
      if (property.permissions.moderate) {
        expection.toBeTruthy();
      } else {
        expection.toBeFalsy();
      }
    });
  });
});
