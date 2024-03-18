<template>
    <PopupMessage v-if="showPopup" :message="message" @cancel="handelCancel"></PopupMessage>
    
    <div class="container d-flex justify-content-center p-5">
        <form class="h-100" @submit.prevent="registerUser">
            <legend>New User Registration</legend>
            <div class="row mb-3 p-2">
                <label for="email" class="col-sm-3 col-form-label" >Email</label>
                <div class="col-sm-9">
                    <input type="email" class="form-control" id="email" v-model="email" />
                </div>
            </div>
            <div class="row mb-3 p-2">
                <label for="email" class="col-sm-3 col-form-label" >Username</label>
                <div class="col-sm-9">
                    <input type="text" class="form-control" id="name" v-model="name" />
                </div>
            </div>
            <div class="row mb-3 p-2">
                <label for="password" class="col-sm-3 col-form-label">Password</label>
                <div class="col-sm-9">
                    <input type="password" class="form-control" id="password" v-model="password" />
                </div>
            </div>
            <button type="submit" class="btn btn-warning" @click="loginUser">Register</button>
        </form>
    </div>
</template>

<script>
// import {mapMutations} from 'vuex'
import PopupMessage from './PopupMessage.vue';

export default { 
    name: 'RegistrationPage',
    components:{
        PopupMessage
    },
    data(){
        return {
            name: '',
            email: '',
            password: '',
            message: '',
            showPopup: false
        }
    },
    methods: {
        // ...mapMutations('auth',['SET_LOGIN_USER_DATA']),
        registerUser(){
            if (this.password==''||this.email==''||this.name==''){
                this.message = 'All field are compulsory!'
                this.showPopup=true;
                console.log(this.message, this.showPopup);
            }
            else { this.register(); }
        },
        async register(){
            console.log('Login API Called');
            this.message = 'Successfully Registered! Login Now!'
            this.showPopup=true;
        },
        handelCancel(){
            this.showPopup=false;
            console.log('canceled!')
        }
    }
}
</script>

