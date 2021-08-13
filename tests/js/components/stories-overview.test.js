import {shallowMount} from "@vue/test-utils";

import {createJsonElement} from "../../../planning_poker/assets/js/utils";

import AsideStory from "../../../planning_poker/assets/js/components/AsideStory";
import StoriesOverview from "../../../planning_poker/assets/js/components/StoriesOverview";
import StoriesList from "../../../planning_poker/assets/js/components/StoriesList";

describe("Vote", () => {
    const $consumer = {
        nextStoryRequested: jest.fn()
    }

    function generateStories() {
        return [...Array(5).keys()].map(i => {
            let j = i + 1;
            return {id: j, story_label: `Story ${j}`, description: `<p>Description of Story #${j}</p>`};
        });
    }

    createJsonElement(generateStories(), "initial-stories");

    const wrapper = shallowMount(StoriesOverview, {
        propsData: {
            permissions: {
                moderate: false
            }
        },
        mocks: {
            $consumer,
            $t: jest.fn(x => x)
        }
    });

    it("displays the correct state initially", () => {
        let storiesLists = wrapper.findAllComponents(StoriesList);
        expect(storiesLists).toHaveLength(1);
        expect(storiesLists.at(0).vm.stories).toEqual(generateStories());
        expect(wrapper.findAllComponents(AsideStory)).toHaveLength(0);
    });

    describe.each([
        [
            "Upcoming Stories",
            {
                previousStories: [],
                upcomingStories: generateStories()
            }
        ],
        [
            "Previous Stories",
            {
                previousStories: generateStories(),
                upcomingStories: []
            }
        ],
    ])("activates the correct story when the activated story is in '%s'", (title, stories) => {
        test("", async () => {
            wrapper.vm.previousStories = stories.previousStories;
            wrapper.vm.upcomingStories = stories.upcomingStories;
            wrapper.vm.activeStory = null;
            await wrapper.vm.$nextTick;
            let storiesLists = wrapper.findAllComponents(StoriesList);
            let storiesList = storiesLists.wrappers.find(wrapper => wrapper.vm.title == title);
            expect(storiesList.vm.stories).toHaveLength(5);

            await storiesList.vm.$emit("activate-story", 3);
            await wrapper.vm.$nextTick();

            expect(wrapper.findAllComponents(StoriesList)).toHaveLength(2);
            wrapper.findAllComponents(StoriesList).wrappers.forEach(storiesListWrapper => {
                expect(storiesListWrapper.vm.stories).toHaveLength(2);
            });
            expect(wrapper.vm.activeStory.id).toEqual(3);
        });
    });
});
