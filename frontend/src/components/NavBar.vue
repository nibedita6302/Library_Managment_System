<template>
  <nav class="navbar navbar-expand-lg navbar-dark">
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
          <li v-if="this.getRole()>1" class="nav-item">
            <router-link to='/mybooks' active-class="active" class="nav-link">My Books</router-link>
          </li>
          <li v-if="this.getRole()>1" class="nav-item">
            <router-link to='/mystats' active-class="active" class="nav-link">My Stats</router-link>
          </li>
          <li v-if="this.getRole()>1" class="nav-item">
            <router-link to='/myprofile' active-class="active" class="nav-link">My Profile</router-link>
          </li>

          <!-- Librarian -->
          <li v-if="this.getRole()==1" class="nav-item">
            <router-link to='/issues' active-class="active" class="nav-link">Issues</router-link>
          </li>
          <li v-if="this.getRole()==1" class="nav-item">
            <router-link to='/analytics' active-class="active" class="nav-link">Analytics</router-link>
          </li>

          <!-- Login & Logout -->
          <li v-if="this.getRole()==null" class="nav-item">
            <router-link to='/login' active-class="active" class="nav-link">Login</router-link>
          </li>
          <li v-else class="nav-item">
            <LogoutUser />
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import LogoutUser from '@/components/LogoutUser.vue'

export default {
  name: 'NavBar',
  data(){
    return {
      user: {},
    }
  },
  components:{
    LogoutUser
  },
  methods:{
    getLoggedInUser(){
      const user = localStorage.getItem('user');
      if (user){
        this.user = JSON.parse(user);
      }else{
        this.user = {};
      }
    },
    getRole(){
      if (this.user){
        return this.user.role;
      }
      return null
    }
  },
  created(){
    this.getLoggedInUser();
  }
}
</script>

<style scoped>
  .active {
    border-bottom: 2px solid white;
  }
  .navbar{
    background-color: brown;
    font-size: large;
  }
</style>
 

