<template>
    <PendingIssues></PendingIssues>
    <CurrentIssues></CurrentIssues>
</template>

<script>
import CurrentIssues from '@/components/CurrentIssues.vue';
import PendingIssues from '@/components/PendingIssues.vue';

export default{
    name: 'IssuesView',
    data(){
        return{
        }
    },
    components:{
        CurrentIssues,
        PendingIssues
    }
}
</script>

<style scoped>

</style>