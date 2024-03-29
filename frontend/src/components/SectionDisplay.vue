<template>
    <div class="container p-4">
        <div class="row row-col-3 g-0">
            <div class="col-sm-4 card text-white me-3" v-for="s in sections" :key="s.s_id">
                <div style="transform: rotate(0);">
                    <img :src="require('@/assets/upload/'+s.s_image)" class="card-img" :alt="s.s_name">
                    <div class="card-img-overlay">
                        <h3 class="card-title">{{s.s_name}}</h3>
                        <b class="card-text">Book Count: {{ s.book_count }}</b>
                        <router-link :to="'/section/'+s.s_id+'/books'" class="stretched-link"></router-link>
                    </div>
                </div>
                <div class="btn-group" role="group" aria-label="Basic example">
                    <button type="button" class="btn btn-warning" @click.prevent="updateSection($event)">Update</button>
                    <button type="button" class="btn btn-danger" @click.prevent="deleteSection">Delete</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

export default{
    name: 'SectionDisplay',
    data(){
        return{
            sections: [],
            user: JSON.parse(localStorage.getItem('user'))
        }
    },
    methods:{
        async fetchSectionList(){
            try{
                const res = await fetch('http://localhost:8000/api/home/sections', {
                    method: 'GET',
                    mode: 'cors',
                    credentials: 'include'
                })
                if (!res.ok) { throw Error("HTTP Error at Search:"+res.status) }
                const data = await res.json() ;
                this.sections = data;  // set output
            }catch(error){console.log(error);} 
        }, 
        async updateSection(event){
            
        },
        async deleteSection(){
        }
    },
    created(){
        this.fetchSectionList()
    }
}
</script>

<style scoped>
img{
    min-height: 150px;
}
</style>