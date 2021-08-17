import {shallowMount} from "@vue/test-utils";

import AsideStory from "../../../planning_poker/assets/js/components/AsideStory";
import StoriesList from "../../../planning_poker/assets/js/components/StoriesList";

describe("StoriesList", () => {
  const stories =
    [...Array(5).keys()].map(i => {
      let j = i + 1;
      return {id: j, story_label: `Story ${j}`, description: `<p>Description of Story #${j}</p>`};
    });

  const mocks = {
    $interpolate: jest.fn(x => x),
    $t: jest.fn(x => x),
  };

  const wrapper = shallowMount(StoriesList, {
    propsData: {
      permissions: {
        moderate: false
      },
      title: "List-Title",
      stories: stories,
      showLast: false
    },
    mocks: mocks
  });

  it("displays the correct amount of stories", async () => {
    expect(wrapper.findAllComponents(AsideStory)).toHaveLength(3);
    expect(wrapper.find(".stories-list > button").text()).toEqual("Show more (+%s)");

    wrapper.vm.showMore = true;
    await wrapper.vm.$nextTick

    expect(wrapper.findAllComponents(AsideStory)).toHaveLength(stories.length);
    expect(wrapper.find(".stories-list > button").text()).toEqual("Show less");
  });

  it("activates the correct story", async () => {
    wrapper.vm.$nextTick;

    let asideStory = wrapper.findComponent(AsideStory);
    await asideStory.vm.$emit("activate-story", asideStory.vm.storyId);
    expect(wrapper.emitted('activate-story')).toBeTruthy();
  });

  describe("displayStories returns the correct stories", () => {
    it("when showMore is false as well as showLast", () => {
      wrapper.setProps({
        showLast: false
      });
      wrapper.vm.showMore = false;

      expect(wrapper.vm.displayedStories).toEqual(stories.slice(0, 3));
    });

    it("when showMore is false and showLast is true", () => {
      wrapper.setProps({
        showLast: true
      });
      wrapper.vm.showMore = false;

      expect(wrapper.vm.displayedStories).toEqual(stories.slice(2, 5));
    });

    it("when showMore is true and showLast is false", () => {
      wrapper.setProps({
        showLast: false
      });
      wrapper.vm.showMore = true;

      expect(wrapper.vm.displayedStories).toEqual(stories);
    });
  });

  it("calculates the correct undisplayedStoriesAmount", () => {
    expect(wrapper.vm.undisplayedStoriesAmount).toEqual(2);
  });

  it('toggles the showMore flag correctly', () => {
    wrapper.vm.showMore = true;
    wrapper.vm.toggleShowMore();
    expect(wrapper.vm.showMore).toEqual(false);
    wrapper.vm.toggleShowMore();
    expect(wrapper.vm.showMore).toEqual(true);
  });
});
