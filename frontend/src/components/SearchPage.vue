<template>
    <SearchBar @search="refresh"/>
    <div class="container p-2">
        <h4>Search On: {{ this.searchArg }}</h4>
        <p>Search Result: {{ this.search_output.length }} Found</p>
        <h5 v-if="this.error!=''">{{ this.error }}</h5>
        <div v-else class="container p-1">
            <div class="row g-4">
                <div class="card col-sm-4" v-for="book in this.search_output" :key="book.b_id">
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
import SearchBar from '@/components/SearchBar.vue'

export default{
    name: 'SearchPage',
    data(){
        return{
            searchArg: this.$route.query.searchArg,
            search_output: [],
            error: ''
        }
    },
    components:{
        SearchBar
    },
    methods:{
        getDate(date){
            var lst = date.split(" ");
            var newdate = lst[1]+" "+lst[2]+" "+lst[3];
            return newdate;
        },
        async refresh(){
            this.searchArg = this.$route.query.searchArg    // re-intialize searchArg
            // console.log('refresh '+this.searchArg)
            await this.fetchSearchOutput()
        },
        async fetchSearchOutput(){
            try{
                const res = await fetch('http://localhost:8000/api/search', {
                    method: 'POST',
                    mode: 'cors',
                    credentials: 'include',
                    headers: {
                        'Content-Type':'application/json',
                    },
                    body: JSON.stringify({'search':this.searchArg})
                })
                if (!res.ok && res.status!=404) { throw Error("HTTP Error at Search:"+res.status) }
                const data = await res.json() ;
                if (res.status==404){
                    this.error = data.message.error;  // set error
                    this.search_output = [];                // reset output
                }
                else { 
                    this.search_output = data;  // set output
                    this.error = '';            // reset error
                }
            }catch(error){console.log(error);} 
        }
    },
    created() {
        this.fetchSearchOutput()
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