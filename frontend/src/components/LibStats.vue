<template>
    <div class="d-flex container justify-content-center p-3">
        <h3>Digital Library: Overall Analytics</h3>
        <div class="col-sm-6">
            <iframe :src="require('@/assets/graphs/'+stats_data.section_read_path)"></iframe>
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
            stats_data: {}
        }
    }, 
    methods:{
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
                this.stats_data = data;  // set output
            }catch(error){console.log(error);} 
        }
    },
    created(){
        this.getLibrarianStats();
    }
}
</script>

<style>

</style>