<template>
    <div class="story-detail custom-scrollbar">
        <h2 class="story-label ellipsis-overflow" :title="title"><br v-if="!title">{{title}}</h2>
        <div class="description-wrapper">
            <div class="description-overlay" v-if="showOverlay">
                <PlayingCard
                        :rank="rank"
                        :isSmall="false"
                        :isMedium="false"
                        :isFront="true">
                </PlayingCard>
            </div>
            <div class="description-text" v-html="descriptionString" :class="{blur: showOverlay}"></div>
            <button class="clickable close-overlay" v-if="showOverlay" @click="showOverlay = false">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2541 2541" shape-rendering="geometricPrecision"
                     text-rendering="geometricPrecision" image-rendering="optimizeQuality" fill-rule="evenodd"
                     clip-rule="evenodd">
                    <path d="M29 172c-39-39-39-103 0-142s103-39 142 0l1099 1099L2369 30c39-39 103-39 142 0s39 103 0 142L1412 1271l1099 1099c39 39 39 103 0 142s-103 39-142 0L1270 1413 171 2512c-39 39-103 39-142 0s-39-103 0-142l1099-1099L29 172z"
                          fill-rule="nonzero"/>
                </svg>
            </button>
        </div>
    </div>
</template>

<script>
    import PlayingCard from './PlayingCard.vue';

    export default {
        data: function () {
            return {
                title: '',
                description: '',
                showOverlay: false,
                rank: '',
            };
        },
        computed: {
            noDescriptionString: function () {
                return this.$t('No description available.');
            },
            descriptionString: function () {
                return this.description || this.noDescriptionString;
            },
        },
        methods: {
            setupOverlay: function (rank) {
                this.showOverlay = true;
                this.rank = rank;
            },
            resetOverlay: function () {
                this.showOverlay = false;
                this.rank = '';
            },
        },
        components: {PlayingCard}
    }
</script>
