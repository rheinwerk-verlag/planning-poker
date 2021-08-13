<template>
    <div class="votes-overview">
        <div class="heading-wrapper">
           <h2>{{ title }}</h2>
            <button v-if="permissions.moderate && Object.keys(votes).length > 0" @click="reset" class="clickable">
                {{ resetString }}
            </button>
        </div>

        <transition-group name="votes-overview">
            <Vote v-for="vote in displayedVotes"
                  :showValue="showVotes"
                  :value="vote"
                  :users="votes[vote]"
                  :permissions="permissions"
                  :key="vote">
            </Vote>
        </transition-group>
    </div>
</template>

<script>
    import Vote from './Vote.vue';

    export default {
        props: {
            permissions: Object,
        },
        data: function () {
            return {
                votes: {},
                participants: [],
            };
        },
        computed: {
            resetString: function () {
                return this.$t('Reset');
            },
            title: function () {
                return this.$t('Votes');
            },
            showVotes: function () {
                let votes = Object.values(this.votes).reduce((acc, val) => acc.concat(val), []);
                return this.voters.every(voter => votes.some(vote => vote.id == voter.id)) || !this.permissions.vote
            },
            sortedVotesKeys: function () {
                let votes = this.votes;
                return Object.keys(votes).sort((a, b) => votes[b].length - votes[a].length);
            },
            displayedVotes: function () {
                if (this.showVotes) {
                    return this.sortedVotesKeys;
                }
                return this.shuffle(Object.keys(this.votes));
            },
            voters: function () {
                return this.participants.filter(participant => participant.permissions.includes('planning_poker.vote'));
            },
        },
        methods: {
            reset: function () {
                this.$consumer.resetRequested();
            },
            //implementation of the Fisher–Yates Shuffle
            //from https://bost.ocks.org/mike/shuffle/
            shuffle: function (array) {
                let m = array.length, t, i;

                // While there remain elements to shuffle…
                while (m) {

                    // Pick a remaining element…
                    i = Math.floor(Math.random() * m--);

                    // And swap it with the current element.
                    t = array[m];
                    array[m] = array[i];
                    array[i] = t;
                }

                return array;
            },
        },
        components: {Vote}
    }
</script>
