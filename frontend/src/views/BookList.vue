<template>
    <BookDisplay :section_id="section_id"></BookDisplay>
</template>

<script>
import BookDisplay from '@/components/BookDisplay.vue';

export default{
    name: 'BookList',
    data(){
        return{
            section_id: this.$route.params.section_id
        }
    },
    components: {
        BookDisplay
    }
}
</script>

<style scoped>

</style>