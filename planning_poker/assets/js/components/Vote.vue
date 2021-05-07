<template>
    <div class="vote">
        <h5>{{ users.length }} x</h5>
        <div v-on="isClickable ? { click: submitPoints } : {}"
             :class="{clickable: isClickable, 'card-stack': users.length > 1}">
            <PlayingCard
                    v-for="_ in displayedCardsAmount"
                    :isFront="showValue"
                    :isSmall="true"
                    :isMedium="false"
                    :hoverable="false"
                    :rank="value"
                    :key="_">
            </PlayingCard>
        </div>
        <span class="ellipsis-overflow"
              :title="usersString">{{ usersString }}</span>
    </div>
</template>

<script>
    import PlayingCard from "./PlayingCard.vue";

    export default {
        props: {
            showValue: Boolean,
            value: String,
            users: Array,
            permissions: Object
        },
        methods: {
            submitPoints: function () {
                this.$consumer.submitStoryPoints(this.value);
            }
        }
        ,
        computed: {
            usersString: function () {
                return `${this.users.map(user => user.name).join(', ')}`;
            },
            displayedCardsAmount: function () {
                return this.users.length > 1 ? 2 : 1;
            },
            isClickable: function () {
                return this.showValue && this.value.match(/^[0-9]+$/) != null && this.permissions.moderate;
            }
        },
        components: {PlayingCard}
    }
</script>
