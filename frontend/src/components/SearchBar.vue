<template>
    <nav class="navbar">
        <div class="container-fluid">
            <form class="container-fluid p-1" @submit.prevent="search">
                <div class="input-group ">
                    <span class="navbar-brand" id="basic-addon1">Digital Library</span>
                    <input class="form-control me-2" v-model="search_input" type="text" placeholder="Search" 
                    aria-label="Search" aria-describedby="basic-addon1">
                    <button class="btn btn-outline-light" type="submit" @click="search">Search</button>
                </div>
            </form>
        </div>
    </nav>
</template>

<script>
export default {
    name: 'SearchBar',
    data(){
        return {
            search_input: ''
        }
    },
    methods:{
        async search(){
            this.$emit('search',this.search_input);
            this.$router.push({name: 'SearchPage', query:{'searchArg': this.search_input} });
        }
    }
}   
</script>
  
<style scoped>
    nav {
        background-color: black;
    }
    span {
        font-weight: 600;
        font-size: x-large;
        color: orange;
    }
    button {
        background-color: black;
        color: orange;
        font-weight: 500;
    }
</style>