<template>
    <!-- Modal -->
    <div class="modal fade" id="loginAlert" tabindex="-1" aria-labelledby="modallabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <p class="modal-title" id="modallabel">
                        <i v-if="error==0" class="bi bi-check-circle-fill" style="color: green;"></i>
                        <i v-else class="bi bi-x-circle-fill" style="color: red;"></i>
                        &nbsp;
                        {{ message }}
                    </p>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" 
                    aria-label="Close"></button>
                </div>
            </div>
        </div>
    </div>
    
    <div class="container d-flex justify-content-center">
        <form class="h-100" @submit.prevent="loginUser">
            <legend>Login</legend>
            <div class="row mb-3 p-2">
                <label for="loginEmail" class="col-sm-3 col-form-label" >Email</label>
                <div class="col-sm-9">
                    <input type="email" class="form-control" id="loginEmail" v-model="email" />
                </div>
            </div>
            <div class="row mb-3 p-2">
                <label for="loginPass" class="col-sm-3 col-form-label">Password</label>
                <div class="col-sm-9">
                    <input type="password" class="form-control" id="loginPass" v-model="password" />
                </div>
            </div>
            <div class="row mb-3 p-4"></div>
            <button type="submit" class="btn btn-success" data-bs-toggle="modal" data-bs-target="#loginAlert" 
            @click="loginUser">Login</button>
        </form>
    </div>
</template>

<script>
export default { 
    name: 'LoginPage',
    data(){
        return {
            email: '',
            password: '',
            message: '',
            showPopup: false,
            error: 1
        }
    },
    methods: {
        async login(){
            try{
                const res = await fetch('http://localhost:8000/api/login', {
                    method: 'POST',
                    mode: 'cors',
                    credentials: 'include',
                    headers: {
                        'Content-Type':'application/json',
                    },
                    body: JSON.stringify({
                        'email':this.email,
                        'password': this.password
                    })
                })
                if (!res.ok && res.status!=400) { throw Error("HTTP Error at Search:"+res.status) }
                const data = await res.json() ;
                if (res.status==400){
                    this.message = data.message.error;     // set error message
                    this.error=1;
                }
                else { 
                    this.message = data.message.success;   // set success message
                    this.error=0;
                    localStorage.setItem('auth_token', data.auth_token);    // set auth_token
                    // set logged in user data
                    const user = {              
                        'user_id':data.user_id,
                        'name':data.username,
                        'role':data.role,
                        'email':data.email
                    }
                    localStorage.setItem('user', JSON.stringify(user));  
                    this.$router.go();      // refreshing
                }
            }catch(error){console.log(error);} 
        },
        loginUser(){
            if (this.password==''||this.email==''){
                this.message = 'All field are compulsory!'
                this.error=1;
                // this.showPopup=true;
            }
            else { this.login(); }
        }
    }
}
</script>


<style scoped>
.container{
    padding: 50px 10px 50px 10px;
}
</style>