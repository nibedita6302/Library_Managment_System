<template>
    <!-- Modal -->
    <div class="modal fade" id="info1" tabindex="-1" aria-labelledby="modallabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <p class="modal-title" id="modallabel">
                        <!-- <i class="bi bi-exclamation-triangle-fill" style="color:orange;"></i> -->
                        {{ message }}
                    </p>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" 
                    aria-label="Close"></button>
                </div>
            </div>
        </div>
    </div>

    <!-- Book & Author Details -->
    <div class="row row-col-2 g-2">
        <div class="col-sm">
            <img :src="bImage" :alt="book.b_name"/>
        </div>
        <div class="col-sm">
            <h1>{{ book.b_name }}</h1>
            <button class="btn btn-warning" data-bs-toggle="modal" data-bs-target="#info1" 
            @click="IssueBookRequest">
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

    <!-- Book Review -->
    <div class="row g-2">
        <div class="col">
            <div class="row g-2">
                <div class="col-9">
                    <h3>User Review</h3>
                </div>
                <div class="col-3">
                    <button class="btn btn-warning" data-bs-toggle="modal" data-bs-target="#reviewForm">
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
                            <i class="bi bi-star-fill" v-for="i in r.rating" :key="i"
                            style="color: gold;"></i>
                            
                            <i class="bi bi-star" v-for="i in (5-r.rating)" :key="i"
                            style="color: orange;"></i>
                        </p>
                        <i class="card-text">{{ r.review }}</i>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Post Review Form-->
    <div class="modal fade" id="reviewForm" tabindex="-1" aria-labelledby="modallabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5>Write your review here</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" 
                    aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="validateReview">
                        <div class="mb-3">
                            <label for="rating" class="col-form-label">Rating:</label>
                            <input type="number" class="form-control" id="rating" v-model="rating"
                            step="1" max="5" min="1">
                        </div>
                        <div class="mb-3">
                            <label for="review" class="col-form-label">Review:</label>
                            <textarea class="form-control" id="review" v-model="review"></textarea>
                        </div>
                        <button class="btn btn-outline-success" data-bs-dismiss="modal" aria-label="Close" 
                        data-bs-toggle="modal" data-bs-target="#info1">
                            Submit
                        </button>
                        <button class="btn btn-outline-danger" data-bs-dismiss="modal" 
                        aria-label="Close">
                            Cancel
                        </button>
                    </form>
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
            rating: 1,
            review: ''
        }
    },
    methods:{
        getImage(){
            // console.log("path:"+this.book.b_image);
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
                if (!res.ok && res.status!=404) { throw Error("HTTP Error at get book by ID:"+res.status) }
                const data = await res.json() ;
                if (res.status==404){
                    this.message = data.message.error;  // set error
                    this.book = {};                   // reset output
                    this.reviews = [];
                }
                else { 
                    this.book = data.book_details;  // set output
                    this.reviews = data.reviews;
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
                if (!res.ok && res.status!=404) { throw Error("HTTP Error at get author:"+res.status) }
                const data = await res.json() ;
                if (res.status==404){
                    this.message = data.message.error;  // set error
                    this.author = null;               // reset output
                }
                else { 
                    this.author = data;  // set output
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
                    if (!res.ok && res.status!=400) { throw Error("HTTP Error at issue book:"+res.status) }
                    const data = await res.json() ;
                    if (res.status==400){
                        this.message = data.message.error;  // set error
                    }
                    else { this.message = data.message.success; }
                }catch(error){console.log(error);} 
            }else{this.message='You must be logged-in as User to issue books'}
        },
        validateReview(){
            if (this.rating<1 || this.rating>5 || this.review==''){
                console.log('here'+this.review+'review')
                this.message = 'Invalid Rating or Empty Review!'
            }else{ this.submitReview();}
        },
        async submitReview(){
            const user = JSON.parse(localStorage.getItem('user'))
            if (user && user.role==2){
                const token = localStorage.getItem('auth_token')
                try{
                    const res = await fetch("http://localhost:8000/api/book/"+this.book.b_id+'/review', {
                        method: 'POST',
                        mode: 'cors',
                        credentials: 'include',
                        headers: {
                            'Content-Type':'application/json',
                            'Authorization': `${token}`
                        },
                        body: JSON.stringify({'rating':this.rating, 'review':this.review})
                    })
                    if (!res.ok && (res.status!=400 && res.status!=403)) { 
                        throw Error("HTTP Error at submitReview:"+res.status) 
                    }
                    const data = await res.json() ;
                    if (res.status==400 || res.status==403){
                        this.message = data.message.error;  // set error
                    }
                    else { this.message = data.message.success; }
                }catch(error){console.log(error);} 
            }else{this.message='You must be logged-in as User to issue books'}
        }
    },
    async created(){
        await this.fetchBookByID();
        this.getImage();
        if (this.book!=null){
            await this.fetchAuthorDetails();
        }
    }
}
</script>

<style scoped>
img{
    min-height: 500px;
    max-height: 500px;
}
form{
    border: 0px;
}
</style>