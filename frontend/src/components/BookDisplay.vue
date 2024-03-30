<template>
    <!-- Modal -->
    <div class="modal fade" id="info5" tabindex="-1" aria-labelledby="modallabel" aria-hidden="true">
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
    <div class="modal fade" id="deleteBook" tabindex="-1" aria-labelledby="modallabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-body">
                    <p class="modal-title" id="modallabel">Click confirm to delete Book</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-success" data-bs-dismiss="modal" aria-label="Close"
                    data-bs-toggle="modal" data-bs-target="#info5" @click="deleteBook(b_id)">
                        Confirm
                    </button> 
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        Cancel
                    </button>
                </div>
            </div>
        </div>
    </div>

    <div class="container p-3">
        <h4>Section: {{ section.s_name }}</h4><br>
        <p v-if="this.books.length==0">Empty Section</p>
        <div v-else class="container p-0">
            <div class="row row-col-3 g-4">
                <div class="card col-sm-4 p-0" v-for="book in this.books" :key="book.b_id">
                    <div class="row g-0" style="transform: rotate(0);">
                        <div class="col-md-5">
                            <img :src="require('@/assets/upload/'+book.b_image)" 
                                class="img-fluid rounded-start" :alt="book.b_name">
                        </div>
                        <div class="col-md-7">
                            <div class="card-body">
                                <h5 class="card-title">{{ book.b_name }}</h5>
                                <p class="card-text"><i>Publisher:</i> {{ book.publisher }}</p>
                                <p class="card-text"><small class="text-muted">
                                    Published Date: {{ this.getDate(book.date_published) }}
                                </small></p>
                                <p class="card-text" style="color:red">PDF Price: ₹{{ book.pdf_price }}</p>
                            </div>
                        </div>
                        <router-link :to="'/book/'+book.b_id" class="stretched-link"></router-link>
                    </div>
                    <div v-if="user.role==1" class="btn-group me-2" role="group" aria-label="section">
                        <button type="button" class="btn btn-warning" @click="go_to_update(book.b_id)">Update</button>
                        <button type="button" class="btn btn-danger" @click="b_id=book.b_id"
                        data-bs-toggle="modal" data-bs-target="#deleteBook">
                            Delete
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

export default{
    name: 'BookDisplay',
    props: ['section_id'],
    data(){
        return{
            books: [],
            section: {},
            user: JSON.parse(localStorage.getItem('user')),
            token: localStorage.getItem('auth_token'),
            message: '',
            b_id: null
        }
    },
    methods:{
        getDate(date){
            var lst = date.split(" ");
            var newdate = lst[1]+" "+lst[2]+" "+lst[3];
            return newdate;
        },
        go_to_update(b_id){
            this.$router.push('/book/'+b_id+'/update')
        },
        async deleteBook(b_id){
            try{
                const res = await fetch('http://localhost:8000/api/book/delete/'+b_id, {
                    method: 'DELETE',
                    mode: 'cors',
                    credentials: 'include',
                    headers: {
                        'Authorization': this.token
                    }
                })
                if (!res.ok && res.status!=404 && res.status!=409) { throw Error("HTTP Error at Book Delete:"+res.status) }
                const data = await res.json() ;
                if (res.status==404 || res.status==409){ this.message=data.message.error }
                else {this.message=data.message.success}
            }catch(error){console.log(error);} 
        },
        async fetchBookbySectionID(){
            try{
                const res = await fetch('http://localhost:8000/api/section/'+this.section_id+'/books', {
                    method: 'GET',
                    mode: 'cors',
                    credentials: 'include'
                })
                if (!res.ok) { throw Error("HTTP Error at Search:"+res.status) }
                const data = await res.json() ;
                this.books = data;  // set output
            }catch(error){console.log(error);} 
        },
        async fetchSection(){
            try{
                const res = await fetch('http://localhost:8000/api/section/'+this.section_id, {
                    method: 'GET',
                    mode: 'cors',
                    credentials: 'include'
                })
                if (!res.ok) { throw Error("HTTP Error at Search:"+res.status) }
                const data = await res.json() ;
                this.section = data;  // set output
            }catch(error){console.log(error);} 

        }
    },
    created(){
        this.fetchBookbySectionID();
        this.fetchSection();
    }
}
</script>

<style scoped>
.card{
    max-width: 100%;
}
img{
    max-height: 300px;
}
</style>