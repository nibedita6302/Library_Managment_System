<template>
    <div class="container p-3">
        <h4>Section: {{ section.s_name }}</h4><br>
        <p v-if="this.books.length==0">Empty Section</p>
        <div v-else class="container">
            <div class="row row-col-3 g-2">
                <div class="card col me-2" v-for="book in this.books" :key="book.b_id">
                    <div class="row g-0">
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
            section: {}
        }
    },
    methods:{
        getDate(date){
            var lst = date.split(" ");
            var newdate = lst[1]+" "+lst[2]+" "+lst[3];
            return newdate;
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