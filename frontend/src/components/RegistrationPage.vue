<template>
    <PopupMessage v-if="showPopup" :message="message" :cancel_text="cancel_text"
    :show-confirm="show_confirm" :confirm_text="confirm_text" :alert_type="alert_type"
    @confirm="handelConfirm" @cancel="handelCancel"></PopupMessage>
    
    <div class="container d-flex justify-content-center">
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
            <button type="submit" class="btn btn-warning" @click="registerUser">Register</button>
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
            show_confirm: false,
            cancel_text: null,
            confirm_text: null,
            showPopup: false,
            alert_type: null
        }
    },
    methods: {
        // ...mapMutations('auth',['SET_LOGIN_USER_DATA']),
        registerUser(){
            if (this.password==''||this.email==''||this.name==''){
                this.message = 'All field are compulsory!'
                this.showPopup=true;
                // console.log(this.message, this.showPopup);
            }
            else { 
                this.message = 'Registering New User will logout your current session. \
                Are you sure you want to continue?'
                this.showPopup=true;
                this.show_confirm=true;
                this.cancel_text="Cancel";
                this.confirm_text='Continue';
            }
        },
        async register(){
            try{
                const res = await fetch('http://localhost:8000/api/user-registration', {
                    method: 'POST',
                    mode: 'cors',
                    credentials: 'include',
                    headers: {
                        'Content-Type':'application/json',
                    },
                    body: JSON.stringify({
                        'name': this.name,
                        'email':this.email,
                        'password': this.password
                    })
                })
                if (!res.ok && res.status!=400) { throw Error("HTTP Error at Search:"+res.status) }
                const data = await res.json() ;
                if (res.status==400){
                    this.showPopup=true;
                    this.alert_type='danger'
                    this.message = data.message.error;     // set error message
                }
                else {    
                    this.showPopup=true;
                    this.alert_type='success';
                    this.message = data.message.success;   // set success message
                }
            }catch(error){console.log(error);} 
        },
        handelCancel(){
            this.showPopup=false;
            this.alert_type=null;
            console.log('canceled!')
        },
        handelConfirm(){
            this.showPopup=false;
            this.alert_type=null;
            this.show_confirm=false;
            this.cancel_text=null;
            this.confirm_text=null;
            this.register(); 
        }
    }
}
</script>

<style scoped>
.container{
    padding: 50px 10px 50px 10px;
}
</style>