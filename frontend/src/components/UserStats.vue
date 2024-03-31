<template>
    <div class="container p-3">
        <div class="row">
            <h3>Digital Library: Overall Analytics</h3>
        </div>
        <div class="row row-col-2 p-2">
            <div class="col-sm-6">
                <h5>Section Popularity Among Users</h5>
                <img :src="section_dist_path" height="400" width="400"/>
            </div>
            <div class="col-sm-6">
                <h5>Section Wise Revenue Generation Distribution</h5>
                <img :src="fav_author_path" height="400" width="400"/>
            </div>
        </div>
    </div>
    <div class="container p-5 ">
        <h5>Top 5 User Ranking</h5>
        <table class="table table-danger table-striped table-sm">
            <thead>
                <tr class="align-center">
                    <th>Username</th>
                    <th>Issue Count</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in user_rank" :key="user.name" class="align-center">
                    <td>{{ user.name }}</td>
                    <td>{{ user.issue_count }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
export default{
    name: 'UserStats',
    data(){
        return {
            user: JSON.parse(localStorage.getItem('user')),
            token: localStorage.getItem('auth_token'),
            user_rank: [],
            fav_author_path: '',
            section_dist_path: ''
        }
    }, 
    methods:{
        getImage(path){
            // console.log('require', import('@/assets/graphs/'+path))
            return require('@/assets/graphs/'+path);
        },
        async getUserStats(){
            try{
                const res = await fetch('http://localhost:8000/api/user-stats', {
                    method: 'GET',
                    mode: 'cors',
                    credentials: 'include',
                    headers: {
                        'Authorization': this.token
                    }
                })
                if (!res.ok) { throw Error("HTTP Error at User Stats:"+res.status) }
                const data = await res.json() ;
                this.user_rank = data.ranking;  // set output
                this.fav_author_path = this.getImage(data.fav_author_path);
                this.section_dist_path = this.getImage(data.section_dist_path);
                console.log(this.fav_author_path, this.section_dist_path)
            }catch(error){console.log(error);} 
        }
    },
    async created(){
        await this.getUserStats();

    }
}
</script>

<style scoped>
h3, h5{
    text-align: center;
}
th{
    font-weight: 500;
    font-size: large;
    color: white;
    background-color: purple;
}
</style>