<template>
    <div class="container p-5">
        <BookAuthorInfo :book_id="book_id"></BookAuthorInfo>
    </div>
</template>

<script>
import BookAuthorInfo from '@/components/BookAuthorInfo.vue'

export default{
    name: 'BookDetailsView',
    data(){
        return{
            book_id: this.$route.params.book_id,
        }
    },
    components:{
        BookAuthorInfo,
    },
    beforeRouteLeave(){
        this.book_id = null
        // console.log(this.book_id)
    }
}
</script>

<style scoped>

</style>