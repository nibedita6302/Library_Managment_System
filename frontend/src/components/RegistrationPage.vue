<template>
    <!-- Modal -->
    <div class="modal fade" id="logoutAlert" tabindex="-1" aria-labelledby="modallabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <p class="modal-title" id="modallabel">{{ message }}</p>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" 
                    aria-label="Close"></button>
                </div>
                <div class="modal-footer">
                    <button v-if="showCancel" class="btn btn-outline-danger" type="button" 
                    data-bs-dismiss="modal" aria-label="Close">
                        {{ cancel_text? cancel_text: 'Close' }}
                    </button> &nbsp;
                    <button v-if="showConfirm" @click="handleConfirm" type="button" class="btn btn-outline-success">
                        {{ confirm_text? confirm_text: 'Confirm' }}
                    </button>
                </div>
            </div>
        </div>
    </div>
    
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
            <button type="submit" class="btn btn-warning" data-bs-toggle="modal" data-bs-target="#logoutAlert" 
            @click="registerUser">Register</button>
        </form>
    </div>
</template>

<script>
export default { 
    name: 'RegistrationPage',
    data(){
        return {
            name: '',
            email: '',
            password: '',
            message: '',
            showConfirm: false,
            showCancel: false,
            cancel_text: null,
            confirm_text: null
        }
    },
    methods: {
        registerUser(){
            if (this.password==''||this.email==''||this.name==''){
                this.message = 'All field are compulsory!'
            }
            else { 
                this.message = 'Registering New User will logout your current session. \
                Are you sure you want to continue?'
                this.showConfirm=true;
                this.showCancel=true;
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
                    this.showCancel = true;
                    this.cancel_text = 'Okay';
                    this.message = data.message.error;     // set error message
                }
                else {    
                    this.message = data.message.success;   // set success message
                }
            }catch(error){console.log(error);} 
        },
        handleConfirm(){
            this.showConfirm=false;
            this.showCancel=false;
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