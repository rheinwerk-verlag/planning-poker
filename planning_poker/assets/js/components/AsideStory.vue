<template>
    <button class="list-story"
            :class="{scored: points, clickable: permissions.moderate}"
            v-on="permissions.moderate ? { click: activateStory } : {}"
            :title="storyTitle">
        <span class="ellipsis-overflow">{{ storyTitle }}</span>
        <PlayingCard v-if="points" :is-front="true" :is-small="false" :is-medium="false" :rank="points"
                     :class="{tiny: true}">
        </PlayingCard>
    </button>
</template>

<script>
    import PlayingCard from "./PlayingCard.vue";

    export default {
        props: {
            points: String,
            storyId: Number,
            storyTitle: String,
            permissions: Object,
        },
        methods: {
            activateStory: function () {
                this.$emit('activate-story', this.storyId);
            }
        },
        components: {PlayingCard}
    }
</script>
