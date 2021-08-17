<template>
    <div class="vote-options">
        <div class="cards-wrapper" v-if="displayPointOptions">
            <PlayingCardButton v-for="point in options.point_options"
                               :key="point[0]"
                               :is-front="isFront"
                               :is-small="isSmall"
                               :is-medium="isMedium"
                               :rank="point[1]"
                               :value="point[0]"
                               :chosen="false"
                               class="clickable"
                               @make-chosen="makeChosen($event)">
            </PlayingCardButton>
        </div>
        <div v-if="displayNonPointOptions" class="buttons-wrapper">
            <button v-for="option in options.non_point_options" v-on:click="makeChosen({rank: option[0]})"
                    class="clickable">
                {{ option[1] }}
            </button>
        </div>
    </div>
</template>

<script>
    import PlayingCardButton from './PlayingCardButton.vue';

    export default {
        props: {
            permissions: Object,
            userVoted: Boolean,
        },
        data: function () {
            return {
                options: JSON.parse(document.getElementById('options').textContent),
                isFront: true,
                isSmall: false,
                isMedium: true,
                choice: null,
            };
        },
        computed: {
            moderate: function () {
                return ((!this.permissions.vote || this.userVoted) && this.permissions.moderate);
            },
            spectate: function () {
                return Object.values(this.permissions).every(permission => permission === false);
            },
            displayPointOptions: function () {
                return !this.spectate && this.$parent.$refs.storiesOverview.activeStory !== null;
            },
            displayNonPointOptions: function () {
                return !this.moderate && this.displayPointOptions;
            },
        },
        methods: {
            vote: function (choice) {
                if (this.moderate) {
                    this.$consumer.submitStoryPoints(choice);
                } else {
                    this.$consumer.submitChoice(choice);
                }
            },
            removeOption: function (rank) {
                let key = Object.keys(this.options).find(key => this.options[key].find(option => option[0] === rank));
                let index = this.options[key].findIndex(option => option[0] === rank);
                this.choice = {[key]: this.options[key].splice(index, 1), index: index};
            },
            resetOptions: function () {
                if (this.choice == null) {
                    return;
                }
                let key = Object.keys(this.choice)[0];
                this.options[key].splice(this.choice.index, 0, this.choice[key][0]);
                this.choice = null;
            },
            makeChosen: function (card) {
                this.vote(card.rank);
                if (this.choice !== null) {
                    this.resetOptions();
                }
                if (!this.permissions.moderate) {
                    this.$consumer.app.$refs.storyDetail.setupOverlay(card.rank);
                    this.removeOption(card.rank);
                }
            },
        },
        components: {PlayingCardButton},
    }
</script>
