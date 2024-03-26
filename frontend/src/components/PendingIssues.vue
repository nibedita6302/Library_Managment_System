<template>
    <!-- Modal -->
    <div class="modal fade" id="AppAlert" tabindex="-1" aria-labelledby="modallabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <p class="modal-title" id="modallabel">
                        {{ message }}
                    </p>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" 
                    aria-label="Close"></button>
                </div>
            </div>
        </div>
    </div>

    <div class="container p-4">
        <h4>Pending Issue</h4>
        <div class="container p-3">
            <table class="table table-warning table-striped table-sm">
                <thead>
                    <tr class="align-center">
                        <th v-if="user? (user.role==1? true: false): false">User ID</th>
                        <th v-if="user? (user.role==1? true: false): false">Book ID</th>
                        <th>Book Name</th>
                        <th>Section</th>
                        <th>Author</th>
                        <th v-if="user? (user.role==1? true: false): false">Approval</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="align-center" v-for="issue in pending_issues" :key="issue.user_id">
                        <td v-if="user? (user.role==1? true: false): false">{{ issue.user_id }}</td>
                        <td v-if="user? (user.role==1? true: false): false">{{ issue.b_id }}</td>
                        <td>{{ issue.b_name }}</td>
                        <td>{{ issue.s_name }}</td>
                        <td>{{ issue.a_name }}</td>
                        <td v-if="user? (user.role==1? true: false): false">
                            <div class="btn-group" role="group" aria-label="Basic example">
                                <!-- Accept -->
                                <button type="button" class="btn btn-success" 
                                data-bs-toggle="modal" data-bs-target="#AppAlert" 
                                @click="postIssueApproval(1,issue.b_id, issue.user_id)">
                                    <i class="bi bi-check-square-fill"></i>
                                </button>
                                <!-- Reject -->
                                <button type="button" class="btn btn-danger" 
                                data-bs-toggle="modal" data-bs-target="#AppAlert" 
                                @click="postIssueApproval(0,issue.b_id, issue.user_id)">
                                    <i class="bi bi-x-square-fill"></i>
                                </button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>

export default{
    name: 'PendingIssues',
    data(){
        return{
            user: JSON.parse(localStorage.getItem('user')),
            token: localStorage.getItem('auth_token'),
            pending_issues: [],
            message: ''
        }
    },
    methods:{
        async fetchPendingIssues(){
            try{
                const res = await fetch("http://localhost:8000/api/pending-issues", {
                    method: 'GET',
                    mode: 'cors',
                    credentials: 'include',
                    headers:{
                        'Authorization': `${this.token}`,
                    }
                })
                if (!res.ok) { throw Error("HTTP Error at get author:"+res.status) }
                const data = await res.json() ;
                this.pending_issues = data;  // set output
            }catch(error){console.log(error);} 
        },
        async postIssueApproval(approval, b_id, u_id){
            try{
                const res = await fetch("http://localhost:8000/api/issue-requests/approval/"+b_id+'/'+u_id, {
                    method: 'PUT',
                    mode: 'cors',
                    credentials: 'include',
                    headers:{
                        'Content-Type': 'application/json',
                        'Authorization': `${this.token}`,
                    },
                    body: JSON.stringify({'approval':approval})
                })
                if (!res.ok && res.status!=400) { throw Error("HTTP Error at pending issue:"+res.status) }
                const data = await res.json() ;
                if (res.status==400){
                    this.error = data.message.error;  // set error
                }else{
                    this.message = data.message.success;
                }
            }catch(error){console.log(error);} 
        }
    },
    created(){
        this.fetchPendingIssues();
    }
}
</script>

<style scoped>
h4{
    text-align: center;
}
th{
    font-weight: 500;
    font-size: large;
    color: white;
    background-color: darkgoldenrod;
}
</style>