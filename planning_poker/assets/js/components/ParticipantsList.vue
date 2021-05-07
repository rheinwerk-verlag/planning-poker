<template>
    <div class="participants-list"
         @mouseover="displayTooltip = true"
         @mouseleave="displayTooltip = false">
        <slot></slot>
        <span>({{ participants.length }})</span>

        <div class="participants-tooltip" v-if="displayTooltip && participants.length > 0">
            <ul>
                <li v-for="participant in participants">
                    <span>{{ participant.username }}</span>
                    <span class="muted">{{ permissionsDisplay(participant) }}</span>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
    export default {
        data: function () {
            return {
                participants: [],
                displayTooltip: false,
            };
        },
        computed: {
            permissions: function () {
                return {'poker.vote': this.$t('Voter'), 'poker.moderate': this.$t('Moderator')};
            }
        },
        methods: {
            userPermissions: function (user) {
                return user.permissions.map(permission => this.permissions[permission]);
            },
            permissionsDisplay: function (user) {
                let userPermissions = this.userPermissions(user);
                return userPermissions.length === 0 ? '' : `(${userPermissions.sort().join(', ')})`;
            }
        }
    }
</script>
