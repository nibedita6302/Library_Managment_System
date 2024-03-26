<template>
    <!-- Modal -->
    <div class="modal fade" id="alert2" tabindex="-1" aria-labelledby="modallabel" aria-hidden="true">
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
        <h4>Current Issue</h4>
        <div class="container p-3">
            <table class="table table-success table-striped table-sm">
                <thead>
                    <tr class="align-center">
                        <th v-if="user? (user.role==1? true: false): false">Issue ID</th>
                        <th v-if="user? (user.role==1? true: false): false">Book ID</th>
                        <th>Section</th>
                        <th id="book_name">Book Name</th>
                        <th>Author</th>
                        <th>Issue Date</th>
                        <th>Due Date</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="align-center" v-for="issue in current_issues" :key="issue.issue_id">
                        <td v-if="user? (user.role==1? true: false): false">{{ issue.issue_id }}</td>
                        <td v-if="user? (user.role==1? true: false): false">{{ issue.b_id }}</td>
                        <td>{{ issue.s_name }}</td>
                        <td id="book_name">{{ issue.b_name }}</td>
                        <td>{{ issue.a_name }}</td>
                        <td>{{ getDate(issue.issue_date) }}</td>
                        <td>{{ getDate(issue.due_date) }}</td>
                        <td>
                            <div v-if="user? (user.role==1? true: false): false">
                                <!-- Revoke -->
                                <button type="button" class="btn btn-danger" 
                                data-bs-toggle="modal" data-bs-target="#alert2" 
                                @click="revokeIssue(issue.issue_id)">
                                    <i class="bi bi-arrow-clockwise"></i>
                                    Revoke
                                </button>
                            </div>
                            <div v-if="user? (user.role==2? true: false): false">
                                <!-- Read Book -->
                                <button type="button" class="btn btn-primary" @click="readBook(issue.issue_id)">
                                    <i class="bi bi-book-half"></i>
                                    Read
                                </button>
                                <!-- Read Book -->
                                <button type="button" class="btn btn-success" @click="BuyBook(issue.issue_id)"
                                data-bs-toggle="modal" data-bs-target="#alert2" >
                                    <i class="bi bi-file-earmark-arrow-down-fill"></i>
                                    Download
                                </button>
                                <!-- Return -->
                                <button type="button" class="btn btn-secondary" @click="ReturnBook(issue.issue_id)" 
                                data-bs-toggle="modal" data-bs-target="#alert2" >
                                    <i class="bi bi-box-arrow-in-right"></i>
                                    Return
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
    name: 'CurrentIssues',
    data(){
        return{
            user: JSON.parse(localStorage.getItem('user')),
            token: localStorage.getItem('auth_token'),
            current_issues: [],
            message: ''
        }
    },
    methods:{
        getDate(date){
            var lst = date.split(" ");
            var newdate = lst[1]+" "+lst[2]+" "+lst[3];
            return newdate;
        },
        async fetchCurrentIssues(){
            try{
                const res = await fetch("http://localhost:8000/api/current-issues", {
                    method: 'GET',
                    mode: 'cors',
                    credentials: 'include',
                    headers:{
                        'Authorization': `${this.token}`,
                    }
                })
                if (!res.ok) { throw Error("HTTP Error at get author:"+res.status) }
                const data = await res.json() ;
                this.current_issues = data;  // set output
            }catch(error){console.log(error);} 
        },
        async readBook(issue_id){
            try{
                const res = await fetch("http://localhost:8000/api/book/read/"+issue_id, {
                    method: 'GET',
                    mode: 'cors',
                    credentials: 'include',
                    headers:{
                        'Authorization': `${this.token}`,
                    }
                })
                if (!res.ok && res.status!=400 && res.status!=403) { 
                    throw Error("HTTP Error at get author:"+res.status) 
                }
                const data = await res.json() ;
                if ('content_link_view' in data){
                    window.open(data.content_link_view, '_blank')
                }else{
                    this.message = data.message.error
                }
            }catch(error){console.log(error);} 
        },
        async BuyBook(issue_id){        // NOT WORKING
            try{
                const res = await fetch("http://localhost:8000/api/book/read/"+issue_id, {
                    method: 'GET',
                    mode: 'cors',
                    credentials: 'include',
                    headers:{
                        'Authorization': `${this.token}`,
                    }
                })
                if (!res.ok && res.status!=400 && res.status!=403) { 
                    throw Error("HTTP Error at get author:"+res.status) 
                }
                const data = await res.json() ;
                if ('content_link_view' in data){
                    console.log('download')
                }else{
                    this.message = data.message.error
                }
            }catch(error){console.log(error);} 

        },
        async ReturnBook(issue_id){
            try{
                const res = await fetch("http://localhost:8000/api/issue-requests/return/"+issue_id, {
                    method: 'PUT',
                    mode: 'cors',
                    credentials: 'include',
                    headers:{
                        'Authorization': `${this.token}`,
                    }
                })
                if (!res.ok && res.status!=400) { throw Error("HTTP Error at get author:"+res.status)}
                const data = await res.json() ;
                if (res.status==400){
                    this.message = data.message.error;
                }else{
                    this.message = data.message.success;
                }
            }catch(error){console.log(error);} 
        }
    },
    created(){
        this.fetchCurrentIssues();
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
    background-color: darkslategray;
}
#book_name{
    width: 350px;
}
button{
    font-size: small;
}
</style>