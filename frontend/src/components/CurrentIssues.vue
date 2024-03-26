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
                        <th v-if="user? (user.role==1? true: false): false">Issue ID</th>
                        <th v-if="user? (user.role==1? true: false): false">Book ID</th>
                        <th>Book Name</th>
                        <th>Section</th>
                        <th>Author</th>
                        <th>Issue Date</th>
                        <th>Due Date</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="align-center" v-for="issue in current_issues" :key="issue.user_id">
                        <td v-if="user? (user.role==1? true: false): false">{{ issue.user_id }}</td>
                        <td v-if="user? (user.role==1? true: false): false">{{ issue.b_id }}</td>
                        <td>{{ issue.b_name }}</td>
                        <td>{{ issue.s_name }}</td>
                        <td>{{ issue.a_name }}</td>
                        <td>{{ issue.issue_date }}</td>
                        <td>{{ issue.due_date }}</td>
                        <td>
                            <div v-if="user? (user.role==1? true: false): false">
                                <!-- Revoke -->
                                <button type="button" class="btn btn-danger" 
                                data-bs-toggle="modal" data-bs-target="#AppAlert" 
                                @click="postIssueApproval(0,issue.b_id, issue.user_id)">
                                    Revoke
                                </button>
                            </div>
                            <div v-if="user? (user.role==2? true: false): false">
                                <!-- Read Book -->
                                <button type="button" class="btn btn-success" 
                                data-bs-toggle="modal" data-bs-target="#AppAlert" 
                                @click="postIssueApproval(1,issue.b_id, issue.user_id)">
                                    Read
                                </button>
                                <!-- Read Book -->
                                <button type="button" class="btn btn-warning" 
                                data-bs-toggle="modal" data-bs-target="#AppAlert" 
                                @click="postIssueApproval(1,issue.b_id, issue.user_id)">
                                    Download
                                </button>
                                <!-- Return -->
                                <button type="button" class="btn btn-danger" 
                                data-bs-toggle="modal" data-bs-target="#AppAlert" 
                                @click="postIssueApproval(0,issue.b_id, issue.user_id)">
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