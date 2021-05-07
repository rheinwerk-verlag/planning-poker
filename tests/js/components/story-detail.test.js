import {shallowMount} from "@vue/test-utils";

import StoryDetail from "../../../planning_poker/assets/js/components/StoryDetail";
import PlayingCard from "../../../planning_poker/assets/js/components/PlayingCard";

describe('StoryDetail', () => {
    const mocks = {
        $t: jest.fn(x => x)
    };

    const wrapper = shallowMount(StoryDetail, {
        mocks: mocks
    });

    wrapper.vm.title = "Story Title";
    wrapper.vm.description = "<p>Some Description</p>";

    it("displays the correct title and description", () => {
        expect(wrapper.find("h2.story-label").text()).toEqual("Story Title");
        expect(wrapper.find("div.description-text").text()).toEqual("Some Description");
    });

    it("shows the overlay with the correct rank", async () => {
        wrapper.vm.showOverlay = true;
        wrapper.vm.rank = "3";
        await wrapper.vm.$nextTick;

        expect(wrapper.findComponent(PlayingCard).vm.rank).toEqual("3");
    });

    it("returns the noDescriptionString when the description is empty", () => {
        wrapper.vm.description = '';
        expect(wrapper.vm.descriptionString).toEqual("No description available.")
    });

    it("sets up the overlay", () => {
        wrapper.vm.showOverlay = false;
        wrapper.vm.rank = "";

        wrapper.vm.setupOverlay("3");

        expect(wrapper.vm.showOverlay).toEqual(true);
        expect(wrapper.vm.rank).toEqual("3");
    });

    it("resets the overlay", () => {
        expect(wrapper.vm.showOverlay).toEqual(true);
        expect(wrapper.vm.rank).toEqual("3");

        wrapper.vm.resetOverlay();

        wrapper.vm.showOverlay = false;
        wrapper.vm.rank = "";
    });
});
