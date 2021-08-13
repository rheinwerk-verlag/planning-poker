<template>
    <div v-if="isFront" class="card card-front" :class="{small: isSmall, medium: isMedium, hover: hoverable}">
        <div class="card-content card-front medium" :class="{small: isSmall, medium: isMedium}">
            <div>{{ displayableRank }}</div>
            <span>{{ displayableRank }}</span>
            <div>{{ displayableRank }}</div>
        </div>
    </div>
    <div v-else class="card card-back" :class="{small: isSmall, medium: isMedium, hover: hoverable}">
        <div class="card-content card-back" :class="{small: isSmall, medium: isMedium}"></div>
    </div>
</template>

<script>
    export default {
        props: {
            isFront: Boolean,
            isSmall: Boolean,
            isMedium: Boolean,
            hoverable: Boolean,
            rank: String,
        },
        computed: {
            displayableRank: function () {
                if (this.rank.length > 2) {
                    return this.rank[0];
                }
                return this.rank;
            },
        },
    }
</script>
