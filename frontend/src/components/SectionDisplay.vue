<template>
    <!-- Modal -->
    <div class="modal fade" id="info4" tabindex="-1" aria-labelledby="modallabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <p class="modal-title" id="modallabel">{{ message }}</p>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" 
                    aria-label="Close"></button>
                </div>
            </div>
        </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div class="modal fade" id="deleteAlert" tabindex="-1" aria-labelledby="modallabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-body">
                    <p class="modal-title" id="modallabel">Click confirm to delete Section</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-success" data-bs-dismiss="modal" aria-label="Close"
                    data-bs-toggle="modal" data-bs-target="#info4" @click="deleteSection(s_id)">
                        Confirm
                    </button> 
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                </div>
            </div>
        </div>
    </div>

    <div class="container p-3">
        <div v-if="isLibrarian()" class="d-flex justify-content-center">
            <button class="btn" id="btn-section"  @click="go_to_create">
                <i class="bi bi-shield-fill-plus"></i>
                Add New Section
            </button> &nbsp;
            <button class="btn" id="btn-author" @click="go_to_author">
                <i class="bi bi-send-arrow-up-fill"></i>
                Go to Authors Page
            </button> &nbsp;
            <button class="btn" id="btn-book"  @click="go_to_create_book">
                <i class="bi bi-plus-circle-fill"></i>
                Add New Book
            </button> 
        </div>
        <hr>
        <div class="row row-col-3 g-3 p-2 d-flex justify-content-center">
            <div class="col-sm-3 card text-white me-4" v-for="s in sections" :key="s.s_id">
                <div style="transform: rotate(0);">
                    <img :src="require('@/assets/upload/'+s.s_image)" class="card-img" :alt="s.s_name">
                    <div class="card-img-overlay">
                        <h3 class="card-title">{{s.s_name}}</h3>
                        <b class="card-text">Book Count: {{ s.book_count }}</b>
                        <router-link :to="'/section/'+s.s_id+'/books'" class="stretched-link"></router-link>
                    </div>
                </div>
                <div v-if="isLibrarian()" class="btn-group" role="group" aria-label="section">
                    <button type="button" class="btn btn-warning" @click="go_to_update(s.s_id)">
                        Update
                    </button>
                    <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#deleteAlert"
                    @click="s_id = s.s_id">
                        Delete
                    </button>
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
            s_id: null, 
            user: JSON.parse(localStorage.getItem('user')),
            token: localStorage.getItem('auth_token'),
            message: ''
        }
    },
    methods:{
        isLibrarian(){
            if (this.user!=null){
                if (this.user.role==1) { return true; }
            }
            return false;
        },
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
        go_to_update(s_id){
            this.$router.push('/section/'+s_id+'/update')
        }, 
        go_to_create(){
            this.$router.push('/section/create')
        },
        go_to_create_book(){
            this.$router.push('/book/create');
        },
        async deleteSection(s_id){
            try{
                const res = await fetch('http://localhost:8000/api/section/delete/'+s_id, {
                    method: 'DELETE',
                    mode: 'cors',
                    credentials: 'include',
                    headers: {
                        'Authorization': this.token
                    }
                })
                if (!res.ok && res.status!=404 && res.status!=409) { throw Error("HTTP Error at Section Delete:"+res.status) }
                const data = await res.json() ;
                if (res.status==404 || res.status==409){ this.message=data.message.error }
                else {this.message=data.message.success}
            }catch(error){console.log(error);} 
        }, 
        go_to_author(){
            this.$router.push('/authors')
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
i{
    font-size: x-large;
}
button#btn-author{
    background-color: orange;
}
button#btn-section{
    background-color: lightsalmon;
}
button#btn-book{
    background-color: greenyellow;
}
</style>
