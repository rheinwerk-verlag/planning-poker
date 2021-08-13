<template>
    <div class="stories-list">
        <h5>{{ title }}</h5>
        <transition-group name="stories-list" tag="div">
            <AsideStory v-for="story in displayedStories"
                        :points="story.points"
                        :story-id="story.id"
                        :story-title="story.title"
                        :key="story.id"
                        :permissions="permissions"
                        @activate-story="activateStory($event)">
            </AsideStory>
        </transition-group>
        <button v-if="!showMore" @click="toggleShowMore" class="clickable show-more">
            {{stories.length > 3? showMoreString : ''}}
        </button>
        <button v-else @click="toggleShowMore" class="clickable show-more">{{stories.length > 3? showLessString : ''}}
        </button>
    </div>
</template>

<script>
    import AsideStory from './AsideStory.vue';

    export default {
        props: {
            title: String,
            stories: Array,
            showLast: Boolean,
            permissions: Object,
        },
        data: function () {
            return {
                showMore: false
            };
        },
        methods: {
            activateStory: function (storyId) {
                this.$emit('activate-story', storyId);
            },
            toggleShowMore: function () {
                this.showMore = !this.showMore;
            },
        },
        computed: {
            displayedStories: function () {
                let stories;
                if (this.showMore) {
                    stories = this.stories;
                } else {
                    if (this.showLast) {
                        stories = this.stories.slice(Math.max(this.stories.length - 3, 0));
                    } else {
                        stories = this.stories.slice(0, 3);
                    }
                }
                return stories;
            },
            undisplayedStoriesAmount: function () {
                return this.stories.length - 3;
            },
            showMoreString: function () {
                return this.$interpolate(this.$t('Show more (+%s)'), [this.undisplayedStoriesAmount]);
            },
            showLessString: function () {
                return this.$t('Show less');
            },
        },
        components: {AsideStory}
    }
</script>
