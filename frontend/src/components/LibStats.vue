<template>
    <div class="container p-3">
        <div class="row">
            <h3>Digital Library: Overall Analytics</h3>
        </div>
        <div class="row row-col-2 p-2">
            <div class="col-sm-6">
                <h5>Section Popularity Among Users</h5>
                <img :src="require('@/assets/graphs/'+stats_data.section_read_path)" height="400" width="600"/>
            </div>
            <div class="col-sm-6">
                <h5>Section Wise Revenue Generation Distribution</h5>
                <img :src="require('@/assets/graphs/'+stats_data.section_revenue_path)" height="400" width="400"/>
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
            stats_data: {},

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
                // console.log(data)
                this.stats_data = data;  // set output
                // console.log(this.stats_data, 'fetch')
            }catch(error){console.log(error);} 
        }
    },
    created(){
        this.getLibrarianStats();
        // console.log('here created', this.stats_data)
    }
}
</script>

<style scoped>
h3, h5{
    text-align: center;
}
</style>