<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <!-- Toggle Button -->
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#nav" 
        aria-controls="nav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-center" id="nav">
        <ul class="navbar-nav">
          <!-- Common Home -->
          <li class="nav-item"> 
            <router-link to="/" active-class="active" class="nav-link" aria-current="page">Home</router-link>  
          </li>

          <!-- User -->
          <li class="nav-item">
            <router-link to='/mybooks' active-class="active" class="nav-link">My Books</router-link>
          </li>
          <li class="nav-item">
            <router-link to='/mystats' active-class="active" class="nav-link">My Stats</router-link>
          </li>
          <li class="nav-item">
            <router-link to='/myprofile' active-class="active" class="nav-link">My Profile</router-link>
          </li>

          <!-- Librarian -->
          <li class="nav-item">
            <router-link to='/issues' active-class="active" class="nav-link">Issues</router-link>
          </li>
          <li class="nav-item">
            <router-link to='/analytics' active-class="active" class="nav-link">Analytics</router-link>
          </li>

          <!-- Login & Logout -->
          <li class="nav-item">
            <router-link to='/login' active-class="active" class="nav-link">Login</router-link>
          </li>
          <li class="nav-item">
            <!-- <LogoutAlert /> -->
            Logout
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
// import LogoutAlert from './LogoutAlert.vue'
// import {mapGetters} from "vuex"

export default {
  name: 'NavBar',
  // components:{
  //   LogoutAlert
  // },
  methods:{
    refresh(){
      const router = this.$router
      router.push('/')
    }
  }
  // computed:{
  //   ...mapGetters('auth',['GET_USER_ROLE'])
  // }
}
</script>

<style scoped>
  .active {
    border-bottom: 2px solid white;
  }
</style>
 

