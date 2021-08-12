<template>
    <button @click="makeChosen" :class="{chosen: chosen}">
        <PlayingCard
                :is-front="isFront"
                :is-small="isSmall"
                :isMedium="isMedium"
                :hoverable="true"
                :rank="rank">
        </PlayingCard>
    </button>
</template>

<script>
    import PlayingCard from './PlayingCard.vue';

    export default {
        props: {
            isFront: Boolean,
            rank: String,
            value: String,
        },
        data: function () {
            return {
                isSmall: false,
                isMedium: true,
                chosen: false,
            };
        },
        methods: {
            makeChosen: function () {
                this.$emit('make-chosen', this);
            },
        },
        components: {PlayingCard}
    }
</script>
