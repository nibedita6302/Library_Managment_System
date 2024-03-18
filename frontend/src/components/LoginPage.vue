<template>
    <PopupMessage v-if="showPopup" :message="message" @cancel="handelCancel"></PopupMessage>
    
    <div class="container d-flex justify-content-center p-5">
        <form class="h-100" @submit.prevent="loginUser">
            <legend>Login</legend>
            <div class="row mb-3 p-2">
                <label for="email" class="col-sm-3 col-form-label" >Email</label>
                <div class="col-sm-9">
                    <input type="email" class="form-control" id="email" v-model="email" />
                </div>
            </div>
            <div class="row mb-3 p-2">
                <label for="password" class="col-sm-3 col-form-label">Password</label>
                <div class="col-sm-9">
                    <input type="password" class="form-control" id="password" v-model="password" />
                </div>
            </div>
            <div class="row mb-3 p-4"></div>
            <button type="submit" class="btn btn-success" @click="loginUser">Login</button>
        </form>
    </div>
</template>

<script>
// import {mapMutations} from 'vuex'
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
            showPopup: false
        }
    },
    methods: {
        // ...mapMutations('auth',['SET_LOGIN_USER_DATA']),
        loginUser(){
            if (this.password==''||this.email==''){
                this.message = 'All field are compulsory!'
                this.showPopup=true;
                console.log(this.message, this.showPopup);
            }
            else { this.login(); }
        },
        async login(){
            console.log('Login API Called');
            // this.$router.push('/')
        },
        handelCancel(){
            this.showPopup=false;
            console.log('canceled!')
        }
    }
}
</script>

