<template>
    <div class="container p-3">
        <div class="row">
            <h3>Digital Library: Overall Analytics</h3>
        </div>
        <div class="row row-col-2 p-2">
            <div class="col-sm-6">
                <h5>Book Popularity Among Users</h5>
                <img :src="book_read_path" height="400" width="600"/>
            </div>
            <div class="col-sm-6">
                <h5>Section Wise Revenue Generation Distribution</h5>
                <img :src="section_revenue_path" height="400" width="400"/>
            </div>
        </div>
    </div>
</template>

<script>
export default{
    name: 'LibStats',
    data(){
        return {
            user: JSON.parse(localStorage.getItem('user')),
            token: localStorage.getItem('auth_token'),
            book_read_path: '',
            section_revenue_path: ''
        }
    }, 
    methods:{
        getImage(path){
            // console.log('require', import('@/assets/graphs/'+path))
            return require('@/assets/graphs/'+path);
        },
        async getLibrarianStats(){
            try{
                const res = await fetch('http://localhost:8000/api/librarian-stats', {
                    method: 'GET',
                    mode: 'cors',
                    credentials: 'include',
                    headers: {
                        'Authorization': this.token
                    }
                })
                if (!res.ok) { throw Error("HTTP Error at Lib Stats:"+res.status) }
                const data = await res.json() ;
                this.book_read_path = this.getImage(data.book_read_path);         // set output
                this.section_revenue_path = this.getImage(data.section_revenue_path);
            }catch(error){console.log(error);} 
        }
    },
    created(){
        this.getLibrarianStats();
    }
}
</script>

<style scoped>
h3, h5{
    text-align: center;
}
table{
    padding: 100px;
}
</style>