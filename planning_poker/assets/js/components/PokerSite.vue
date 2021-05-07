<template>
    <div class="poker-container">
        <div class="overviews">
            <VoteOverview :permissions="permissions" ref="voteOverview"></VoteOverview>
            <StoryDetail ref="storyDetail"></StoryDetail>
            <StoriesOverview :permissions="permissions" ref="storiesOverview"></StoriesOverview>
        </div>
        <VoteOptions
                :user-voted="userVoted"
                :permissions="permissions"
                ref="voteOptions">
        </VoteOptions>
    </div>
</template>

<script>
    import VoteOverview from "./VoteOverview.vue";
    import StoryDetail from "./StoryDetail.vue";
    import StoriesOverview from "./StoriesOverview.vue";
    import VoteOptions from "./VoteOptions.vue";

    export default {
        data: function () {
            return {
                userVoted: false,
                permissions: JSON.parse(document.getElementById('permissions').textContent)
            }
        },
        components: {
            VoteOverview, StoryDetail, StoriesOverview, VoteOptions
        }
    }
</script>
