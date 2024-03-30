<template>
    <!-- Modal -->
    <div class="modal fade" id="modal" tabindex="-1" aria-labelledby="modallabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <p class="modal-title" id="modallabel">{{ message }}</p>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" 
                    aria-label="Close" @click="handleClose"></button>
                </div>
            </div>
        </div>
    </div>

    <!-- Button trigger modal -->
    <a href="#" class="nav-link" data-bs-toggle="modal" data-bs-target="#modal" 
    @click="logoutUser">Logout</a>

</template>

<script>
export default{
    name: 'LogoutUser',
    data(){
        return {
            message: ''
        }
    },
    methods:{
        async logoutUser(){
            try{
                const res = await fetch('http://localhost:8000/api/logout', {
                    method: 'POST',
                    mode: 'cors',
                    credentials: 'include'
                })
                if (!res.ok && res.status!=400) { throw Error("HTTP Error at Search:"+res.status) }
                const data = await res.json() ;
                if (res.status==400){
                    this.message = data.message.error;     // remove error message
                    localStorage.removeItem('auth_token');   // remove auth_token
                    localStorage.removeItem('user');         // remove user
                }
                else { 
                    this.message = data.message.success;     // set success message
                    localStorage.removeItem('auth_token');   // remove auth_token
                    localStorage.removeItem('user');         // remove user
                }
            }catch(error){console.log(error);}
        },
        handleClose(){
            this.$router.push('/login');  // reload page
        }
    }
}
</script>

<style scoped>

</style>
