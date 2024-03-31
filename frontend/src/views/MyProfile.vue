<template>
    <UserProfileCRUD></UserProfileCRUD>
</template>

<script>
import UserProfileCRUD from '@/components/UserProfileCRUD.vue'

export default{
    name: 'MyProfile',
    data(){
        return{
            user: JSON.parse(localStorage.getItem('user')),
            token: localStorage.getItem('auth_token')
        }
    },
    components:{
        UserProfileCRUD,
    }
}
</script>

<style scoped>

</style>