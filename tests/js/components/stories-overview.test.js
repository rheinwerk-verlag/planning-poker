import {shallowMount} from '@vue/test-utils';

import {createJsonElement} from '../../../planning_poker/assets/js/utils.js';

import AsideStory from '../../../planning_poker/assets/js/components/AsideStory.vue';
import StoriesOverview from '../../../planning_poker/assets/js/components/StoriesOverview.vue';
import StoriesList from '../../../planning_poker/assets/js/components/StoriesList.vue';

describe('StoriesOverview', () => {
  const $consumer = {
    nextStoryRequested: jest.fn()
  }

  function generateStories(offset = 1, length = 5) {
    return [...Array(length).keys()].map(i => {
      let j = offset + i;
      return {id: j, story_label: `Story ${j}`, description: `<p>Description of Story #${j}</p>`};
    });
  }

  createJsonElement(generateStories(), 'initial-stories');

  const wrapper = shallowMount(StoriesOverview, {
    propsData: {
      permissions: {
        moderate: false,
      },
    },
    mocks: {
      $consumer,
      $t: jest.fn(x => x)
    }
  });

  it('displays the correct state initially', () => {
    let storiesLists = wrapper.findAllComponents(StoriesList);
    expect(storiesLists).toHaveLength(1);
    expect(storiesLists.at(0).vm.stories).toEqual(generateStories());
    expect(wrapper.findAllComponents(AsideStory)).toHaveLength(0);
  });

  describe.each([
    ['Upcoming Stories', null],
    ['Upcoming Stories', generateStories(11, 1).pop()],
    ['Previous Stories', null],
    ['Previous Stories', generateStories(11, 1).pop()],
  ])(`activates the correct story when the activated story is in '%s'`, (title, active_story) => {
    test('', async () => {
      wrapper.vm.previousStories = generateStories();
      wrapper.vm.upcomingStories = generateStories(6);
      wrapper.vm.activeStory = active_story;
      await wrapper.vm.$nextTick;
      let storiesLists = wrapper.findAllComponents(StoriesList);
      let clickedStoriesList = storiesLists.wrappers.find(wrapper => wrapper.vm.title === title);
      let clickedStory = clickedStoriesList.vm.stories[2];
      expect(clickedStoriesList.vm.stories).toHaveLength(5);
      let unclickedStoriesList = storiesLists.wrappers.find(wrapper => wrapper.vm.title !== title);
      expect(unclickedStoriesList.vm.stories).toHaveLength(5);

      await clickedStoriesList.vm.$emit('activate-story', clickedStory.id);
      await wrapper.vm.$nextTick();

      expect(clickedStoriesList.vm.stories).toHaveLength(2);
      expect(unclickedStoriesList.vm.stories).toHaveLength(active_story !== null ? 8 : 7);
      expect(wrapper.vm.activeStory.id).toEqual(clickedStory.id);
    });
  });

  it('does not change the active story if the chosen story is already activated', async () => {
    wrapper.vm.previousStories = generateStories();
    wrapper.vm.upcomingStories = generateStories(6);
    let activeStory = wrapper.vm.upcomingStories.pop();
    wrapper.vm.activeStory = activeStory;
    await wrapper.vm.$nextTick;
    let storiesLists = wrapper.findAllComponents(StoriesList);
    let previousStoriesList = storiesLists.wrappers.find(wrapper => wrapper.vm.title === 'Previous Stories');
    expect(previousStoriesList.vm.stories).toHaveLength(5);
    let upcomingStoriesList = storiesLists.wrappers.find(wrapper => wrapper.vm.title === 'Upcoming Stories');
    expect(upcomingStoriesList.vm.stories).toHaveLength(4);
    upcomingStoriesList.findIndex = jest.fn(x => x);

    await upcomingStoriesList.vm.$emit('activate-story', activeStory.id);
    expect(upcomingStoriesList.findIndex.mock.calls).toHaveLength(0);
  });

  it('requests the next story when the user has the moderate permission', async () => {
    wrapper.vm.upcomingStories = generateStories();
    let activeStory = wrapper.vm.upcomingStories.pop();
    wrapper.vm.activeStory = activeStory;
    await wrapper.vm.$nextTick;
    wrapper.setProps({
      permissions: {
        moderate: false,
      },
    });
    wrapper.vm.$consumer.nextStoryRequested.mockClear();
    wrapper.vm.makeActive(1);
    expect(wrapper.vm.$consumer.nextStoryRequested).not.toBeCalled();

    wrapper.setProps({
      permissions: {
        moderate: true,
      },
    });
    wrapper.vm.makeActive(2);
    await wrapper.vm.$nextTick;
    expect(wrapper.vm.$consumer.nextStoryRequested).toHaveBeenLastCalledWith(2);
  });
});
