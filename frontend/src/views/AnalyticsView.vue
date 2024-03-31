<template>
    <LibStats></LibStats>
</template>

<script>
import LibStats from '@/components/LibStats.vue';

export default{
    name: 'AnalyticsView',
    data(){
        return {
            // user: JSON.parse(localStorage.getItem('user')),
            // token: localStorage.getItem('auth_token')
        }
    },
    components: {
        LibStats
    }, 
    methods: {
        isLibrarian(){
            if (this.user!=null){
                if (this.user.role==1) {return true;}
            }
            return false;
        }, 
        isUser(){
            if (this.user!=null){
                if (this.user.role==2) {return true;}
            }
            return false
        }
    }
}
</script>