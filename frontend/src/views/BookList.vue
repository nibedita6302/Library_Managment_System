<template>
    <div v-if="user.role==1" class="d-flex justify-content-center p-4">
        <button class="btn" id="btn-book"  @click="go_to_create_book">
            <i class="bi bi-shield-fill-plus"></i>
            Add New Book
        </button> 
    </div>
    <BookDisplay :section_id="section_id"></BookDisplay>
</template>

<script>
import BookDisplay from '@/components/BookDisplay.vue';

export default{
    name: 'BookList',
    data(){
        return{
            section_id: this.$route.params.section_id,
            user: JSON.parse(localStorage.getItem('user'))
        }
    },
    components: {
        BookDisplay
    },
    methods:{
        go_to_create_book(){
            this.$router.push('/book/create');
        }
    }
}
</script>

<style scoped>
button#btn-book{
    background-color: greenyellow;
}
</style>