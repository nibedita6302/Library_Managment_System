<template>
    <div class="container">
        <div class="row">
            <div class="col-sm-6">
                <LoginPage></LoginPage>
            </div>
            <div class="col-sm-6">
                <RegistrationPage></RegistrationPage>
            </div>
        </div>
    </div>
</template>

<script>
import LoginPage from '@/components/LoginPage.vue';
import RegistrationPage from '@/components/RegistrationPage.vue'

export default{
    name: 'LoginView',
    components:{
        LoginPage,
        RegistrationPage,
    }
}

</script>

<style>
form {
    border: 1px solid black;
    text-align: center;    
    padding: 10%;
}
legend {
    font-weight: 600;
    font-size: x-large;
    text-align: center;
    padding: 1%;
}
</style>