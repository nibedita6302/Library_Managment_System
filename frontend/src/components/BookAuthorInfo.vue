<template>
    <div class="container p-5">
        <div class="row row-col-2 g-2">
            <div class="col-sm">
                <img :src="bImage" :alt="book.b_name"/>
            </div>
            <div class="col-sm">
                <h1>{{ book.b_name }}</h1>
                <button class="btn btn-warning" @click="IssueBookRequest">
                    <i class="bi bi-bookmark-star"></i>
                    Issue Book
                </button>
                <hr>
                <h4> Summary</h4>
                <p>{{ book.summary }}</p>
                <hr>
                <h4 style="color: brown;">
                    <i class="bi bi-vector-pen"></i>
                    Author: {{ author.a_name }}
                </h4>
                <h5>About Author</h5>
                <p>{{ author.about_author }}</p>
            </div>
        </div>
        <hr><br>
        <div class="row g-2">
            <div class="col">
                <div class="row g-2">
                    <div class="col-9">
                        <h3>User Review</h3>
                    </div>
                    <div class="col-3">
                        <button class="btn btn-warning" @click="submitReview">
                            <i class="bi bi-pen"></i>
                            Post Review
                        </button>
                    </div>
                </div>
                <div class="row g-3 p-2">
                    <p v-if="reviews.length==0">No reviews yet</p>
                    <div class="card" v-for="r in reviews" :key="r.r_id">
                        <p class="card-header">
                            <i class="bi bi-person-circle"></i>
                            {{ r.user_name }}
                        </p>
                        <div class="card-body">
                            <p class="card-title">
                                <i class="bi bi-star-fill" style="color: gold;" v-for="i in r.rating" :key="i"></i>
                                <i class="bi bi-star" style="color: orange;" v-for="i in (5-r.rating)" :key="i"></i>
                            </p>
                            <i class="card-text">{{ r.review }}</i>
                        </div>
                    </div>
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
            message: '',
            book: {},
            author: {},
            reviews: [],
            bImage: '',
            rating: 0,
            review: '',
            dis: true
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
                    credentials: 'include'
                })
                if (!res.ok && res.status!=404) { throw Error("HTTP Error at Search:"+res.status) }
                const data = await res.json() ;
                if (res.status==404){
                    this.error = data.message.error;  // set error
                    this.author = null;               // reset output
                }
                else { 
                    this.author = data;  // set output
                    this.error = '';           // reset error
                }
            }catch(error){console.log(error);} 
        },
        async IssueBookRequest(){
            const user = JSON.parse(localStorage.getItem('user'))
            if (user && user.role==2){
                const token = localStorage.getItem('auth_token')
                    try{
                        const res = await fetch("http://localhost:8000/api/issue-requests/new/"+this.book.b_id, {
                            method: 'POST',
                            mode: 'cors',
                            credentials: 'include',
                            headers: {
                                'Content-Type':'application/json',
                                'Authorization': `${token}`
                            }
                        })
                        if (!res.ok && res.status!=400) { throw Error("HTTP Error at Search:"+res.status) }
                        const data = await res.json() ;
                        if (res.status==400){
                            this.error = data.message.error;  // set error
                            console.log(this.error);
                        }
                        else { 
                            this.message = data.message.success;
                            console.log(this.message);
                        }
                    }catch(error){console.log(error);} 

            }else{this.message='You must be logged-in as User to issue books'}
        },
        async submitReview(){

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