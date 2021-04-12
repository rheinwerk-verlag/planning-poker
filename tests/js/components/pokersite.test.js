import {shallowMount} from "@vue/test-utils";

import {createJSONElement} from "../../../planning_poker/assets/js/utils";

import PokerSite from "../../../planning_poker/assets/js/components/PokerSite";
import StoryDetail from "../../../planning_poker/assets/js/components/StoryDetail";
import StoriesOverview from "../../../planning_poker/assets/js/components/StoriesOverview";
import VoteOptions from "../../../planning_poker/assets/js/components/VoteOptions";
import VoteOverview from "../../../planning_poker/assets/js/components/VoteOverview";

describe('PokerSite', () => {
    createJSONElement({moderate: false, vote: true}, "permissions");

    const wrapper = shallowMount(PokerSite);

    it('displays all other components correctly', async () => {
        expect(wrapper.findComponent(VoteOverview)).toBeTruthy();
        expect(wrapper.findComponent(StoryDetail)).toBeTruthy();
        expect(wrapper.findComponent(StoriesOverview)).toBeTruthy();
        expect(wrapper.findComponent(VoteOptions)).toBeTruthy();
    });
});
