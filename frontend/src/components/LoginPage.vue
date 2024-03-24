<template>
    <PopupMessage v-if="showPopup" :message="message" :alert_type="alert_type"
    @cancel="handelCancel"></PopupMessage>
    
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
            <button type="submit" class="btn btn-success" @click="loginUser">Login</button>
        </form>
    </div>
</template>

<script>
import PopupMessage from './PopupMessage.vue';

export default { 
    name: 'LoginPage',
    components:{
        PopupMessage
    },
    data(){
        return {
            email: '',
            password: '',
            message: '',
            showPopup: false,
            alert_type: null
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
                    this.showPopup=true;
                    this.alert_type='danger';
                    this.message = data.message.error;     // set error message
                }
                else { 
                    localStorage.setItem('auth_token', data.auth_token);    // set auth_token
                    // set logged in user data
                    const user = {              
                        'id':data.id,
                        'name':data.username,
                        'role':data.role,
                        'email':data.email
                    }
                    localStorage.setItem('user', JSON.stringify(user));    
                    this.showPopup=true;
                    this.alert_type='success';
                    this.message = data.message.success;   // set success message
                }
            }catch(error){console.log(error);} 
        },
        loginUser(){
            if (this.password==''||this.email==''){
                this.message = 'All field are compulsory!'
                this.showPopup=true;
                console.log(this.message, this.showPopup);
            }
            else { this.login(); }
        },
        handelCancel(){
            this.showPopup=false;
            this.alert_type=null;
            this.$router.go();      // refreshing
        }
    }
}
</script>


<style scoped>
.container{
    padding: 50px 10px 50px 10px;
}
</style>