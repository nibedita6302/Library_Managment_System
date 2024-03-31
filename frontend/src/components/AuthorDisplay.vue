<template>
    <!-- Modal -->
    <div class="modal fade" id="info7" tabindex="-1" aria-labelledby="modallabel" aria-hidden="true">
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
                    data-bs-toggle="modal" data-bs-target="#info7" @click="deleteAuthor(a_id)">
                        Confirm
                    </button> 
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                </div>
            </div>
        </div>
    </div>

    <div class="container p-4">
        <div v-if="user.role==1" class="d-flex justify-content-center p-3">
            <button class="btn" id="btn-author"  @click="showForm=true">
                <i class="bi bi-patch-plus-fill"></i>
                Add New Book
            </button> 
        </div><br>
        <div class="row row-col-3 g-3 d-flex justify-content-center">
            <div class="col-sm-3 card me-3" v-for="a in author_data" :key="a.a_id">
                <h5 class="d-flex card-title justify-content-center p-1">{{a.a_name}}</h5> 
                <p class="card-body">{{ a.about_author }}</p>
                <div v-if="user.role==1" class="btn-group" role="group" aria-label="section">
                    <button type="button" class="btn btn-warning" @click="go_to_form(a)">
                        Update
                    </button>
                    <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#deleteAlert"
                    @click="a_id = a.a_id">
                        Delete
                    </button>
                </div>
            </div>
        </div>
        <hr>
        <div class="d-flex justify-content-center p-0">
            <form v-if="showForm" @submit.prevent="selectAPI">
                <legend>Author {{ author==null?'Create':'Update' }} Form:</legend>
                <label for="a_name">Author Name</label>
                <input type="text" :placeholder="author==null?'':author.a_name" id="a_name" v-model="a_name"/><br><br>
                <label for="about_author">About Author</label>
                <textarea type="text" :placeholder="author==null?'':author.about_author" id="about_author" v-model="about"></textarea><br><br>
                <button class="btn btn-primary" type="submit" data-bs-toggle="modal" data-bs-target="#info7">Submit</button>
                <button class="btn btn-secondary" @click="closeForm">Close</button>
            </form>
        </div>
    </div>
</template>

<script>
export default{
    name:'AuthorDisplay',
    data(){
        return{
            user: JSON.parse(localStorage.getItem('user')),
            token: localStorage.getItem('auth_token'),
            author_data: [],
            author: null,
            showForm: false,
            a_id: '',
            a_name: '',
            about: '',
            message: ''
        }
    },
    methods:{
        async fetchAllAuthors(){
            try{
                const res = await fetch('http://localhost:8000/api/all-authors', {
                    method: 'GET',
                    mode: 'cors',
                    credentials: 'include',
                    headers:{
                        'Authorization': this.token
                    }
                })
                if (!res.ok) { throw Error("HTTP Error at get all authors:"+res.status) }
                const data = await res.json() ;
                this.author_data = data;  // set output
            }catch(error){console.log(error);} 
        },
        go_to_form(a=null){
            this.author = a
            this.showForm=true
        }, 
        closeForm(){
            this.author=null
            this.showForm=false
        },
        selectAPI(){
            console.log(this.author==null, this.author)
            if (this.author==null){this.createAuthor();}
            else {this.updateAuthor();}
        },
        async updateAuthor(){
            try{
                const res = await fetch('http://localhost:8000/api/author/update/'+this.author.a_id, {
                    method: 'PUT',
                    mode: 'cors',
                    credentials: 'include',
                    headers:{
                        'Authorization': this.token,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({'a_name':this.a_name, 'about_author':this.about})
                })
                if (!res.ok && res.status!=400) { throw Error("HTTP Error at update author:"+res.status) }
                const data = await res.json() ;
                if (res.status==400){this.message = data.message.error;}
                else{this.message = data.message.success;}
            }catch(error){console.log(error);} 
        },
        async createAuthor(){
            try{
                const res = await fetch('http://localhost:8000/api/author/create', {
                    method: 'POST',
                    mode: 'cors',
                    credentials: 'include',
                    headers:{
                        'Authorization': this.token,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({'a_name':this.a_name, 'about_author':this.about})
                })
                if (!res.ok && res.status!=400) { throw Error("HTTP Error at create author:"+res.status) }
                const data = await res.json() ;
                if (res.status==400){this.message = data.message.error;}
                else{this.message = data.message.success;}
            }catch(error){console.log(error);} 
        }, 
        async deleteAuthor(){
            try{
                const res = await fetch('http://localhost:8000/api/author/delete/'+this.a_id, {
                    method: 'DELETE',
                    mode: 'cors',
                    credentials: 'include',
                    headers:{
                        'Authorization': this.token
                    }
                })
                if (!res.ok && res.status!=409) { throw Error("HTTP Error at delete author:"+res.status) }
                const data = await res.json() ;
                if (res.status==409){this.message = data.message.error;}
                else{this.message = data.message.success;}
            }catch(error){console.log(error);}
        }
    },
    created(){
        this.fetchAllAuthors();
    }
}
</script>

<style scoped>
.card-body{
    font-size: small;
}
i{
    font-size: larger;
}
button#btn-author{
    background-color: lightsalmon;
}
</style>