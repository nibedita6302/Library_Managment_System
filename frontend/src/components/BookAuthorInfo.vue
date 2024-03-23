<template>
    <div class="container p-5">
        <div class="row g-2">
            <div class="col-sm-4">
                <img :src="bImage" :alt="book.b_name"/>
            </div>
            <div class="col-sm-8">
                <h1>{{ book.b_name }}</h1>
                <button class="btn btn-warning" @click="IssueBookRequest">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bookmark-star" viewBox="0 0 16 16">
                        <path d="M7.84 4.1a.178.178 0 0 1 .32 0l.634 1.285a.18.18 0 0 0 .134.098l1.42.206c.145.021.204.2.098.303L9.42 6.993a.18.18 0 0 0-.051.158l.242 1.414a.178.178 0 0 1-.258.187l-1.27-.668a.18.18 0 0 0-.165 0l-1.27.668a.178.178 0 0 1-.257-.187l.242-1.414a.18.18 0 0 0-.05-.158l-1.03-1.001a.178.178 0 0 1 .098-.303l1.42-.206a.18.18 0 0 0 .134-.098z"/>
                        <path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.777.416L8 13.101l-5.223 2.815A.5.5 0 0 1 2 15.5zm2-1a1 1 0 0 0-1 1v12.566l4.723-2.482a.5.5 0 0 1 .554 0L13 14.566V2a1 1 0 0 0-1-1z"/>
                    </svg>
                    Issue Book
                </button>
                <hr>
                <h4> Summary</h4>
                <p>{{ book.summary }}</p>
                <hr>
                <h4 style="color: brown;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-vector-pen" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M10.646.646a.5.5 0 0 1 .708 0l4 4a.5.5 0 0 1 0 .708l-1.902 1.902-.829 3.313a1.5 1.5 0 0 1-1.024 1.073L1.254 14.746 4.358 4.4A1.5 1.5 0 0 1 5.43 3.377l3.313-.828zm-1.8 2.908-3.173.793a.5.5 0 0 0-.358.342l-2.57 8.565 8.567-2.57a.5.5 0 0 0 .34-.357l.794-3.174-3.6-3.6z"/>
                        <path fill-rule="evenodd" d="M2.832 13.228 8 9a1 1 0 1 0-1-1l-4.228 5.168-.026.086z"/>
                    </svg>
                    Author: {{ author.a_name }}
                </h4>
                <h5>About Author</h5>
                <p>{{ author.about_author }}</p>
            </div>
        </div>
        <hr>
        <div class="row g-2">
            <div class="col">
                <div class="row">
                    <div class="col-9">
                        <h3>User Review</h3>
                    </div>
                    <div class="col-3">
                        <button class="btn btn-warning" @click="submitReview">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pen me-1" viewBox="0 0 16 16">
                                <path d="m13.498.795.149-.149a1.207 1.207 0 1 1 1.707 1.708l-.149.148a1.5 1.5 0 0 1-.059 2.059L4.854 14.854a.5.5 0 0 1-.233.131l-4 1a.5.5 0 0 1-.606-.606l1-4a.5.5 0 0 1 .131-.232l9.642-9.642a.5.5 0 0 0-.642.056L6.854 4.854a.5.5 0 1 1-.708-.708L9.44.854A1.5 1.5 0 0 1 11.5.796a1.5 1.5 0 0 1 1.998-.001m-.644.766a.5.5 0 0 0-.707 0L1.95 11.756l-.764 3.057 3.057-.764L14.44 3.854a.5.5 0 0 0 0-.708z"/>
                            </svg>
                            Post Review
                        </button>
                    </div>
                </div>
                <div class="row" v-for="r in reviews" :key="r.r_id">
                    {{ r }}
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default{
    name: 'BookAuthorInfo',
    props: ['book_id'],
    data(){
        return {
            error: '',
            book: {},
            author: {},
            reviews: [],
            bImage: ''
        }
    },
    methods:{
        getImage(){
            console.log("path:"+this.book.b_image);
            this.bImage = require(`@/assets/upload/${this.book.b_image}`);
        },
        async fetchBookByID(){
            try{
                const res = await fetch("http://localhost:8000/api/book/"+this.book_id, {
                    method: 'GET',
                    mode: 'cors',
                    credentials: 'include',
                    headers: {
                        'Content-Type':'application/json',
                    }
                })
                if (!res.ok && res.status!=404) { throw Error("HTTP Error at Search:"+res.status) }
                const data = await res.json() ;
                if (res.status==404){
                    this.error = data.message.error;  // set error
                    this.book = {};                   // reset output
                    this.reviews = [];
                }
                else { 
                    this.book = data.book_details;  // set output
                    this.reviews = data.reviews;
                    this.error = '';                // reset error
                }
            }catch(error){console.log(error);} 
        },
        async fetchAuthorDetails(){
            try{
                const res = await fetch("http://localhost:8000/api/author/"+this.book.a_id, {
                    method: 'GET',
                    mode: 'cors',
                    credentials: 'include',
                    headers: {
                        'Content-Type':'application/json',
                    }
                })
                if (!res.ok && res.status!=404) { throw Error("HTTP Error at Search:"+res.status) }
                const data = await res.json() ;
                if (res.status==404){
                    this.error = data['message']['error'];  // set error
                    this.author = null;               // reset output
                }
                else { 
                    this.author = data;  // set output
                    this.error = '';           // reset error
                }
            }catch(error){console.log(error);} 
        },
        async IssueBookRequest(){

        }
    },
    async created(){
        await this.fetchBookByID();
        this.getImage();
        if (this.book!=null){
            await this.fetchAuthorDetails();
            console.log('complete2')
        }
    }
}
</script>

<style scoped>
img{
    min-height: 500px;
    max-height: 500px;
}
</style>