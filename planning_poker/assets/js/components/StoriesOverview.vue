<template>
    <div class="stories-overview">
        <h2 class="aside-stories-label">{{ title }}</h2>
        <StoriesList v-if="previousStories.length > 0"
                     :title="previousStoriesTitle"
                     :stories="previousStories"
                     :showLast="true"
                     :permissions="permissions"
                     @activate-story="makeActive($event)">
        </StoriesList>
        <div class="active-story">
            <h5>{{ activeStoryTitle }}</h5>
            <transition name="active-story-fade" mode="out-in">
                <AsideStory
                        v-if="activeStory"
                        :points="activeStory.points"
                        :story-id="activeStory.id"
                        :story-title="activeStory.title"
                        :permissions="permissions"
                        :key="activeStory.id">
                </AsideStory>
            </transition>
        </div>
        <StoriesList v-if="upcomingStories.length > 0"
                     :title="upcomingStoriesTitle"
                     :stories="upcomingStories"
                     :showLast="false"
                     :permissions="permissions"
                     @activate-story="makeActive($event)">
        </StoriesList>
    </div>
</template>

<script>
    import StoriesList from './StoriesList.vue';
    import AsideStory from './AsideStory.vue';

    export default {
        props: {
            permissions: Object,
        },
        data: function () {
            return {
                previousStories: [],
                activeStory: null,
                upcomingStories: JSON.parse(document.getElementById('initial-stories').textContent),
            };
        },
        computed: {
            title: function () {
                return this.$t('Stories');
            },
            previousStoriesTitle: function () {
                return this.$t('Previous Stories');
            },
            activeStoryTitle: function () {
                return this.$t('Active Story');
            },
            upcomingStoriesTitle: function () {
                return this.$t('Upcoming Stories');
            },
        },
        methods: {
            makeActive: function (storyId) {
                if (this.activeStory !== null) {
                    if (this.activeStory.id === storyId) {
                        return;
                    }
                }
                let index = this.upcomingStories.findIndex(element => element.id === storyId);
                if (index < 0) {
                    index = this.previousStories.findIndex(element => element.id === storyId);
                    if (this.activeStory !== null) {
                        this.upcomingStories.unshift(this.activeStory);
                    }
                    this.upcomingStories.unshift(...this.previousStories.splice(
                        index + 1,
                        this.previousStories.length - index - 1)
                    );
                    this.activeStory = this.previousStories.pop();
                } else {
                    if (this.activeStory !== null) {
                        this.previousStories.push(this.activeStory);
                    }
                    this.previousStories.push(...this.upcomingStories.splice(0, index));
                    this.activeStory = this.upcomingStories.shift();
                }
                if (this.permissions.moderate) {
                  this.$consumer.nextStoryRequested(this.activeStory.id)
                }
            },
        },
        components: {AsideStory, StoriesList}
    }
</script>
