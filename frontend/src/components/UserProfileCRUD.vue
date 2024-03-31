<template>
    <!-- Modal -->
    <div class="modal fade" id="info8" tabindex="-1" aria-labelledby="modallabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <p class="modal-title" id="modallabel">{{ message }}</p>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" 
                    aria-label="Close"></button>
                </div>
            </div>
        </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div class="modal fade" id="deleteProfile" tabindex="-1" aria-labelledby="modallabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-body">
                    <p class="modal-title" id="modallabel">
                        All your current issues will get deleted. Click confirm to delete your profile.
                    </p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-success" data-bs-dismiss="modal" aria-label="Close"
                    data-bs-toggle="modal" data-bs-target="#info5" @click="deleteProfile()">
                        Confirm
                    </button> 
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                </div>
            </div>
        </div>
    </div>

    <div class="container d-flex justify-content-center p-5">
        <form @submit.prevent="updateProfile">
            <legend>My Profile</legend>
            <div class="row mb-3 p-1">
                <label for="name" class="col-sm-3 col-form-label" >Username</label>
                <div class="col-sm-9">
                    <input type="text" class="form-control" id="name" v-model="username" 
                    :placeholder="profile.name" />
                </div>
            </div>
            <div class="row mb-3 p-1">
                <label for="loginEmail" class="col-sm-3 col-form-label" >Email</label>
                <div class="col-sm-9">
                    <input type="email" class="form-control" id="loginEmail" v-model="email" 
                    :placeholder="profile.email"/>
                </div>
            </div>
            <button type="submit" class="btn btn-warning" 
            data-bs-toggle="modal" data-bs-target="#info8">Update</button>
        </form>
    </div>

    <div class="d-flex justify-content-center p-4" id="btn-delete">
        <button type="submit" class="btn btn-danger" 
        data-bs-toggle="modal" data-bs-target="#deleteProfile">Delete Profile</button>
    </div>
</template>

<script>
export default{
    name: 'UserProfileCRUD',
    data(){
        return {
            user: JSON.parse(localStorage.getItem('user')),
            token: localStorage.getItem('auth_token'),
            profile: {}, 
            username: '',
            email: '', 
            message: ''

        }
    },
    methods:{
        async fetchUserProfile(){
            try{
                const res = await fetch('http://localhost:8000/api/user/profile', {
                    method: 'GET',
                    mode: 'cors',
                    credentials: 'include',
                    headers: {
                        'Authorization': this.token
                    }
                })
                if (!res.ok && res.status!=400) { throw Error("HTTP Error at fetch User profile:"+res.status) }
                const data = await res.json() ;
                if (res.status==400){ this.message=data.message.error }
                else {this.profile = data;}
            }catch(error){console.log(error);} 
        },
        async updateProfile(){
            try{
                const res = await fetch('http://localhost:8000/api/user/profile/update', {
                    method: 'PUT',
                    mode: 'cors',
                    credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': this.token
                    },
                    body: JSON.stringify({'name':this.username, 'email':this.email})
                })
                if (!res.ok && res.status!=400) { throw Error("HTTP Error at Profile Update:"+res.status) }
                const data = await res.json() ;
                if (res.status==400){ this.message=data.message.error }
                else {this.message=data.message.success}
            }catch(error){console.log(error);} 
        }, 
        async deleteProfile(){
            try{
                const res = await fetch('http://localhost:8000/api/user/profile/delete', {
                    method: 'DELETE',
                    mode: 'cors',
                    credentials: 'include',
                    headers: {
                        'Authorization': this.token
                    }
                })
                if (!res.ok && res.status!=400) { throw Error("HTTP Error at Profile delete:"+res.status) }
                const data = await res.json() ;
                if (res.status==400){ this.message=data.message.error }
                else {
                    this.message=data.message.success;
                    this.$router.push('/login')
                }
            }catch(error){console.log(error);} 
        }
    }, 
    created(){
        this.fetchUserProfile();
    }
}
</script>

<style scoped>
</style>